import asyncio
import websockets

# Configuração do servidor WebSocket
HOST = "127.0.0.1"
PORT = 8080

async def handle_client(websocket, path):
    try:
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            
            # Simula resposta
            if message == b'\x07gabriel\x041234':
                await websocket.send("Login bem-sucedido")
            else:
                await websocket.send("Login falhou")
    except websockets.exceptions.ConnectionClosed:
        print("Conexão fechada")

start_server = websockets.serve(handle_client, HOST, PORT)

print(f"Servidor WebSocket rodando em {HOST}:{PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
