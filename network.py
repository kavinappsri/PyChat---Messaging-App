import socket
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

#Networking API, for both server and client
#CLASSES

class socketClientManager:
    """Provides a simple socket client API"""
    def __init__(self, encoding):
        self.encoding = encoding
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    
    def connect(self, ip, port):
        """Connects to a server at the given ip and port"""
        try:
            self.client.connect((ip, port))
        except Exception:
            raise
            
    
    def tryRecv(self): 
        """Tries to recieve a message from the server, returns None if no message is recieved"""
        try:
            header = self.client.recv(10)
            
            if not header:
                return None

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
        """Sends a message to the server"""
        encData = data.encode(self.encoding)
        encDataHeader = f"{len(encData):<10}".encode(self.encoding)
        
        self.client.sendall(encDataHeader + encData)

    def close(self):
        """Closes the client connection"""
        try:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        except OSError:
           pass 


#Server Class
class socketServerManager:
    """Provides a simple socket server API"""
    def __init__(self, ip, port, maxBacklog = 5):
        #Initialize all the properties
        self.ip = ip
        self.port = port
        self.maxBacklog = maxBacklog
        self.serverOnline = False
        self.connectionsDict = {}
        self.inputQueue = queue.Queue()
        self.sendallQueue = queue.Queue()
        self.shutdownEvent = threading.Event()
        self.clientLock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.encoding = 'utf-8'

        #Create the socket, set the opts and bind the ip and port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.server.bind((self.ip, self.port))


    def start(self):
        """Starts the server"""
        try:
            self.serverOnline = True

            self.executor.submit(self._sendallThread)

            id = 0
            while self.serverOnline:
                id += 1
                self.server.listen(self.maxBacklog)
                connection, address = self.server.accept()
                with self.clientLock:
                    self.connectionsDict[id] = connection

                self.executor.submit(self._clientThread, connection, id)

        except Exception as e:
            if not self.serverOnline:
                print("[NETWORK] Server stopping exception occured")
            print("[NETWORK] Error: ", e)

        finally:
            self.server.close()

    def stop(self):
        """Stops the server"""
        #Setting variables
        self.serverOnline = False
        self.shutdownEvent.set()
        
        #Reloading accept loop
        reloader_ip = "127.0.0.1" if self.ip == "0.0.0.0" else self.ip
        try:
            serverReloader = socketClientManager(self.encoding)
            serverReloader.connect(reloader_ip, self.port)
            serverReloader.close()
        except Exception as e:
            print(f'[NETWORK-STOP] Error {e}')
        
        #Closing Client Threads
        with self.clientLock:
            for connection in self.connectionsDict.values():
                try:
                    connection.shutdown(socket.SHUT_RDWR)
                    connection.close()
                except Exception as e:
                    print(f'[NETWORK-STOP] Error {e}')
        
        #Sending Poison Pills
        self.sendallQueue.put(None)
        self.inputQueue.put(None)
        
        #Stopping Executor
        self.executor.shutdown(wait=False)
        
        

    # Client Handling Function
    def _clientThread(self, connection, id):
        """Internal function for handling client connections"""
        try:
            while not self.shutdownEvent.is_set():
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
                    self.inputQueue.put([id, data])

                if not header:
                    break

        except Exception as e:
            if not self.shutdownEvent.is_set():
                print(f"[NETWORK-CLIENT {id}] Error: {e}")
                
        finally:
            with self.clientLock:
                if id in self.connectionsDict:
                    del self.connectionsDict[id]
            try:
                connection.close()
            except OSError:
                pass

    def _sendallThread(self):
        """Internal function for sending messages to all clients"""
        while not self.shutdownEvent.is_set():
            data = self.sendallQueue.get()
            
            if data is None:
                break
                
            with self.clientLock:
                connectionSnapshot = list(self.connectionsDict.values())


            for connection in connectionSnapshot:
                try:
                    encData = data.encode(self.encoding)
                    encDataHeader = f"{len(encData):<10}".encode(self.encoding)
                    
                    connection.sendall(encDataHeader + encData)
                except OSError:
                    pass


    def send(self, id, data):
        """Sends a message to a specific client"""
        encData = data.encode(self.encoding)
        encDataHeader = f"{len(encData):<10}".encode(self.encoding)
        with self.clientLock:
            connection = self.connectionsDict[id]
            
        try:
            connection.sendall(encDataHeader + encData)
        except OSError as e:
            print(f"[NETWORK] Error: {e}")
            
                

            
        