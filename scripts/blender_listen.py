import bpy, socket, threading, traceback

HOST = '127.0.0.1'; PORT = 9876

def handle_client(conn):
    try:
        data = b''
        while True:
            chunk = conn.recv(4096)
            if not chunk: break
            data += chunk
        code = data.decode('utf-8')
        if code:
            try:
                exec(code)
                conn.sendall(b'{"status": "success", "result": {"executed": true}}')
            except Exception as e:
                tb = traceback.format_exc()
                conn.sendall(f'{{"status": "error", "result": "{e}"}}'.encode())
    except: pass
    finally: conn.close()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)); s.listen(5)
    bpy.app.timers.register(lambda: None, persistent=True)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

threading.Thread(target=server, daemon=True).start()
print(f"Blender TCP server listening on {HOST}:{PORT}")
