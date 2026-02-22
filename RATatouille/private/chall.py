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
                "question": "The malware verifies if it was launched with a specific secret argument. If the argument is missing, it relaunches itself using that key to hide its execution. What is the value of this argument?",
                "answer": "HCPrMNUTufgxpxMSH"
            },
            {
                "number": 2,
                "question": 'To evade analysis, the malware checks for specific hardware to ensure it is running on a real victim\'s machine. What Disk Model and Drive Letter does it check for?\nFormat: "<disk_model>, <drive_letter>:"',
                "answer": "WDS100T2B0A, F:"
            },
            {
                "number": 3,
                "question": 'Provide the list of strings the malware searches for to detect if it is running inside a Virtual Machine.\nFormat: "<string1> <string2>"',
                "answer": "QEMU DADY VirtualBox BOCHS_ BXPC___"
            },
            {
                "number": 4,
                "question": 'The loader uses AES encryption to unpack the payload. Provide the Key, the IV (in Base64), and the Cipher Mode used.\nFormat: "<key> <IV> <mode>"',
                "answer": "XPtZOUHY5OeenWFPBw1yCsPCGanSXRbZFoEprI16QF8= FRxUQwvJ84LwrFZMYH8pPg== CBC"
            },
            {
                "number": 5,
                "question": "The malware achieves persistence or stores its configuration in the Windows Registry. What is the Registry path used?",
                "answer": "HKLM:\\SOFTWARE\\OOhhhm="
            },
            {
                "number": 6,
                "question": "In the deobfuscated PowerShell script, what is the original name of the function responsible for loading the final .NET payload into memory?",
                "answer": "Acwq"
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

            if q["number"] == 3:
                user_answer = user_answer.split(" ")
                correct_answers = q["answer"].split(" ")
                if (len(user_answer) == len(set(user_answer))) and (len(set(user_answer)) == len(correct_answers)):
                    for answer in user_answer:
                        if answer not in correct_answers:
                            send("✗ Incorrect")
                            client_socket.close()
                            return
                    send("✓ Correct!")
                    score += 1
                else:
                    send("✗ Incorrect")
                    client_socket.close()
                    return
            else:
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
        server_socket.listen()
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
