import re
import sys
import socketserver
import time
import sqlite3 as sql
import geoip2.database
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
con = None
con = sql.connect('fwlog.db')
cur = con.cursor()
if len(sys.argv)>1:
    if (str(sys.argv[1]) == '--setup'):
        print("Setting up tables...")
        cur.execute("CREATE TABLE firewall(Id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, protocol TEXT, sourceIP TEXT, destPort TEXT, geo TEXT)")
portnames= {'23': 'Telnet', '22': 'SSH', '80': 'HTTP', '443': 'HTTPS'}
regex = "firewall,info py: .* input: in:Node4-FTTC out:\(none\), src-mac.*, proto (TCP|UDP|ICMP) .* ([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\:(\d{1,5})-\>([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\:(\d{1,5}), len \d{1,4}"
HOST, PORT = "0.0.0.0", 514
class SyslogUDPHandler(socketserver.BaseRequestHandler):
 def handle(self):
  data = bytes.decode(self.request[0].strip())
  vv = self.client_address[0]
  socket = self.request[1]
  matches = re.finditer(regex, str(data))
  for matchNum, match in enumerate(matches):
    sourceIP=match.group(2) + "."  + match.group(3) + "."  + match.group(4) + "."  + match.group(5)
    proto=match.group(1)
    port=match.group(11)
    logTime=str(int(time.time()))
#    geo=pycountry.countries.get(alpha_2=geolite2.lookup(sourceIP).country).name
    geo=reader.city(sourceIP).country.name
    with con:
        cur.execute("INSERT INTO firewall(timestamp,protocol,sourceIP,destPort,geo) VALUES (datetime('now', 'localtime'),?, ?, ?,?);", (proto,sourceIP,port,geo))
    print ("Protocol: " + match.group(1))
    print ("Source IP: " + sourceIP)
    print ("Time: " + logTime)
    print ("Destination Port: " + portnames[match.group(11)])
    print ("Country" + geo)
if __name__ == "__main__":
	try:
		server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")

        
