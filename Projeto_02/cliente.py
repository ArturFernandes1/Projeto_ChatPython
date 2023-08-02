import threading
import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12400))

    username = input('Usuário> ')

    client.send(username.encode())
    mensagem = client.recv(2048).decode('utf-8')

    while mensagem.startswith("Nome de usuário já em uso."):
        print('Nome já está em uso, tente outro.')
        username = input('Digite outro nome>')
        client.send(username.encode())
        mensagem = client.recv(2048).decode('utf-8')

    print('Escolha uma sala:')
    print(' Sala 1')
    print(' Sala 2')
    print(' Sala 3')

    sala = input('Digite o nome da sala> ')

    while sala not in ('Sala 1', 'Sala 2', 'Sala 3'):
        print('Sala inválida.')
        sala = input('Digite o nome da sala> ')

    sala = str(sala)

    client.send(str(sala).encode())

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])
   
    thread1.start()
    thread2.start()

 
def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except Exception as e:
            print(f'\nNão foi possível permanecer conectado ao servidor: {e}\n')
            print('Pressione (Enter) para continuar.')
            client.close()
            break

def sendMessages(client, username):
    while True:
        try:
            msg = input('')
            client.send(f'<{username}> {msg}'.encode('utf-8'))    

            if msg == '/SAIR':
                client.close()
                break
        except Exception as e:
            print(f'Erro ao enviar mensagem: {e}')

main() 
