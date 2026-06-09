import socket, json, time, sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    code = f.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(60)
s.connect(('127.0.0.1', 9876))
time.sleep(0.2)

payload = json.dumps({"type": "execute_code", "params": {"code": code}})
s.sendall(payload.encode() + b'\n')

time.sleep(3)
s.settimeout(5)
data = b''
while True:
    try:
        c = s.recv(65536)
        if not c: break
        data += c
    except: break
s.close()

sys.stdout.write(data.decode()[:2000])
sys.stdout.flush()
