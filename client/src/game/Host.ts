import { ref, reactive } from 'vue';

export class Host {
    room_num = ref<number>(0);
    game_token = ref<string>('');
    players = reactive<string[]>([]);

    constructor(room_num: number, game_token?: string) {
        this.room_num.value = room_num;
        this.game_token.value = game_token ?? '';
    }

    addPlayer(player: string) {
        this.players.push(player);
    }

    removePlayer(removedPlayer: string) {
        const index = this.players.indexOf(removedPlayer);
        if (index !== -1) {
            this.players.splice(index, 1); // keeps reactivity
        }
    }
}
