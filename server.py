import threading
import socket
import struct
import bitstring
import pydes
import pydh

class Server(threading.Thread):
   def __init__(self, port, lock):
      super(Server, self).__init__()
      self.port = port
      self.lock = lock
      self.box = None

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
      self.tprint("Waiting for Diffie-Helman initation...")
      buff = self.client.recv(8)
      gen, group = struct.unpack('!II', buff)
      
      self.tprint("Diffie-Helman initiated!")
      DH = pydh.DiffieHellman(generator=gen, group=group)

      self.client.send(bytes(DH.publicKey))
      otherKey = int(self.client.recv(4096))
      DH.genKey(otherKey)

      self.box = pydes.DES(DH.getKey()[:16])
      self.box.genSubKeys()
      self.tprint('DES key calculated, beginning DES communication now!')

   def tprint(self, str):
      self.lock.acquire()
      print '\033[92m[Server]\033[0m', str
      self.lock.release()

if __name__=='__main__':
   print 'Do not run this module as main.'
else:
   pass
