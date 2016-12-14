import argparse, threading, time
import client as sc
import server as ss

IP = '127.0.0.1'
clientPort = 8000
serverPort = 8001

parser = argparse.ArgumentParser(description='A chat client secured using DES with Diffie-Helman for key selection')
parser.add_argument('-ip', required=False, help='The IP to connect to to chat.', nargs=1, type=str, metavar='IP', dest='ip')
parser.add_argument('-cp', required=False, help='Port to use for client', nargs=1, type=int, metavar='cPort', dest='cport')
parser.add_argument('-sp', required=False, help='Port to use for server', nargs=1, type=int, metavar='sPort', dest='sport')

args = parser.parse_args()

if args.ip != None:
   IP = args.ip
if args.cport != None:
   clientPort = int(args.cport[0])
if args.sport != None:
   serverPort = int(args.sport[0])

def main():
   lock = threading.Lock()

   client = sc.Client(IP, clientPort, lock)
   server = ss.Server(serverPort, lock)

   client.daemon = True
   server.daemon = True

   client.start()
   server.start()

   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
