import socket, subprocess

proc = subprocess.Popen(["powershell.exe", '(Invoke-WebRequest -uri "http://ifconfig.me/ip").Content'], stdout=subprocess.PIPE)
print("Hostname: " + socket.gethostname() + " IP: " + proc.stdout.read().decode('utf-8').strip())
