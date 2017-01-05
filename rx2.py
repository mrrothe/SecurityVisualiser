print("This is a DEBUG version - no data is written to the database, RAW syslog data is printed to the console only!!")
import socketserver
HOST, PORT = "0.0.0.0", 514
class SyslogUDPHandler(socketserver.BaseRequestHandler):
 def handle(self):
  data = bytes.decode(self.request[0].strip())
  vv = self.client_address[0]
  socket = self.request[1]
  print(data)


if __name__ == "__main__":
	try:
		server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=0.5)
	except (IOError, SystemExit):
		raise
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")

        