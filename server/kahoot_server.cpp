// kahoot_server.cpp
// Build with: g++ -std=c++17 kahoot_server.cpp -lboost_system -lpthread
// Make sure Boost headers/libs are installed.

#include <boost/asio.hpp>
#include <boost/beast.hpp>
#include <boost/beast/websocket.hpp>
#include <boost/asio/steady_timer.hpp>
#include <iostream>
#include <string>
#include <memory>
#include <set>
#include <map>
#include <deque>
#include <nlohmann/json.hpp>


using tcp = boost::asio::ip::tcp;
namespace websocket = boost::beast::websocket;
using json = nlohmann::json;
using namespace std::chrono_literals;

class Session : public std::enable_shared_from_this<Session> {
public:
    websocket::stream<tcp::socket> ws;
    std::string name;
    int player_id = -1;
    Session(tcp::socket socket) : ws(std::move(socket)) {}

    void start(std::function<void(std::shared_ptr<Session>, const json&)> on_msg,
               std::function<void(std::shared_ptr<Session>)> on_close) {
        on_message = on_msg;
        on_close_cb = on_close;
        ws.async_accept([self=shared_from_this()](boost::beast::error_code ec){
            if(ec) return;
            self->do_read();
        });
    }

    void send(const json& j) {
        auto txt = j.dump();
        // enqueue to avoid concurrent writes
        write_queue.push_back(txt);
        if(write_queue.size() == 1) do_write();
    }

private:
    std::deque<std::string> write_queue;
    boost::beast::flat_buffer buffer;
    std::function<void(std::shared_ptr<Session>, const json&)> on_message;
    std::function<void(std::shared_ptr<Session>)> on_close_cb;

    void do_read() {
        auto self = shared_from_this();
        ws.async_read(buffer, [self](boost::beast::error_code ec, std::size_t bytes){
            if(ec == boost::beast::websocket::error::closed) {
                if(self->on_close_cb) self->on_close_cb(self);
                return;
            }
            if(ec) {
                std::cerr << "read error: " << ec.message() << "\n";
                if(self->on_close_cb) self->on_close_cb(self);
                return;
            }
            std::string s = boost::beast::buffers_to_string(self->buffer.data());
            self->buffer.consume(self->buffer.size());
            try {
                auto j = json::parse(s);
                if(self->on_message) self->on_message(self, j);
            } catch(std::exception& e) {
                std::cerr << "json parse error: " << e.what() << " data=[" << s << "]\n";
            }
            self->do_read();
        });
    }

    void do_write() {
        auto self = shared_from_this();
        ws.async_write(boost::asio::buffer(write_queue.front()), [self](boost::beast::error_code ec, std::size_t){
            if(ec) {
                std::cerr << "write error: " << ec.message() << "\n";
                return;
            }
            self->write_queue.pop_front();
            if(!self->write_queue.empty()) self->do_write();
        });
    }
};

// Simple in-memory room
struct Player { std::shared_ptr<Session> sess; std::string name; int id; int points = 0; };

class GameRoom {
public:
    std::string code;
    std::map<int, Player> players;
    int next_player_id = 1;
    boost::asio::io_context& ioc;
    GameRoom(boost::asio::io_context& ioc_, const std::string& code_): ioc(ioc_), code(code_) {}

    void broadcast(const json& j) {
        for(auto & [id, p] : players) p.sess->send(j);
    }

    int add_player(std::shared_ptr<Session> s, const std::string& name) {
        int id = next_player_id++;
        players[id] = Player{ s, name, id };
        players[id].sess->player_id = id;
        players[id].sess->name = name;
        json j = { {"type","player_joined"}, {"id",id}, {"name",name} };
        broadcast(j);
        return id;
    }

    void remove_player(std::shared_ptr<Session> s) {
        int id = s->player_id;
        if(id > 0 && players.count(id)) {
            players.erase(id);
            json j = { {"type","player_left"}, {"id",id} };
            broadcast(j);
        }
    }

    // start a question: broadcast question JSON and start timer
    void start_question(int question_id, const json& question_payload, int duration_ms) {
        // add question id and duration
        json msg = question_payload;
        msg["type"] = "question";
        msg["question_id"] = question_id;
        msg["duration_ms"] = duration_ms;
        current_question_id = question_id;
        answers_received.clear();
        broadcast(msg);

        // set a timer to end the question
        timer = std::make_unique<boost::asio::steady_timer>(ioc, std::chrono::milliseconds(duration_ms));
        timer->async_wait([this](const boost::system::error_code& ec){
            if(ec) return;
            this->end_question();
        });
    }

    // handle player answer
    void handle_answer(int player_id, int question_id, int choice, int time_left_ms) {
        if(question_id != current_question_id) return;
        if(answers_received.count(player_id)) return; // ignore double answers
        answers_received[player_id] = {choice, time_left_ms};
        // immediate ack to player
        players[player_id].sess->send(json{{"type","answer_ack"},{"ok",true}});
        // optional: if all answered, end early
        if((int)answers_received.size() >= (int)players.size()) {
            if(timer) timer->cancel();
            end_question();
        }
    }

    void end_question() {
        // compute stats & scoring (example: assume answer 1 is correct)
        int correct_choice = 1; // for demo; replace with real data
        std::vector<int> counts(4,0);
        for(auto &kv : answers_received) {
            int choice = kv.second.choice;
            if(choice >=0 && choice<(int)counts.size()) counts[choice]++;
        }
        // scoring
        for(auto &kv : answers_received) {
            int pid = kv.first;
            int choice = kv.second.choice;
            int time_left_ms = kv.second.time_left_ms;
            if(choice == correct_choice) {
                int base = 1000;
                int bonus = std::max(0, time_left_ms * 1000 / 100); // simplified
                players[pid].points += base + bonus;
            }
        }
        // broadcast result & leaderboard
        json stats = { {"type","question_ended"}, {"counts", counts} };
        broadcast(stats);
        json lb;
        lb["type"] = "leaderboard";
        lb["top"] = json::array();
        for(auto &pr : players) {
            lb["top"].push_back({ {"id", pr.first}, {"name", pr.second.name}, {"points", pr.second.points} });
        }
        broadcast(lb);
    }

private:
    struct Answer { int choice; int time_left_ms; };
    std::map<int, Answer> answers_received;
    int current_question_id = -1;
    std::unique_ptr<boost::asio::steady_timer> timer;
};

int main() {
    try {
        boost::asio::io_context ioc{1};
        tcp::acceptor acceptor{ioc, tcp::endpoint{tcp::v4(), 8080}};

        // single demo room
        auto room = std::make_shared<GameRoom>(ioc, "ABCD");

        std::function<void()> do_accept;
        do_accept = [&](){
            acceptor.async_accept([&](boost::system::error_code ec, tcp::socket socket){
                if(ec) {
                    std::cerr << "accept error: " << ec.message() << "\n";
                    do_accept();
                    return;
                }
                auto session = std::make_shared<Session>(std::move(socket));
                session->start(
                    // on message
                    [&](std::shared_ptr<Session> s, const json& j){
                        try {
                            std::string t = j.value("type", "");
                            if(t == "join") {
                                std::string name = j.value("name","guest");
                                int id = room->add_player(s, name);
                                s->send(json{{"type","joined"},{"id",id},{"room",room->code}});
                            } else if(t == "answer") {
                                int qid = j.value("question_id",-1);
                                int choice = j.value("choice", -1);
                                int time_left = j.value("time_left_ms", 0);
                                room->handle_answer(s->player_id, qid, choice, time_left);
                            } else if(t == "start_question") {
                                int qid = j.value("question_id", 1);
                                json q = {
                                    {"text","What's 2+2?"},
                                    {"choices", json::array({"1","3","4","5"})}
                                };
                                room->start_question(qid, q, 15000);
                            }
                        } catch(...) {}
                    },
                    // on close
                    [&](std::shared_ptr<Session> s){
                        room->remove_player(s);
                    }
                );
                do_accept();
            });
        };
        do_accept();

        std::cout << "Server running on :8080\n";
        ioc.run();
    } catch(std::exception& e) {
        std::cerr << "Fatal: " << e.what() << "\n";
    }
    return 0;
}
