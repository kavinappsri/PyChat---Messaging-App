import network
import jsonDB
import json
import userInt
import threading 
import sys

#Dictionaries
CONFIG_DEFAULT = {
    "encoding":"utf-8",
    "username":"Guest",
    "password":"PyChat",
    "servers": {}
}

STRINGS = {
    "header":"==============\n    PyChat    \n==============",
    "configDefaultWarning":"\n[WARNING] Default username and pasword are being used, please change them in 'config.json'",
    "startMenu":"\nAvailable Actions:\n1. Register Server\n2. Connect to Server\n3. Exit",
    "invalidAction":"\n[ERROR] Invalid action, please try again",
    "actionCompleted":"\n[INFO] Action completed. Press enter to continue",
    "unregisteredServer":"\n[ERROR] Server is not registered, please register it first."
    
}

#Action Functions

def registerServer():
    """Adds Server to config"""
    
    terminal.clear()
    
    terminal.print("Enter Server IP")
    ip = terminal.getInput()

    terminal.print("Enter Server Port")
    port = int(terminal.getInput())
    
    configurations.data["servers"][ip] = {
        "ip":ip,
        "port":port,
        "registered":False
    }
    configurations.save()


def connectServer():
    """Handles the entire process of connecting to the server"""
    
    terminal.clear()

    terminal.print("Enter Server IP")
    ip = terminal.getInput()
    
    #Unregistered Server Check
    if ip in configurations.data["servers"]:
        port = configurations.data["servers"][ip]["port"]
    else:
        terminal.print(STRINGS["unregisteredServer"])
        return

    #Instantiate a connection
    client = network.socketClientManager(configurations.data["encoding"])
    try:
        client.connect(ip, port)
    except Exception as e:
        terminal.print(f"[ERROR] {e}")
        return
    
    # Registers itself in the server, if not done so before
    if configurations.data["servers"][ip]["registered"] == False:
        data = {
            "action":"register",
            "username":configurations.data["username"],
            "password":configurations.data["password"]
        }
        client.send(json.dumps(data))

        try:
            response = json.loads(client.tryRecv())
            
            if response is None:
                raise Exception("Server Disconnected")
            
            if "status" not in response:
                raise Exception("Invalid server response")
            
            elif response["status"] != "1":
                
                #Checking for already registered server
                if response["status"] == "3":
                    data = {
                        "action":"msg",
                        "username":configurations.data["username"],
                        "password":configurations.data["password"],
                        "message":""
                    }
                    client.send(json.dumps(data))
                    response = json.loads(client.tryRecv())
                    if "status" not in response:
                        raise Exception("Invalid server response")
                    elif response["status"] != "1":
                        raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
                    configurations.data["servers"][ip]["registered"] = True
                    configurations.save()
                else:
                    raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
                
            else:
                configurations.data["servers"][ip]["registered"] = True
                configurations.save()
                
        except Exception as e:
            terminal.print(f"[ERROR] {e}")
            return
    
    def _recvThread(shutdownEvent):
        """Internal function for receiving messages from the server"""
        while not shutdownEvent.is_set():
            try:
                raw_data = client.tryRecv()
                if raw_data is None:
                    raise Exception("Server Disconnected. Type 'exit' to leave")

                data = json.loads(raw_data)
                if "status" not in data:
                    raise Exception("Invalid server response")
                elif data["status"] != "1":
                    raise Exception(f"Server responded with status {data['status']}, error: {data['Error']}")
                else:
                    if "ping" in data:
                        terminal.print(data["ping"])

            except Exception as e:
                if not shutdownEvent.is_set():
                    terminal.print(f"[ERROR] {e}")
                    break
                
    #Setting the Stop Signal and starting the thread
    stopEvent = threading.Event()

    recvThread = threading.Thread(target=_recvThread, daemon=True, args=(stopEvent,))
    recvThread.start()

    #Main Sending Loop, to be running on main thread
    while True:
        message = terminal.getInput()
        if message == "exit":
            stopEvent.set()
            
            client.close()
            break
        if not message.strip():
            continue
        payload = {
            "action":"msg",
            "username":configurations.data["username"],
            "password":configurations.data["password"],
            "message":message
        }
        try:
            client.send(json.dumps(payload))
        except Exception as e:
            terminal.print(f'[ERROR] {e}')
                    
                    
    
        
        

#EXECUTION LINE

#Get the config and User Interface 
configurations = jsonDB.jsonDB("config.json", CONFIG_DEFAULT)
terminal = userInt.userInt("Action > ")

#Main Loop
while True:
    #Printing Information and Getting input
    terminal.clear()

    terminal.print(STRINGS["header"])

    if configurations.data["username"] == CONFIG_DEFAULT["username"] or configurations.data["password"] == CONFIG_DEFAULT["password"]:
        terminal.print(STRINGS["configDefaultWarning"])

    terminal.print(STRINGS["startMenu"])
    action = terminal.getInput()
    
    #Processing and Executing Input    
    try:
        action = int(action)
    except:
        terminal.print(STRINGS["invalidAction"])
        terminal.getInput()
        continue
            
    if action == 1:
        registerServer()
        terminal.print(STRINGS["actionCompleted"])
        terminal.getInput()
    elif action == 2:
        connectServer()
        terminal.print(STRINGS["actionCompleted"])
        terminal.getInput()
    elif action == 3:
        terminal.clear()
        terminal.print(":)")
        sys.exit()
    else:
        terminal.print(STRINGS["invalidAction"])
        terminal.getInput()
    
        











