#/usr/bin/python
#oneway.responder.py

#Sender         Listen UDP Port 4002
#               Send   UDP Port 4003

#oneway.client.v1.py
import multiprocessing
import sys,time,re,time
from socket import *
from datetime import datetime
import sys, traceback
from multiprocessing import Process, Manager
from time import sleep

global d, s, toplamdelay, mess, delay, ortalamdelay, maxdelay, mindelay
global g, sq, say, ilkunix

logfile = open(str(time.time())+'_oneway_client_data.txt', 'a')

size=100
interval=1
#####SYS.ARGV SET########################
argsayisi=len(sys.argv)
print argsayisi ; a=1
for k in sys.argv[1:]:
        if a==argsayisi:
                break

        if k == "?":
                print "USAGE :\n\t -s for SIZE\n\t -i for INTERVAL\n\t And Responder IP:X.X.X.X \n\t oneway.sender.py -s 100 -i 50 1.2.3.4 \n "
                sys.exit()

        elif k=="-s" and sys.argv[a+1]!="?":
                size=int(sys.argv[a+1])

        elif k=="-i"and sys.argv[a+1]!="?":
                interval = float(sys.argv[a+1])/1000

        elif "." in k :
                destinationip=str(sys.argv[a])
        a+=1

#####Payload Calculation/Creation########


payload='PS' #payload started

if size > 70:
        print "pass"
        for i in xrange(size-70):
                payload+="#"

payload+="PE" #payload ended
ip_payload_size=len(payload)+66



def client():
 try:
    host = destinationip
    port = 4003
    sq = 0; g = ''; say= 0
    addr = host, port
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', 0))
    print 'UDP Client Factory Started'
    print "Sequence Number\t;TimeStamp;\tSend Time;\t\t\t: DATA"
    while 1:

        senddata='',
        header = "seq="+str(sq).zfill(7)+" ; "+str("%.3f" % float(time.time()))+" ; SRC_TIME: "+str("%.9s" % datetime.now().strftime("%H:%M.%f"))+" ; "+"APP_HEAD_END"
        print header+" SEND DATA WITH: "+str(ip_payload_size)+" BYTE IP PAYLOAD"
        senddata=header+payload
        logfile.write(header)
        s.sendto(senddata, addr)
        if say == 0:
                ilkunix=time.time()
        say+=1; sq+=1

        time.sleep(interval)
 except KeyboardInterrupt:
                print "\n"
                print "\nUDP Client Factory Istatislikleri"

                logfile.write("\n"+str(time.time()-ilkunix)+" sn. surede : "+str(say)+" adet ONEWAY paket yollandi. \n"); logfile.close()
 finally:
                print "\n"+str(time.time()-ilkunix)+" sn. surede : "+str(say)+" adet ONEWAY paket yollandi. \n"


def server():
 try:


        d = ''
        s=0; toplamdelay = float(0); ortalamadelay = float(0); maxdelay = float(0); mindelay = float(0)
        prt = 4002
        ss = socket(AF_INET, SOCK_DGRAM)
        ss.bind(('', prt))
        print '\nUDP Server Factory Started'
        print "Sequence Number\t;TimeStamp;\tSend Time;\t\t\t: DATA"
        while 1:

                while not d.endswith("PE"):
                                data, addr = ss.recvfrom(100)
                                d+=data;

                mess = re.split(";",d)
                delay = 1000*(time.time()-float(mess[1]))
                if s == 0:
                        mindelay=delay
                        maxdelay=delay
                if delay > maxdelay:
                        maxdelay=delay
                elif delay < mindelay:
                        mindelay=delay

                toplamdelay+=delay; s+=1
                ortalamadelay=toplamdelay/s
                print "\nOrtalama Delay:\t" +str("%.3f" % delay)+" ms."
                log = str(data)+" from "+str(addr)
                print log
                log = ''; d = ''; data = ''

 except KeyboardInterrupt:
                logfile.write("\nOrtalama Delay:\t" +str(1000*(time.time()-float(mess[1])))+" ms."); logfile.close()
                print "\n"
                print "\nUDP Server Factory Istatislikleri"

 finally:
                print "\nToplam " +str(s)+ " adet ONEWAY paketi cevabi (REPLY) yakalandi. REPLY paketlerine gore :\nOrtalama Delay: "+str(ortalamadelay)+" ms.  Maximum Delay: "+str(maxdelay)+" ms.  Minimum Delay: "+str(mindelay)+" ms."





if __name__ == '__main__':
    processes = []

    manager = Manager()


    p = Process(target=client)
    p.start()
    processes.append(p)


    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
                print ""
    finally:
                print ""      
