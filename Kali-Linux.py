#!/usr/bin/env python3
import socket
import os
import time

# Hacker Style Colors
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'

def loading():
    print(f"{GREEN}[*] Initializing Secure Connection", end="")
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print(RESET)

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""{RED}

██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗ 
██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝

{CYAN}╔══════════════════════════════════════════════════════════════╗
║             REMOTE WEBSITE OPENER - CONTROLLER              ║
║                       [⚡] Controller [⚡]                   ║
╚══════════════════════════════════════════════════════════════╝
{RESET}
""")

def main():
    banner()
    loading()

    target_ip = input(f"{YELLOW}[?] Enter Target IP ➤ {WHITE}")
    target_port = 5555

    try:
        print(f"\n{GREEN}[*] Connecting to target {target_ip}:{target_port}...{RESET}")

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))

        print(f"{GREEN}[+] Connection Established Successfully!{RESET}")
        print(f"{CYAN}[+] Type 'help' for commands")
        print(f"[+] Type 'exit' to disconnect{RESET}\n")

        while True:
            cmd = input(f"{MAGENTA}root@Controller ➤ {WHITE}")

            if not cmd:
                continue

            client.send(cmd.encode())

            if cmd.lower() == 'exit':
                print(f"{RED}\n[-] Disconnecting Session...{RESET}")
                break

            result = client.recv(4096).decode()
            print(f"{GREEN}{result}{RESET}")

        client.close()
        print(f"{RED}[!] Session Closed.{RESET}")

    except Exception as e:
        print(f"{RED}[-] Connection failed: {e}{RESET}")

if __name__ == "__main__":
    main()
