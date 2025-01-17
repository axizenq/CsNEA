# import socket 
# import threading
# import json

# client = socket.socket()
# client.connect(('4.tcp.eu.ngrok.io', 19645))

# game_state = {"players": {}}
# player_id = None

# def listen_to_server():
#     global game_state, player_id
#     buffer = ""
#     while True:
#         try:
#             data = client.recv(1024).decode()
#             if data:
#                 buffer += data
#                 while "\n" in buffer:
#                     message, buffer = buffer.split("\n", 1)
#                     try:
#                         parsed_message = json.loads(message)
#                         if parsed_message.get("type") == "id":
#                             player_id = parsed_message["player_id"]
#                             print(f"Assigned player ID: {player_id}")
#                         else:
#                             game_state = parsed_message
#                     except json.JSONDecodeError:
#                         print(f"Error decoding JSON: {message}")
#         except Exception as e:
#             print(f"Error receiving data: {e}")
#             break

# def send_action(action):
#     try:
#         client.send((json.dumps(action) + "\n").encode())
#     except Exception as e:
#         print(f"Error sending action: {e}")

# threading.Thread(target=listen_to_server, daemon=True).start()
