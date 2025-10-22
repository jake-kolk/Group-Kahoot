interface Options {
    onopen?: (e: Event) => void,
    onclose?: (e: Event) => void,
    onmessage?: (e: MessageEvent) => void,
    autoReconnect?: boolean
}

class WS {
    static webSocket: WebSocket;
    static initialized = false;
    private static listeners = new Map<string, (e: Object) => void>();
    private static url: string;
    private static options: Options

    static initialize(url: string, options?: Options) {
        if (WS.initialized) return;
        WS.initialized = true;

        WS.url = url;
        WS.options = options || {autoReconnect: true}; // default settings

        WS.connect();
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

    private static connect() {
        WS.webSocket = new WebSocket(WS.url);
        console.log("initializing websocket...");
        WS.webSocket.onopen = WS.options.onopen ?? (() => console.log("Websocket open!"));
        WS.webSocket.onclose = (ev: CloseEvent) => {
            if (WS.options.onclose) WS.options.onclose(ev);
            else console.warn("Websocket closed!", ev.code, ev.reason);
            
            if (WS.options.autoReconnect !== false) {
                console.log("Attempting to reconnect in 6 seconds.")
                setTimeout(WS.connect, 6000);
            }
        }

        WS.webSocket.onmessage = (event) => {
            WS.handleMessage(event);
            if (WS.options?.onmessage) WS.options.onmessage(event);
        };
    }

    static on(eventName: string, callback: (data: Object) => void) {
        WS.listeners.set(eventName, callback);
    }

    static emit(eventName: string, value: Object) {
        WS.webSocket.send(JSON.stringify({type: eventName, ...value})); // TODO: Change from ...value to value after server fixes
    }

    static removeListener(eventName: string) {
        WS.listeners.delete(eventName);
    }
}

export { WS };