# Group Kahoot

## Installation
You can run this through docker or manually:

### Docker Run
1. Install [docker](https://www.docker.com/).
2. Clone the repo
3. Run `docker compose up --build` in the root folder
4. Go to `http://localhost`

### Manual Run (Recommended for active development)
#### Frontend
1. Install [node.js](https://nodejs.com)
3. open terminal in root
4. `cd client`
5. `npm install`
6. `npm run dev`
#### Backend
I would recommend still using docker for backend, as C++ doesn't benefit from live updating like js does.
1. Install [docker](https://www.docker.com/).
2. Open terminal in root
3. `cd server`
4. `docker build -t kahoot-server .`
5. `docker run -it --rm -p 8080:8080 kahoot-server`

## Contributing
- Make sure you only push working code to main