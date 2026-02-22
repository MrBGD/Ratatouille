#!/usr/bin/env python3
import os
import socket
import sys
import threading

flag = os.environ['FLAG']

def handle_client(client_socket):
    """Handle a single client connection"""
    def send(msg, end='\n'):
        client_socket.sendall((msg + end).encode())
    
    def receive():
        return client_socket.recv(4096).decode().strip()
    
    try:
        send("=" * 80)
        send("MALWARE ANALYSIS QUIZ")
        send("=" * 80)
        send("\nAnswer the following questions about the malware analysis.\n")
        
        questions = [
            {
                "number": 1,
                "question": "The malware uses a specific prefix for its Registry keys and file paths to hide them from the user and system tools (Stealth Mode). What is this prefix?",
                "answer": "$nya"
            },
            {
                "number": 2,
                "question": 'This stealth technique is based on a well-known open-source Rootkit project. Provide the opensource link to the original malware is based on.',
                "answer": "https://github.com/bytecode77/r77-rootkit"
            },
            {
                "number": 3,
                "question": 'The malware drops a malicious binary that masquerades as a legitimate system driver to blend in. What is the filename and extension of this dropped file?  filename.extension',
                "answer": "ACPIx86.sys"
            },
            {
                "number": 4,
                "question": 'In which Registry Key path does the malware store the configuration for the files it is hiding?',
                "answer": "HKEY_LOCAL_MACHINE\SOFTWARE\$nya-config\paths"
            },
            {
                "number": 5,
                "question": "What is the specific family name of this malware?",
                "answer": "Onimai"
            }
        ]
        
        score = 0
        total = len(questions)
        
        for q in questions:
            send(f"\nQuestion {q['number']}:")
            send("-" * 80)
            send(q['question'])
            send("")
            send("Your answer: ", end='')
            
            user_answer = receive()
            
            if user_answer == q['answer']:
                send("✓ Correct!")
                score += 1
            else:
                send("✗ Incorrect")
                client_socket.close()
                return
        
        send("\n" + "=" * 80)
        send("QUIZ COMPLETE")
        send(f"Here is your flag: {flag}")
        send("=" * 80)
    
    except Exception as e:
        print(f"Error handling client: {e}", file=sys.stderr)
    finally:
        client_socket.close()

def main():
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 1337))
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[*] Server listening on {HOST}:{PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Connection from {client_address[0]}:{client_address[1]}")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            print(f"[-] Connection closed from {client_address[0]}:{client_address[1]}")
    
    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
    except Exception as e:
        print(f"[!] Server error: {e}", file=sys.stderr)
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
