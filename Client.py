import socket
import threading

HOST = '127.0.0.1'
PORT = 5001

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\nСоединение с сервером потеряно.")
                break
            print(f"\r{data.decode('utf-8')}\n> ", end='')
        except ConnectionResetError:
            print("\nСоединение разорвано.")
            break
        except OSError:
            break

def send_messages(sock):
    print("Введите сообщение (или 'exit' для выхода):")
    while True:
        try:
            msg = input("> ")
            if msg.lower() == 'exit':
                sock.send('exit'.encode('utf-8'))
                break
            sock.send(msg.encode('utf-8'))
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение работы...")
            sock.send('exit'.encode('utf-8'))
            break

# Основной код клиента
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_sock.connect((HOST, PORT))
    print("Подключены к чат-серверу.")

    recv_thread = threading.Thread(target=receive_messages, args=(client_sock,), daemon=True)
    recv_thread.start()

    send_messages(client_sock)

except ConnectionRefusedError:
    print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
finally:
    client_sock.close()
    print("Соединение закрыто.")