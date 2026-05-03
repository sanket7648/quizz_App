from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        # Maps session_id to a list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Maps session_id to scores: {"session_123": {"player1": 10, "player2": 5}}
        self.scores: Dict[str, Dict[str, int]] = {}

    async def connect(self, websocket: WebSocket, session_id: str, player_name: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
            self.scores[session_id] = {}
            
        self.active_connections[session_id].append(websocket)
        self.scores[session_id][player_name] = 0
        
        # Notify others in the room
        await self.broadcast(session_id, {
            "type": "system",
            "message": f"{player_name} has joined the challenge!"
        })

    # FIXED: Made this an async function to safely await the broadcast
    async def disconnect(self, websocket: WebSocket, session_id: str, player_name: str):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            
            if not self.active_connections[session_id]:
                # Clean up if room is empty
                del self.active_connections[session_id]
                del self.scores[session_id]
            else:
                # Announce departure
                await self.broadcast(session_id, {
                    "type": "system",
                    "message": f"{player_name} disconnected."
                })

    async def broadcast(self, session_id: str, message: dict):
        """Sends a JSON message to all players in a specific session."""
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_text(json.dumps(message))

    def update_score(self, session_id: str, player_name: str, points: int):
        if session_id in self.scores:
            self.scores[session_id][player_name] += points

manager = ConnectionManager()