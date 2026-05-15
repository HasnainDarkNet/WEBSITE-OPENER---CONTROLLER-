#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import time

PORT = 5555

def open_website(url):
    """Open website on target"""
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        
        if os.name == 'nt':  # Windows
            os.system(f'start {url}')
        else:  # Linux/Mac/Termux
            try:
                subprocess.run(['xdg-open', url], capture_output=True)
            except:
                try:
                    subprocess.run(['termux-open-url', url], capture_output=True)
                except:
                    pass
        return f"[✓] Opened: {url}"
    except Exception as e:
        return f"[-] Error: {e}"

def handle_client(conn, addr):
    """Handle single client connection"""
    print(f"\n[+] Connected: {addr[0]}")
    
    try:
        while True:
            data = conn.recv(1024).decode()
            
            if not data or data.lower() == 'exit':
                break
            
            if data.lower().startswith('open '):
                url = data[5:].strip()
                result = open_website(url)
                conn.send(result.encode())
            
            elif data.lower() == 'help':
                help_text = """
╔══════════════════════════════════════════════════════════════╗
║  Commands:                                                   ║
║  open <url>  - Open website (e.g., open google.com)         ║
║  help        - Show this help                                ║
║  exit        - Disconnect                                    ║
╚══════════════════════════════════════════════════════════════╝
                """
                conn.send(help_text.encode())
            else:
                conn.send(b"[-] Type 'help' for commands")
    
    except:
        pass
    
    conn.close()
    print(f"[-] Disconnected: {addr[0]}")

def start_server():
    """Start server with auto-restart"""
    while True:
        try:
            # Create socket
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind and listen
            server.bind(('0.0.0.0', PORT))
            server.listen(5)
            
            print(f"""
╔══════════════════════════════════════════════════════════════╗
║         REMOTE WEBSITE OPENER - ACTIVE                        ║
║         Listening on port: {PORT}                               ║
║         Server will auto-restart if stopped                   ║
║                   [🐺] HasnainDarkNet [🐺]                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
            
            while True:
                try:
                    conn, addr = server.accept()
                    handle_client(conn, addr)
                except KeyboardInterrupt:
                    print("\n[!] Press Ctrl+C again to exit...")
                    time.sleep(2)
                except Exception as e:
                    print(f"[-] Client error: {e}")
                    continue
                    
        except KeyboardInterrupt:
            print("\n[!] Server shutting down...")
            sys.exit(0)
        except Exception as e:
            print(f"[-] Server error: {e}")
            print("[*] Restarting server in 5 seconds...")
            time.sleep(5)
            continue

if __name__ == "__main__":
    start_server()
