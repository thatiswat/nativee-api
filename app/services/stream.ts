let socket: WebSocket | null = null;

export function connectStream() {

    socket = new WebSocket(
        "ws://YOUR-IP:8000/stream"
    );

    socket.onopen = () => {
        console.log("Connected");
    };

    socket.onmessage = (e) => {
        console.log(e.data);
    };

    socket.onerror = console.log;

    socket.onclose = () => {
        console.log("Closed");
    };
}

export function sendChunk(
    chunk: ArrayBuffer
) {

    socket?.send(chunk);

}