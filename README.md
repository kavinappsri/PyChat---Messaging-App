# PyChat

PyChat is a lightweight desktop chat application that pairs a PySide6 client with a threaded TCP server. It gives you a small, readable Python codebase for experimenting with socket networking, JSON message payloads, client registration, and real-time message broadcasting.

## Key Features

- **Desktop chat client**: Qt-based interface built with PySide6.
- **Threaded TCP server**: Handles multiple connected clients concurrently.
- **JSON protocol**: Sends structured requests and responses over persistent socket connections.
- **Client registration**: Stores usernames and passwords per server before allowing messages.
- **Broadcast messaging**: Relays accepted chat messages to all connected clients.
- **File-backed configuration**: Generates editable JSON config files for client and server settings.
- **Shared networking layer**: Keeps socket framing, send, receive, and shutdown behavior in `network.py`.

## Project Structure

```text
PyChat/
├── client/
│   ├── main.py                 # Desktop client entry point
│   ├── application.py          # Wires the GUI to the client networking layer
│   ├── client.py               # Client connection, registration, and messaging logic
│   ├── config/defaults.py      # Default client configuration
│   └── gui/                    # PySide6 windows, pages, widgets, and styles
├── server/
│   ├── main.py                 # Server entry point
│   ├── server.py               # Server lifecycle and request handling
│   ├── const.py                # Default server configuration and response constants
│   └── userInt.py              # Console input/output helper for server commands
├── network.py                  # Shared socket client/server managers
├── jsonDB.py                   # JSON file persistence helper
├── pyproject.toml              # Python and dependency metadata
└── poetry.lock                 # Locked dependency versions
```

## Prerequisites

- Python `>=3.14,<3.15`
- Poetry 2.x or newer
- A network interface and port you can bind for the server

PyChat currently depends on:

```toml
pyside6 = ">=6.11.1,<7.0.0"
```

## Installation

Clone the repository and install the locked dependencies with Poetry:

```bash
git clone https://github.com/kavinappsri/PyChat---Messaging-App.git
cd PyChat
poetry install
```

If you prefer to use an existing virtual environment, install the project dependency directly:

```bash
python3.14 -m pip install "pyside6>=6.11.1,<7.0.0"
```

## Configuration

PyChat creates JSON configuration files automatically the first time each entry point runs.

### Server Configuration

Run the server once to generate `server/serverconfig.json`:

```bash
poetry run python -m server.main
```

Stop it by typing the configured stop word, which is `stop` by default. Then edit the generated file as needed:

```json
{
  "ip": "0.0.0.0",
  "port": 8080,
  "stopWord": "stop",
  "serverName": "Server1234",
  "registeredClients": {}
}
```

### Client Configuration

Run the client once to generate `client/config.json`:

```bash
poetry run python -m client.main
```

Close the app, then edit the generated username and password before connecting to a shared server:

```json
{
  "encoding": "utf-8",
  "username": "Guest",
  "password": "hello_world",
  "servers": {}
}
```

Using unique credentials per user is recommended because the server registers usernames and rejects duplicate or mismatched credentials.

## Basic Usage

Start the server in one terminal:

```bash
poetry run python -m server.main
```

Start one or more clients in separate terminals:

```bash
poetry run python -m client.main
```

In the client window:

1. Enter the server IP address.
2. Enter the server port, such as `8080`.
3. Select **Connect To Server**.
4. Type a message and select **Send**.
5. Select **Disconnect** to leave the server.

To stop the server, type the configured stop word in the server terminal:

```text
stop
```

## Message Protocol

PyChat frames each socket message with a 10-byte length header followed by a JSON payload. Clients send an `action` field to request server behavior.

Example registration payload:

```json
{
  "action": "register",
  "username": "Guest",
  "password": "hello_world"
}
```

Example chat payload:

```json
{
  "action": "msg",
  "username": "Guest",
  "password": "hello_world",
  "message": "Hello from PyChat!"
}
```

Server responses include a `status` field:

| Status | Meaning |
| --- | --- |
| `1` | OK |
| `2` | Bad request |
| `3` | Action denied |

## Development Notes

- `network.py` owns socket setup, message framing, broadcast queues, and shutdown behavior.
- `server/server.py` validates requests, persists registered clients, and broadcasts accepted messages.
- `client/client.py` manages async connection setup, server registration, message sending, and receive-loop signals.
- `client/gui/` contains the PySide6 interface pages and reusable widgets.

