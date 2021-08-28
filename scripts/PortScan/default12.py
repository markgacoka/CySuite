# WORKS! Very slow af... but shows reason
from datetime import datetime
import errno
import sys
import socket

remote_server = 'markgacoka.com'
remote_server_ip = socket.gethostbyname(remote_server)

port_range = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080]# top 20
time_init = datetime.now()

try:
  for port in port_range:
      print("Checking port {} ...".format(port))
      server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_sock.settimeout(5)
      result = server_sock.connect_ex((remote_server_ip, port))
      if result == 0:
          print("Port {}: Open".format(port))
      else:
          print("Port {}: Closed".format(port))
          print("Reason:", errno.errorcode[result])
      server_sock.close()
except socket.error:
  print("Couldn't connect to server")
  sys.exit()

time_finish = datetime.now()
total_time = time_finish - time_init
print('Time to complete Port Scan: ', total_time)