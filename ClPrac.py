import socket
import threading

HOST = '127.0.0.1'
PORT = 5001

clients = {}
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with clients_lock:
        disconnected = []
        for sock, addr in clients.items():
            if sock != sender_socket:
                try:
                    sock.send(message)
                except:
                    disconnected.append(sock)
        for sock in disconnected:
            del clients[sock]

def handle_client(client_socket, client_address):
    with clients_lock:
        clients[client_socket] = client_address

    print(f'[+] Новый клиент: {client_address}')
    client_socket.send("Добро пожаловать в чат!".encode('utf-8'))
    broadcast(f"Участник {client_address} присоединился.".encode('utf-8'), sender_socket=client_socket)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8').strip()
            if msg == 'exit':
                break
            print(f'{client_address}: {msg}')
            broadcast(f"{client_address}: {msg}".encode('utf-8'), sender_socket=client_socket)
    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            if client_socket in clients:
                del clients[client_socket]
        print(f'[-] Клиент отключился: {client_address}')
        broadcast(f"Участник {client_address} покинул чат.".encode('utf-8'))
        client_socket.close()

# Запуск сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f'Сервер запущен на {HOST}:{PORT} и ждёт клиентов...')

try:
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
        thread.start()
except KeyboardInterrupt:
    print("\nСервер завершает работу.")
finally:
    server_socket.close()