#!/usr/bin/env python3
import socket
import time
import os
import argparse
import threading
import datetime

class CallbackReceiver:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.sock = None
        self.connections = []
        self.running = False
        self.data_dir = "results"


        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def handle_client(self, client_socket, addr):
        print(f"[+] Connection from {addr[0]}:{addr[1]}")


        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.data_dir}/callback_{addr[0]}_{timestamp}.txt"


        client_socket.settimeout(30)
        data = b""
        try:
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            print(f"[!] Receive timeout from {addr[0]}:{addr[1]}")
        except Exception as e:
            print(f"[!] Error receiving data from {addr[0]}:{addr[1]}: {e}")


        try:
            if data:
                with open(filename, 'wb') as f:
                    f.write(data)
                print(f"[+] Saved {len(data)} bytes to {filename}")


                try:
                    print("\n--- BEGIN RECEIVED DATA ---")
                    print(data.decode('utf-8', errors='replace'))
                    print("--- END RECEIVED DATA ---\n")
                except Exception as e:
                    print(f"[!] Error decoding data: {e}")
            else:
                print(f"[!] No data received from {addr[0]}:{addr[1]}")
        except Exception as e:
            print(f"[!] Error saving data: {e}")


        client_socket.close()

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            self.running = True

            print(f"[*] Listener started on {self.host}:{self.port}")
            print(f"[*] Saving captured data to {os.path.abspath(self.data_dir)}")

            while self.running:
                try:
                    client, addr = self.sock.accept()
                    client_handler = threading.Thread(
                        target=self.handle_client,
                        args=(client, addr)
                    )
                    client_handler.daemon = True
                    client_handler.start()
                    self.connections.append(client_handler)
                except Exception as e:
                    if self.running:
                        print(f"[!] Error accepting connection: {e}")
                    break

        except Exception as e:
            print(f"[!] Error starting listener: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        print("[*] Listener stopped")

def main():
    parser = argparse.ArgumentParser(description="SSH integration callback receiver")
    parser.add_argument("--host", default="0.0.0.0", help="Host to listen on (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    args = parser.parse_args()

    print("SSH integration callback receiver")

    listener = CallbackReceiver(args.host, args.port)

    try:
        listener.start()
    except KeyboardInterrupt:
        print("\n[*] Keyboard interrupt detected. Shutting down...")
    finally:
        listener.stop()

if __name__ == "__main__":
    main()
