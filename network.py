import socket
import threading
import queue
from concurrent.futures import ThreadPoolExecutor





#CLASSES

#Daemon Thread Class
class daemonExecutor(ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_factory = lambda *a, **kw: threading.Thread(*a, **kw, daemon=True)

#Server Class
class socketServerManager:
    def __init__(self, ip, port, maxBacklog = 5):
        #Save the ip and port
        self.ip = ip
        self.port = port
        self.maxBacklog = maxBacklog
        self.serverOnline = False
        self.connectionsDict = {}
        self.inputQueue = queue.Queue()
        self.sendallQueue = queue.Queue()
        self.encoding = 'utf-8'

        #Create the socket set the opts and bind the ip and port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.server.bind((self.ip, self.port))

    def start(self):
        try:
            self.serverOnline = True
            executor = daemonExecutor(max_workers=5)

            executor.submit(self.sendallThread)

            id = 0
            while self.serverOnline:
                id += 1
                self.server.listen(self.maxBacklog)
                connection, address = self.server.accept()
                self.connectionsDict[id] = connection
                print(f"[SERVER] New connection from {address}")
                
                executor.submit(self.clientThread, connection, id)
                

            connection.close()
            self.server.close()
            
        except Exception as e:
            if not self.serverOnline:
                print("[SERVER] Server stopped")
            print("[SERVER] Error: ", e)
            
        finally:
            self.server.close()

    def stop(self):
        self.serverOnline = False
            
    def clientThread(self, connection, id):
        try:
            while True:
                header = connection.recv(10)
                if header:
                    msgLength = int(header.decode("utf-8").strip())
                    payloadBytes = b""
                    
                    while len(payloadBytes) < msgLength:
                        msgChunk = connection.recv(msgLength - len(payloadBytes))
                        if not msgChunk:
                            break
                        payloadBytes += msgChunk
                        
                    data = payloadBytes.decode("utf-8")
                    print(f"[SERVER] Received: {data}")
                    self.inputQueue.put([id, data])
                    
                if not header:
                    break
                    
        except Exception as e:
            print(f"[SERVER] Error: {e}")

    def sendallThread(self):
        while True:
            data = self.sendallQueue.get()
            
            for connection in self.connectionsDict.values():
                encData = data.encode(self.encoding)
                encDataHeader = f"{len(encData):<10}".encode(self.encoding)

                connection.sendall(encDataHeader + encData)

    def send(self, id, data):
        encData = data.encode(self.encoding)
        encDataHeader = f"{len(encData):<10}".encode(self.encoding)
        self.connectionsDict[id].sendall(encDataHeader + encData)
                
            
        

class socketClientManager:
    def __init__(self, encoding):
        self.encoding = encoding
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def connect(self, ip, port):
        try:
            self.client.connect((ip, port))
        except Exception:
            raise
            

    def tryRecv(self): 
        try:
            header = self.client.recv(10)

            msgLength = int(header.decode("utf-8").strip())
            payloadBytes = b""

            while len(payloadBytes) < msgLength:
                msgChunk = self.client.recv(msgLength - len(payloadBytes))
                if not msgChunk:
                    break
                payloadBytes += msgChunk

            data = payloadBytes.decode("utf-8")
            
            return data
                
        except Exception as e:
             raise

    def send(self, data):
        encData = data.encode(self.encoding)
        encDataHeader = f"{len(encData):<10}".encode(self.encoding)
        
        self.client.sendall(encDataHeader + encData)

    def close(self):
        self.client.close()
            
        
        
        

        
        