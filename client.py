import threading
import socket

class Client(threading.Thread):
   def __init__(self, ip, port, lock):
      super(Client, self).__init__()
      self.ip = ip
      self.port = port
      self.lock = lock
   
   def run(self):
      self.startup()
      while True:
         text = str(raw_input())
         self.tprint(text)
         self.sock.send(text)

   def startup(self):
      self.tprint("Starting up...")
      self.tprint("Attempting to connect at " + self.ip + ":" + str(self.port))
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      err = 1
      while err != 0:
         err = self.sock.connect_ex((self.ip, self.port))

      self.tprint("Speaking on port " + str(self.port))

   def tprint(self, str):
      self.lock.acquire()
      print '\033[94m[Client]\033[0m', str
      self.lock.release()


if __name__=='__main__':
   print 'Do not run this module as main.'
else:
   pass
