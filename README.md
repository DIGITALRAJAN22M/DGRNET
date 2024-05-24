# ABOUT THIS TOOL
DGRNET Is a Network Utility Tool which provide facilities like client and server its a replacement of netcat (not fully ) but some how. you can use this tool 
it is created by @Rajan Kumar Barik known as ANONDGR (me 😊)

# { INSTALLATION }
1.git clone https://github.com/DIGITALRAJAN22M/DGRNET.git

2. cd DGRNET
   
3. chmod +x dgrnet.py
   
4. ./dgrnet.py 


# preview


R:\DGRNET>python dgrnet.py
Could not find platform independent libraries <prefix>
################################################################################
#                                                                              #
#    █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██████╗  ██████╗ ██████╗ ██████╗      #
#   ██╔══██╗████╗  ██║██╔════╝ ████╗  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗     #
#   ███████║██╔██╗ ██║██║  ███╗██╔██╗ ██║██████╔╝██║   ██║██████╔╝██████╔╝     #
#   ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║██╔══██╗██║   ██║██╔═══╝ ██╔══██╗     #
#   ██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║██████╔╝╚██████╔╝██║     ██║  ██║     #
#   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝     #
#                                                                              #
################################################################################
#                                                                              #
#                           DGRNET Tool v1.0                                   #
#                   Created by @Rajan Kumar Barik (ANONDGR)                    #
#                                                         Prof:Ethical Hacker  #
#                                                                              #
################################################################################

Usage: ./dgrnet.py or python dgrnet.py -t target_host -p port
-l --listen                     - listen on [host]:[port] for incoming connections
-e --execute=file_to_run        - execute the given file upon receiving a connection
-c --command                    - initialize a command shell
-u --upload=destination         - upon receiving a connection upload a file and write to [destination]

Examples:
dgrnet.py -t 192.168.0.1 -p 8888 -l -c
dgrnet.py -t 192.168.0.1 -p 8888 -l -u=C:\\file.exe
echo 'ABCDEFGHI' | ./dgrnet.py -t 192.168.23.13 -p 445
################################################################################

R:\DGRNET>![preview jpg](https://github.com/DIGITALRAJAN22M/DGRNET/assets/96865310/fdaab568-f9d6-40c1-a135-8cf136bacbbe)





