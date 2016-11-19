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

def client():
 try:
    host = "kadikoy.sekizbit.xyz"
    port = 4000
    sq = 0; g = ''; say= 0
    addr = host, port
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    print 'UDP Client Factory Started'
    print "Sequence Number\t;TimeStamp;\tSend Time;\t\t\t: DATA"
    while 1:
        line = "seq="+str(sq).zfill(7)+";"+str(time.time())+";"+str(datetime.now())+";"+": ###########"
        logfile.write(line)
        s.sendto(line, addr)
        print "seq="+str(sq).zfill(7)+"\t;"+str(time.time())+";\t"+str(datetime.now())+";\t"+": ###########"
        if say == 0:
                ilkunix=time.time()
        say+=1; sq+=1

        time.sleep(0.3)
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
        prt = 4000
        ss = socket(AF_INET, SOCK_DGRAM)
        ss.bind(('', prt))
        print '\nUDP Server Factory Started'
        print "Sequence Number\t;TimeStamp;\tSend Time;\t\t\t: DATA"
        while 1:

                while not d.endswith("#"):
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
                print "\nOrtalama Delay:\t" +str(delay)+" ms."
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


    p2 = Process(target=server)
    p2.start()
    processes.append(p2)

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
                print ""
    finally:
                print ""                          
