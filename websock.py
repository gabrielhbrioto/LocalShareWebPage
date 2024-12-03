import asyncio
import websockets
import struct

# Dicionário para armazenar arquivos simulados
arquivo_storage = {
    "arquivo1": b"Conteúdo do arquivo 1",
    "arquivo2": b"Conteúdo do arquivo 2"
}

async def processar_mensagem(websocket, path):
    async for message in websocket:
        try:
            data = bytearray(message)

            # Decodifica username
            offset = 0
            username_len = data[offset]
            offset += 1
            username = data[offset:offset + username_len].decode("utf-8")
            offset += username_len
            print(f"Username: {username}")

            # Decodifica password
            password_len = data[offset]
            offset += 1
            password = data[offset:offset + password_len].decode("utf-8")
            offset += password_len
            print(f"Password: {password}")

            # Decodifica comando
            comando = data[offset]
            offset += 1
            print(f"Comando recebido: {comando}")

            if comando == 0x01:  # Solicitação de download
                # Decodifica nome do arquivo
                nome_arquivo_len = data[offset]
                offset += 1
                nome_arquivo = data[offset:offset + nome_arquivo_len].decode("utf-8")
                print(f"Arquivo solicitado: {nome_arquivo}")

                if nome_arquivo in arquivo_storage:
                    conteudo_arquivo = arquivo_storage[nome_arquivo]
                    tamanho_arquivo = len(conteudo_arquivo)

                    # Envia os dados no formato esperado
                    await websocket.send(struct.pack("!B", len(nome_arquivo)) + nome_arquivo.encode("utf-8"))
                    await websocket.send(struct.pack("!I", tamanho_arquivo))
                    for byte in conteudo_arquivo:
                        await websocket.send(bytes([byte]))
                    
                    print(f"Arquivo '{nome_arquivo}' enviado com sucesso!")
                else:
                    await websocket.send("Erro: Arquivo não encontrado.".encode("utf-8"))
                    print(f"Arquivo '{nome_arquivo}' não encontrado.")
            else:
                await websocket.send("Erro: Comando não reconhecido.".encode("utf-8"))
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            await websocket.send("Erro ao processar mensagem.".encode("utf-8"))

start_server = websockets.serve(processar_mensagem, "0.0.0.0", 8080)

print("Servidor WebSocket iniciado na porta 8080...")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
