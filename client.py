import threading
import socket
import struct
import bitstring as bs
import pydes
import pydh

class Client(threading.Thread):
   def __init__(self, ip, port, lock):
      super(Client, self).__init__()
      self.ip = ip
      self.port = port
      self.lock = lock
      self.box = None
   
   def run(self):
      self.startup()
      while True:
         text = str(raw_input())
         text += '\f'
         hext = text.encode('hex')
         ba = bs.BitArray(hex='0x'+hext)

         buff = '' 
         for block in ba.cut(64):
            c = self.box.encrypt(block)
            buff += c.hex
            self.sock.send(c.bytes)
            
         lastbit = self.box.encrypt(ba[ba.length/64 * 64:])
         buff += lastbit.hex
         self.sock.send(lastbit.bytes)
         self.tprint(buff)


   def startup(self):
      self.tprint("Starting up...")
      self.tprint("Attempting to connect at " + self.ip + ":" + str(self.port))
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      err = 1
      while err != 0:
         err = self.sock.connect_ex((self.ip, self.port))

      self.tprint("Speaking on port " + str(self.port))
      self.tprint("Initiating Diffie-Hellman...")
      DH = pydh.DiffieHellman(generator=2, group=17)
      self.sock.send(struct.pack('!II', 2, 17))

      self.sock.send(bytes(DH.publicKey))
      otherKey = int(self.sock.recv(4096))
      DH.genKey(otherKey)

      self.box = pydes.DES(DH.getKey()[:16])
      self.box.genSubKeys()
      self.tprint("DES Key=" + str(DH.getKey()[:16]))
      self.tprint('DES key calculated, beginning DES communication now!')

   def tprint(self, str):
      self.lock.acquire()
      print '\033[94m[Client]\033[0m', str
      self.lock.release()


if __name__=='__main__':
   print 'Do not run this module as main.'
else:
   pass
