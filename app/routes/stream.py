from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/stream")
async def stream(websocket: WebSocket):

    await websocket.accept()

    session_id = str(uuid4())[:8]

    print(f"🟢 {session_id} Connected")

    total_bytes = 0

    try:

        while True:

            chunk = await websocket.receive_bytes()

            total_bytes += len(chunk)

            await websocket.send_json({
                "type": "ack",
                "session": session_id,
                "chunk": len(chunk),
                "total": total_bytes,
            })

    except WebSocketDisconnect:

        print(
            f"🔴 {session_id} Disconnected "
            f"({total_bytes} bytes)"
        )