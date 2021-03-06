#/usr/bin/python 
#oneway.responder.py

#Responder 	Listen UDP Port 4003
#		Send   UDP Port 4002	



import sys,time,re
from socket import *
from datetime import datetime
import sys, traceback



log = ''; d = ''; say =int(0)



BUFSIZE = 9000



def responser(rhost, message):
    rport=4002
    raddr = rhost,rport
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    mess = re.split(";", message)
    t0 = mess[1]
    seq0=mess[0]

    line = seq0+"     ;"+t0+";"+" RTT HESABI ICIN GERI GONDERILEN PAKET ; PS#PE"
    print line #"RTT HESABI ICIN GERI GIDEN PAKET            "+seq0+";"+t0
    s.sendto(line, raddr)


def main():
    try:
                def server():

                        port = 4003; prob_seq = ''
                        global say, d,ilk,ilkl,t2,log, t2unix, ilkunix, logfile, seq1, seq2, prob_seq, delay_interval
                        s = socket(AF_INET, SOCK_DGRAM)
                        s.bind(('', port))
                        print 'udp echo server ready'
                        while 1:

                                while not d.endswith("PE"):
                                                data, addr = s.recvfrom(BUFSIZE)
                                                d+=data;
                                seq2=int(d[4:11])
				header=re.split("PS", d)
				payloadsize=len(header[1])+68

                                t2 = str("%.9s" % datetime.now().strftime("%H:%M.%f")); t2unix=time.time()
                                log = t2+' Responder received %r from %r with %r BYTE IP Payload' % (header[0], addr, payloadsize)
                                print log
                                logfile.write(log+"\n")
                                log = ''
                                if say == 0:
                                        ilk = t2;
                                        ilkunix = int(t2unix)
                                        ilkl = log
                                        seq1=seq2-1

                                if say%5 == 0:
                                        responser(addr[0],d)

                                d = ''; say+=1

                                if (seq2-seq1) != 1:
                                        prob_seq+=str(seq1)+","
                                seq1=seq2



                server()

    except KeyboardInterrupt:
                logfile.write("\n"+str(t2unix-ilkunix)+" sn surede :"+str(say)+" adet paket yakalandi.\n ilk paket yakalanma zamani:"+ilk+"\n son paket yakalanma zamani "+t2+"\n problemli sequence numbers: "+prob_seq);  logfile.close(); print "\n"+str(t2unix-ilkunix)+" sn surede :"+str(say)+" adet paket yakalandi.\n ilk paket yakalanma zamani:"+ilk+"\n son paket yakalanma zamani "+t2+"\n problemli sequence numbers: "+prob_seq+"\n"
    except Exception:
                traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    logfile = open(str(datetime.now().strftime("%H.%M.%S_%f"))+'_oneway_client_data.txt', 'a')
    main()                                            
