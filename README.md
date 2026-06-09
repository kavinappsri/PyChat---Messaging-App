# PyChat

This is a lightweight messaging app built using python.

## Instructions to use

### Start a Server

1. Check for and open the file serverconfig.json (if there is none, run and close server.py once to generate it).

2. In the file, change the values for "ip" and "port" to your desired ip and port (Make sure you have access to your chosen ip and port). By default it willl be set to 0.0.0.0 and 8080.

3. Run server.py to start your server. Do Control+C twice to stop it.

### Use the Client

1. Run client.py

2. It is recommended that you change the "username" and "password" fields in config.json from their default values. Not doing so may result in problems while connecting to servers _Note: if you do, you must close and rerun client.py to load your changes/prevent the from being overwritten_.

3. To connect to a new server, you must register it first. To do this, press 1 and then enter on your keyboard, which will execute Action 1 from the actions menu. Enter the server IP and port when prompted.

4. To connect to a registered server, press 2 and then enter on your keyboard. When prompted, enter the server IP. To exit the server, type 'exit'.

5. To exit the program, type 3 and enter in the actions menu. This will, execute action 3, which will close the program

## Note

This program uses ANSI escape codes. Older terminals such as may fail to register these properly

## Technical

This program uses socket for networking. All the networking calls are in ```network.py```. ```jsonDB.py``` is used to read and write to json files used for storage (eg. config.json). ```userInt.py``` is used to provide the console user interface for the client

In the server, this program uses multi-threading to handle multiple clients, along with another thread to send messages to all the clients. Queues are used to exchange information b/w threads

The client also uses multi-threading to handle simultaneous input and output, from the user and the server. Both server and client use the json files to keep track of the registered servers/clients

JSON is typically transmitted through the TCP stream. The client will send a json object containing a 'action' parameters with the value being the requested action, along with parameters for the action. Not having an action or the required parameters will result in a bad request error being sent by the server. There server will send back a status number (1 - OK, 2 - Bad Request, 3 - Action Denied) along with some optional parameters like error (incase of codes 2 or 3) or ping (what message is sent)