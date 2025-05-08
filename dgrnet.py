#!/usr/bin/env python3

import sys
import socket
import getopt
import threading
import subprocess

# DEFINE SOME GLOBAL VARIABLES

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# MAIN FUNCTION RESPONSIBLE FOR HANDLING COMMAND LINE ARGUMENTS AND CALLING THE REST OF THE FUNCTIONS

def usage():
     ###    ##    ##  #######  ##    ## ########   ######   ########  
     ## ##   ###   ## ##     ## ###   ## ##     ## ##    ##  ##     ## 
    ##   ##  ####  ## ##     ## ####  ## ##     ## ##        ##     ## 
   ##     ## ## ## ## ##     ## ## ## ## ##     ## ##   #### ########  
   ######### ##  #### ##     ## ##  #### ##     ## ##    ##  ##   ##   
   ##     ## ##   ### ##     ## ##   ### ##     ## ##    ##  ##    ##  
   ##     ## ##    ##  #######  ##    ## ########   ######   ##     ## 
    print("################################################################################")
    print("#                                                                              #")
    print("#                           DGRNET Tool v1.0                                   #")
    print("#                   Created by @Rajan Kumar Barik (ANONDGR)                    #")
    print("#                                                         Prof:Ethical Hacker  #")
    print("#                                                                              #")
    print("################################################################################")
    print("\nUsage: ./dgrnet.py or python dgrnet.py -t target_host -p port")
    print("-l --listen                     - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run        - execute the given file upon receiving a connection")
    print("-c --command                    - initialize a command shell")
    print("-u --upload=destination         - upon receiving a connection upload a file and write to [destination]\n")
    print("Examples: ")
    print("dgrnet.py -t 192.168.0.1 -p 8888 -l -c")
    print("dgrnet.py -t 192.168.0.1 -p 8888 -l -u=C:\\\\file.exe")
    print("echo 'ABCDEFGHI' | ./dgrnet.py -t 192.168.23.13 -p 445")
    print("################################################################################")
    sys.exit(0)
def main():
    global listen, port, execute, command, upload_destination, target
    
    if not len(sys.argv[1:]):
        usage()
        
    # READ THE COMMAND LINE OPTIONS
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute=", "target=", "port=", "command", "upload="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-h', "--help"):
            usage()
        elif o in ('-l', "--listen"):
            listen = True
        elif o in ('-e', "--execute"):
            execute = a 
        elif o in ('-c', "--command"):
            command = True
        elif o in ('-u', "--upload"):
            upload_destination = a
        elif o in ('-t', "--target"):
            target = a
        elif o in ('-p', "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
        
    # ARE WE GOING TO LISTEN OR JUST SEND DATA FROM stdin? 
    if not listen and len(target) and port > 0:
        # read in the buffer from the commandline 
        # this will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()
        # send data off
        client_sender(buffer)
    # we are going to listen and potentially
    # upload things, execute commands, and drop a shell back
    # depending on our command line options above
    if listen:
        server_loop()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect to our target host
        client.connect((target, port))
        
        if len(buffer):
            client.send(buffer.encode())
        while True:
            # now wait for data back
            recv_len = 1
            response = ""   
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode()
                
                if recv_len < 4096:
                    break
            print(response, end='')
            
            # wait for more input
            buffer = input("")
            buffer += "\n"
            
            # send it off 
            client.send(buffer.encode())
    except Exception as e:
        print(f"[*] Exception! Exiting. {e}")
        # tear down the connection
        client.close()
        
def server_loop():
    global target
    
    # if no target is defined , we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    print(f"[*] Listening on {target}:{port}")
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # trim the newline
    command = command.rstrip()
    
    # run the command and get the output back 
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = str.encode(f"Failed to execute command. {e}\r\n")
    
    # send the output back to the client
    return output

def client_handler(client_socket):
    global upload, execute, command
    
    # check for upload
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = b""
        
        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
        # now we take these bytes and try to write them out
        try:
            with open(upload_destination, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)
            # acknowledge that we wrote the file out
            client_socket.send(f"Successfully saved file to {upload_destination}\r\n".encode())
        except Exception as e:
            client_socket.send(f"Failed to save file to {upload_destination}. {e}\r\n".encode())
        
    # check for command execution
    if len(execute):
        # run the command
        output = run_command(execute)
        client_socket.send(output)
    
    # now we go into another loop if a command shell was requested 
    if command:
        while True:
            try:
                # show a simple prompt
                client_socket.send("DGR:#> ".encode())
                
                # now we receive until we see a linefeed (enter key)
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024).decode()
                
                # send back the command output
                response = run_command(cmd_buffer)
                client_socket.send(response)
            except Exception as e:
                print(f"[*] Exception in command shell. {e}")
                break

if __name__ == "__main__":
    main()
