import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = []
log_file = "chat_log.txt"

def broadcast(message, sender_socket):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                clients.remove(client)

def handle_client(client_socket, address):
    print(f"[+] Połączono z {address}")
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                broadcast(msg, client_socket)
            else:
                break
        except:
            break
    print(f"[-] Rozłączono z {address}")
    clients.remove(client_socket)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"🛰️ Serwer nasłuchuje na porcie {PORT}...")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
