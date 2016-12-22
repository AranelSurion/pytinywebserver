# -*- coding: utf-8 -*-
# pytinywebserver by Yekta "Aranel" Leblebici <yekta@iamyekta.com>

# Imports
import socket
import os
import sys
import threading
import time
import signal
import time

# Check Python version
if sys.version_info[:1] < (3,):
	print ("This software does not work on versions older than Python 3.")
	os._exit(0)



# Variables
PORT = 80
global STATUS
STATUS = 1

# Creating a socket and binding
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT)) 
s.settimeout(2)
s.listen(50)

# Signal handler
def signal_handler(signum, frame):
	global STATUS
	print("Exiting now.")
	STATUS = 0

# Main server thread
def thread_server():
	global STATUS
	print ("Web server thread started on " + str(PORT))
	while True:
		if STATUS == 0:
			print("[Server Thread] Exiting.")
			exit();
		try:
			connection, addr = s.accept()
			connection.settimeout(2)
			data = connection.recv(4096) # Be careful, this is a blocking method.
			print ("[Server Thread] Accepted a connection from " + addr[0] + ":" + str(addr[1]))
			threading.Thread(target=thread_worker, args=(connection, data)).start()
			connection = None
			addr = None
		except socket.timeout:
			pass




# A worker thread
def thread_worker(connection, data):
	
	data = data.decode("UTF-8")

	# TODO PARSER GOES HERE

		# IF FIRST FOUR WORDS ARE "GET"
	theDirective = data[:4]
	print(theDirective)
	print(data[4:])

	if theDirective == "GET ":
		# TAKE NEXT WORD, APPEND TO WWWROOT
		requestedFile = data[4:].rsplit()[0]
		print(requestedFile)

		if requestedFile == "/": # Client requesting index.
			requestedFile = "/index.html"

		requestedFile = os.getcwd() + requestedFile
		print(requestedFile)
		# TODO CHECK IF ACCEPTABLE (PWD) - CHANGE WWWROOT  #important

	elif theDirective == "POST": #TODO HANDLE THIS? HANDLE "HEAD"?
		connection.send("POST methods are not supported yet.")
		connection.close()
		exit()

	else: # ?? land of unicorns and rainbows I suppose.
		print("[Worker Thread] Neither GET, Nor POST. What to do then? I am outta here.")
		connection.close()
		exit()
		pass



			

		
	# TODO HOW TO HANDLE MIMETYPES?
	# TODO SEND THE HEADERS. PROPERLY.
	# SEND THE FILE.
	# TODO LOG IP?

	# Getting system time, to be used in HTTP headers.
	date = time.strftime("%a, %d %b %Y %H:%M:%S GMT")
	try: # Does this file exist? If it does:
		thePage = open(requestedFile, "rb") #TODO What happens if file exists but empty?
		httpStatusCode = "200 OK"
		print("[Worker Thread] %s: %s"  % (httpStatusCode, requestedFile))
		outputBuf = "HTTP/1.1 %s\r\nDate: %s\r\nServer: pytinywebserver/1.0.0\r\n\r\n" % (httpStatusCode, date) # TODO make an output buffer
		outPage = thePage.read() # Read file contents in bytes
		outputBuf = outputBuf.encode('utf-8') + outPage # Glue the header and content together.
		connection.sendall(outputBuf)
		outputBuf = ""
		thePage.close()
	except (IOError): # If the file does not exist:
		httpStatusCode = "404 Not Found"
		print("[Worker Thread] %s: %s"  % (httpStatusCode, requestedFile))
		outputBuf = "HTTP/1.1 %s\r\nDate: %s\r\nServer: pytinywebserver/1.0.0\r\n\r\n" % (httpStatusCode, date) # TODO make an output buffer
		outputBuf = outputBuf + "<div align=\"center\"><h1>%s</h1><hr><i>pytinywebserver</i></div>" % httpStatusCode
		outputBuf = outputBuf.encode('utf-8')
		connection.sendall(outputBuf)
		outputBuf = ""		

	# TODO HANDLE KEEP-ALIVE. Per HTTP > 1.0, all connections are keep-alive unless stated otherwise.
	# HOW: check if NOT "Connection: close", if: connection.close(). if not: keep connection open, loop back, set timeout to 5seconds.

	# Closing connection. 

	connection.close()
	print ("[Worker Thread " + str(threading.get_ident()) + "] Connection closed. Thread exiting." )
	exit()


# Let the server start.
signal.signal(signal.SIGINT, signal_handler)
threading.Thread(target=thread_server).start()
