import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8082",
http_proxy_host="127.0.0.1", http_proxy_port="8080", headers=Sec-WebSocket-Extensions)
content=json.dumps({'msg': 'connect', 'Taint-version': '1', 'x-taint-bin':'\\x3B\\x03'})
ws.send(content)
print(ws.recv())
ws.close()
