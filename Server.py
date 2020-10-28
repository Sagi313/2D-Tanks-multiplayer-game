import socket 
from _thread import *
import sys

server="10.0.0.3"
port=5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Server started, wating for connection")

def threaded_client(conn): # This Funcs runs as long as the client is connected. using threading, it runs on the background
    conn.send(str.encode("Connected"))
    reply= ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            else:
                print("Recived: ",reply)
                print("Sending: ",reply)

                conn.sendall(str.encode(reply))
        except:
            break

    print("Lost Connection")
    conn.close()

while True:
    conn,addr=s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client,(conn,))

#header = 64
#port = 5050
#server = "93.172.114.8"
#addr = (server, port)
#format = 'utf-8'
#disconnect_message = "!disconnect"

#server = socket.socket(socket.af_inet, socket.sock_stream)
#server.bind(addr)

#def handle_client(conn, addr):
#    print(f"[new connection] {addr} connected.")

#    connected = true
#    while connected:
#        msg_length = conn.recv(header).decode(format)
#        if msg_length:
#            msg_length = int(msg_length)
#            msg = conn.recv(msg_length).decode(format)
#            if msg == disconnect_message:
#                connected = false

#            print(f"[{addr}] {msg}")
#            conn.send("msg received".encode(format))

#    conn.close()
        
#def start():
#    server.listen()
#    print(f"[listening] server is listening on {server}")
#    while true:
#        conn, addr = server.accept()
#        thread = threading.thread(target=handle_client, args=(conn, addr))
#        thread.start()
#        print(f"[active connections] {threading.activecount() - 1}")

#print("[starting] server is starting...")
#start()