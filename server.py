import network
import threading
import json
import jsonDB
import queue

#Dictionaries

configDefault = {
    "ip":"0.0.0.0",
    "port":8080,
    "registeredClients":{}
}

badRequestResponse = {
    "status":"2",
    "Error":"Bad Request"
}

actionDeniedResponse = {
    "status":"3",
    "Error": "Action Denied"
}

okResponse = {
    "status":"1"
}

#EXECUTION LINE

print("[INFO] Loading config")

configurations = jsonDB.jsonDB("serverconfig.json", configDefault)

print(f"[INFO] Starting server at {configurations.data['ip']}:{configurations.data['port']}")

server = network.socketServerManager(configurations.data['ip'], configurations.data['port'])
serverThread =  threading.Thread(target=server.start, daemon=True)
serverThread.start()



while True:
    packet = server.inputQueue.get()
    try:
        data = json.loads(packet[1])
    except:
        server.send(packet[0], json.dumps(badRequestResponse))
        continue

    if "action" not in data:
        server.send(packet[0], json.dumps(badRequestResponse))
        continue

    if data["action"] == "register":
        if "username" not in data or "password" not in data:
            server.send(packet[0], json.dumps(badRequestResponse))
            continue
        elif data["username"] in configurations.data["registeredClients"]:
            server.send(packet[0], json.dumps(actionDeniedResponse))
            continue
        else:
            configurations.data["registeredClients"][data["username"]] = data["password"]
            configurations.save()
            server.send(packet[0], json.dumps(okResponse))
            continue
    elif data["action"] == "msg":
        if "username" not in data or "password" not in data or "message" not in data:
            server.send(packet[0], json.dumps(badRequestResponse))
            continue
        elif data["username"] not in  configurations.data["registeredClients"]:
            server.send(packet[0], json.dumps(actionDeniedResponse))
            continue
        elif data["password"] != configurations.data["registeredClients"][data["username"]]:
            server.send(packet[0], json.dumps(actionDeniedResponse))
            continue
        else:
            sendString = f'<{data["username"]}> {data["message"]}'
            sendable = {
                "status":"1",
                "ping":sendString
            }
            server.sendallQueue.put(json.dumps(sendable))
    else:
        server.send(packet[0], json.dumps(badRequestResponse))
        


