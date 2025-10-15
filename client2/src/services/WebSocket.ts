interface Options {
    onopen: (e: Event) => void,
    onclose: (e: Event) => void,
}

class WS {
    static webSocket: WebSocket;
    static initialized = false;
    static listeners = new Map<string, (e: Object) => void>();

    static initialize(url: string, options?: Options) {
        if (WS.initialized) return;
        WS.initialized = true;

        WS.webSocket = new WebSocket(url);
        console.log("initializing websocket...");
        WS.webSocket.onopen = options?.onopen ?? (() => console.log("Websocket open!"));
        WS.webSocket.onclose = options?.onclose ?? (() => console.log("Websocket closed!"));


        WS.webSocket.onmessage = WS.handleMessage;
    }

    /**
     * Looks to see if there is a listener for the event and runs it. 
    */
    private static handleMessage(rawEvent: MessageEvent) {
        const event = JSON.parse(rawEvent.data);
            if (!WS.listeners.has(event.type)) {
                console.error("Unhandled WS event: " + event.type);
                return;
            }
            WS.listeners.get(event.type)!(event);
    }

    static on(eventName: string, callback: (data: Object) => void) {
        WS.listeners.set(eventName, callback);
    }

    static emit(eventName: string, value: Object) {
        WS.webSocket.send(JSON.stringify({type: eventName, ...value})); // TODO: Change from ...value to value after server fixes
    } 
}

export { WS };