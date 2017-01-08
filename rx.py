import re
import sys
import MySQLdb
import SocketServer
import time
import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')
db = MySQLdb.connect(host="db1.cc1tyj8ewcwf.eu-west-1.rds.amazonaws.com",
                     user="python_rw",
                     passwd="python_backend_script_user",
                     db="events")
cur = db.cursor()
portnames= {'23': 'Telnet', '22': 'SSH', '80': 'HTTP', '443': 'HTTPS'}
regex = "firewall,info py: .* input: in:Node4-FTTC out:\(none\), src-mac.*, proto (TCP|UDP|ICMP) .* ([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\:(\d{1,5})-\>([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\:(\d{1,5}), len \d{1,4}"
HOST, PORT = "0.0.0.0", 514
class SyslogUDPHandler(SocketServer.BaseRequestHandler):
 def handle(self):
  data = bytes.decode(self.request[0].strip())
  vv = self.client_address[0]
  socket = self.request[1]
  matches = re.finditer(regex, str(data))
  for matchNum, match in enumerate(matches):
    sourceIP=match.group(2) + "."  + match.group(3) + "."  + match.group(4) + "."  + match.group(5)
    destIP=match.group(7) + "."  + match.group(8) + "."  + match.group(9) + "."  + match.group(10)
    proto=match.group(1)
    sourcePort=int(match.group(6))
    destPort=int(match.group(11))
    logTime=str(int(time.time()))
    geo=reader.city(sourceIP).country.name
    cur.execute("INSERT INTO firewall(timestamp,proto,sourceIP,destIP,sourcePort,destPort,geo) VALUES (NOW(),%s,%s,%s,%s,%s,%s);", (proto,sourceIP,destIP,sourcePort,destPort,geo))
    print ("Protocol: " + match.group(1))
    print ("Source IP: " + sourceIP)
    print ("Time: " + logTime)
    print ("Destination Port: " + portnames[match.group(11)])
    print ("Country" + geo)
    db.commit()
if __name__ == "__main__":
	try:
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")
        db.close()