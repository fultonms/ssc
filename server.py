import threading
import socket

class Server(threading.Thread):
   def __init__(self, port, lock):
      super(Server, self).__init__()
      self.port = port
      self.lock = lock

   def run(self):
      self.startup()
      while True:
         text = self.client.recv(4096).decode('ascii')
         if text != '':
            self.tprint(text)

   def startup(self):
      self.tprint("Starting up...")
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind(('127.0.0.1', self.port))
      self.sock.listen(0)
      self.tprint("Listening for connections on port " + str(self.port))

      (clientSocket, address) = self.sock.accept()
      self.client = clientSocket
      self.tprint("Made connection with client at " + str(address))
      

   def tprint(self, str):
      self.lock.acquire()
      print "[Server]", str
      self.lock.release()

if __name__=='__main__':
   print 'Do not run this module as main.'
else:
   pass
