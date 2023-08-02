import threading
import socket

HOST = 'localhost'
PORT = 12400
ADDR = (HOST, PORT)
BUFSIZ = 2048


salas = { "Sala 1": {"clients": [], "usernames": []},
         "Sala 2": {"clients": [], "usernames": []},
         "Sala 3": {"clients": [], "usernames": []}}

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Servidor rodando...')
    try:
        server.bind(ADDR)
        server.listen()
    except OSError as e:
        print(f'Erro ao iniciar o servidor: {e}')
        return
    
    while True:
        client_sockt, client_address = server.accept()
        
        print('%s:%s está online.' % client_address)
        username = client_sockt.recv(2048).decode("utf8")

        if username in salas['Sala 1']['usernames'] or username in salas['Sala 2']['usernames'] or username in salas['Sala 3']['usernames']:
            while username in salas['Sala 1']['usernames'] or username in salas['Sala 2']['usernames'] or username in salas['Sala 3']['usernames']:
                mensagem = "Nome de usuário já em uso. Tente outro nome"
                client_sockt.send(mensagem.encode('utf-8'))
                username = client_sockt.recv(2048).decode("utf8")

        welcome = f"Bem vindo {username}!"
        client_sockt.send(bytes(welcome, "utf8"))
        client_sockt.send(bytes("Agora você pode enviar mensagens!", "utf8"))

        # Recebe a opção da sala escolhida
        sala = client_sockt.recv(2048).decode('utf-8')
        
        # adiciona o cliente à sala que ele escolheu
        salas[sala]['clients'].append(client_sockt)
        salas[sala ]['usernames'].append(username)
        print(salas[sala]['usernames'])

        thread = threading.Thread(target=messagesTreatment, args=[client_sockt, username, salas[sala]])
        thread.start()

# Função vai ficar sempre recebendo a msg e analisando, se msg = SAIR ou nao e mandar para e mandar para os outros usuarios.

def messagesTreatment(client_sockt, username, sala):
    while True:
        try:
            msg = client_sockt.recv(2048)
            if msg.decode('utf-8') == '/SAIR':
                sala['clients'].remove(client_sockt)
                sala['usernames'].remove(username)
                broadcast(f'{username} saiu da sala.\n'.encode('utf-8'),sala)
                client_sockt.close()
                break
            else:
                broadcast(msg, client_sockt, sala)
        except ConnectionResetError:
            sala['clients'].remove(client_sockt)
            sala['usernames'].remove(username)
            broadcast(f'{username} saiu da sala.\n'.encode('utf-8'), client_sockt, sala)

            client_sockt.close()
            break


def broadcast(msg, client_sockt, room):
    for clientItem in room['clients']:
        if clientItem != client_sockt and clientItem in room['clients']:
            try:
                clientItem.send(msg)
            except ConnectionResetError:
                deleteClient(clientItem, room)
          
def deleteClient(client_sockt, sala):
    sala['clients'].remove(client_sockt)


if __name__ == '__main__':
    main()
