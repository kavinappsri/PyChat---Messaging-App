import network
import jsonDB
import json
import userInt
import threading 
import sys

#Dictionaries
configDefault = {
    "encoding":"utf-8",
    "username":"Guest",
    "password":"PyChat",
    "servers": {}
}

strings = {
    "header":"==============\n    PyChat    \n==============",
    "configDefaultWarning":"\n[WARNING] Default username and pasword are being used, please change them in 'config.json'",
    "startMenu":"\nAvailable Actions:\n1. Register Server\n2. Connect to Server\n3. Exit",
    "invalidAction":"\n[ERROR] Invalid action, please try again",
    "actionCompleted":"\n[INFO] Action completed. Press enter to continue",
    "unregisteredServer":"\n[ERROR] Server is not registered, please register it first."
    
}

#Action Functions

def registerServer():
    #Adds Server to config
    
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
    #Handles the entire process of connecting to the server
    
    terminal.clear()

    terminal.print("Enter Server IP")
    ip = terminal.getInput()

    port = 0
    
    #Unregistered Server Check
    if ip in configurations.data["servers"]:
        port = configurations.data["servers"][ip]["port"]
    else:
        terminal.print(strings["unregisteredServer"])
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
            
            if "status" not in response:
                raise Exception("Invalid server response")
            elif response["status"] != "1":
                raise Exception(f"Server responded with status {response['status']}, error: {response['Error']}")
            else:
                configurations.data["servers"][ip]["registered"] = True
                configurations.save()
                
        except Exception as e:
            terminal.print(f"[ERROR] {e}")
            return
    
    #Function for receiving Thread
    def _recvThread(shutdownEvent):
        while not shutdownEvent.is_set():
            try:
                data = json.loads(client.tryRecv())
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
        client.send(json.dumps(payload))
                    
                    
    
        
        

#EXECUTION LINE

#Get the config and User Interface 
configurations = jsonDB.jsonDB("config.json", configDefault)
terminal = userInt.userInt("Action > ")

#Main Loop
while True:
    #Printing Information and Getting input
    terminal.clear()

    terminal.print(strings["header"])

    if configurations.data["username"] == configDefault["username"] or configurations.data["password"] == configDefault["password"]:
        terminal.print(strings["configDefaultWarning"])

    terminal.print(strings["startMenu"])
    action = terminal.getInput()
    
    #Processing and Executing Input    
    try:
        action = int(action)
    except:
        terminal.print(strings["invalidAction"])
        terminal.getInput()
        continue
            
    if action == 1:
        registerServer()
        terminal.print(strings["actionCompleted"])
        terminal.getInput()
    elif action == 2:
        connectServer()
        terminal.print(strings["actionCompleted"])
        terminal.getInput()
    elif action == 3:
        terminal.clear()
        terminal.print(":)")
        sys.exit()
    else:
        terminal.print(strings["invalidAction"])
        terminal.getInput()
    
        











