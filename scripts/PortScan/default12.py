# WORKS! Very slow...
from datetime import datetime
import errno
import sys
import socket

remote_server = 'markgacoka.com'
remote_server_ip = socket.gethostbyname(remote_server)

startPort = 1
endPort = 100
time_init = datetime.now()

try:
  for port in range(int(startPort), int(endPort)):
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