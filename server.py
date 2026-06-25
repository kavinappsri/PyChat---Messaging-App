import network
import threading
import json
import jsonDB

#Dictionaries

CONFIG_DEFAULT = {
    "ip":"0.0.0.0",
    "port":8080,
    "stopWord":"stop",
    "registeredClients":{}
}

BAD_REQUEST_RESPONSE = {
    "status":"2",
    "Error":"Bad Request"
}

ACTION_DENIED_RESPONSE = {
    "status":"3",
    "Error": "Action Denied"
}

OK_RESPONSE = {
    "status":"1"
}

#FUNCTIONS

def _shutdownThread():
    """Internal function for handling shutdown"""
    while True:
        cmd = input()
        if cmd == configurations.data["stopWord"]:
            print("[SHUTDOWN THREAD] Commencing Shutdown Process")
            server.stop()
            break

#EXECUTION LINE

#Loading all objects

print("[INFO] Loading config")

configurations = jsonDB.jsonDB("serverconfig.json", CONFIG_DEFAULT)

print(f"[INFO] Starting server at {configurations.data['ip']}:{configurations.data['port']}")

server = network.socketServerManager(configurations.data['ip'], configurations.data['port'])
serverThread =  threading.Thread(target=server.start, daemon=True)
shutdownThread = threading.Thread(target=_shutdownThread, daemon=True)
serverThread.start()
shutdownThread.start()


#Main Loop
while True:
    packet = server.inputQueue.get()
    
    #Check for poison pill
    if packet is None:
        break
    
    #Check for JSON packet
    try:
        data = json.loads(packet[1])
    except:
        server.send(packet[0], json.dumps(BAD_REQUEST_RESPONSE))
        continue

    #Check for Action
    if "action" not in data:
        server.send(packet[0], json.dumps(BAD_REQUEST_RESPONSE))
        continue

    #Register Action
    if data["action"] == "register":
        if "username" not in data or "password" not in data:
            server.send(packet[0], json.dumps(BAD_REQUEST_RESPONSE))
            continue
        elif data["username"] in configurations.data["registeredClients"]:
            server.send(packet[0], json.dumps(ACTION_DENIED_RESPONSE))
            continue
        else:
            configurations.data["registeredClients"][data["username"]] = data["password"]
            configurations.save()
            server.send(packet[0], json.dumps(OK_RESPONSE))
            continue
            
    #Msg Action
    elif data["action"] == "msg":
        if "username" not in data or "password" not in data or "message" not in data:
            server.send(packet[0], json.dumps(BAD_REQUEST_RESPONSE))
            continue
        elif data["username"] not in  configurations.data["registeredClients"]:
            server.send(packet[0], json.dumps(ACTION_DENIED_RESPONSE))
            continue
        elif data["password"] != configurations.data["registeredClients"][data["username"]]:
            server.send(packet[0], json.dumps(ACTION_DENIED_RESPONSE))
            continue
        else:
            sendString = f'<{data["username"]}> {data["message"]}'
            sendable = {
                "status":"1",
                "ping":sendString
            }
            server.sendallQueue.put(json.dumps(sendable))
            
    #Invalid Action
    else:
        server.send(packet[0], json.dumps(BAD_REQUEST_RESPONSE))
        


