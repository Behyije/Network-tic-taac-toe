import socket
import threading
import time
import sys
PORT = 6666
backlog = 5
BUF_SIZE = 1024            # Receive buffer size
player_id=[]
online=0
connect=[]
playing=0
ply1=0
ply2=0
ply1ok=0
ply2ok=0
bb=1

class ServerThread(threading.Thread):
    def __init__(self, t_name, client_sc, rip, rport):
        global ply1
        global ply2
        global ply1ok
        global ply2ok
        global online
        super().__init__(name = t_name)
        self.client = client_sc
        self.rip = rip
        self.rport = rport
        online+=1
        print("有一人上線了")
        while True:
            if ply1==0:
                ply1= self.client
                self.player=1
                break;
            elif ply2 ==0:
                ply2=self.client
                self.player=2
                break;
        self.start()            # Start the thread when it is created
    # end for __init__()
    
    def run(self):
        global ply1
        global ply2
        global ply1ok
        global ply2ok,online,bb
        login=True
        self.client.setblocking(True)
        while login:
            try:
                client_msg=self.client.recv(BUF_SIZE)
            except:
                continue
            state =client_msg.decode('utf-8')
            try:
                client_msg=self.client.recv(BUF_SIZE)
            except:
                continue
            name =client_msg.decode('utf-8')
            if state == 'register':
                print("申請註冊")
                try :
                    for i in player_id:
                        if i == name :
                            sever_reply='fail'
                            self.client.send(sever_reply.encode('utf-8'))
                            login=False
                    if login:
                        player_id.append(name)
                        sever_reply='success'
                        self.client.send(sever_reply.encode('utf-8'))
                        login=False
                    else:
                        login=True
                except:
                    player_id.append(name)
                    sever_reply='success'
                    self.client.send(sever_reply.encode('utf-8'))
                    login=False
            else :
                print('申請登錄')
                try :
                    if len(player_id)>0:
                        num=0
                        for i in player_id:
                            if i == name :
                                sever_reply='success'
                                self.client.send(sever_reply.encode('utf-8'))
                                login=False
                                break
                            num+=1
                            if num == len(player_id):
                                sever_reply='fail'
                                self.client.send(sever_reply.encode('utf-8'))
                                login=True
                    else:
                        sever_reply='fail'
                        self.client.send(sever_reply.encode('utf-8'))
                        login=True
                except:
                    sever_reply='fail'
                    self.client.send(sever_reply.encode('utf-8'))
                    login=True
                    pass
        client_msg=self.client.recv(BUF_SIZE)
        while True:
            self.client.setblocking(True)
            if client_msg.decode('utf-8') == 'start':
                if self.player ==1:
                    ply1ok=1
                else:
                    ply2ok=1
            if ply2ok and ply1ok:
                msg=str(self.player)
                self.client.send(msg.encode('utf-8'))
                while ply1ok==1 and ply2ok==1:
                    try:
                        if self.player ==1:
                            client_msg = ply1.recv(BUF_SIZE)
                        else:
                            client_msg = ply2.recv(BUF_SIZE)
                        if client_msg.decode('utf-8')=='exit':
                            ply1ok=0
                            ply2ok=0
                            ply1=0
                            ply2=0
                            online-=1
                            self.client.close()
                            break
                        if client_msg:
                            msg =": Receive messgae: " + client_msg.decode('utf-8') + ",from IP: " + str(self.rip) + " port: " + str(self.rport)
                            print(msg)
                            print("轉發給別的玩家")
                            # wait for 5 second
                            if self.player==1:
                                try:
                                    ply2.send(client_msg)
                                except:
                                    continue
                            else :
                                try:
                                    ply1.send(client_msg)
                                except:
                                    continue
                    except KeyboardInterrupt:
                        break;
                    except:
                        continue
            if client_msg.decode('utf-8')=='exit':
                print("player",self.player,"下線了")
                break
    # end run()
# end for ServerThread
def command():
    global bb,online
    while bb:
        try:
            cmd=int(input("""##########################
1.在線人數
2.已有帳號
3.關閉服務器
###################"""))
            print("")
            if cmd == 1:
                print("目前在線人數",online)
            if cmd ==2:
                if len(player_id) >0:
                    t=0
                    print("帳號:")
                    for i in player_id:
                        t+=1
                        print(t,".",i)
            if cmd ==3 :
                if online == 0 :
                    bb=False
                    sys.exit()
                    exit()
                    break
                else : 
                    print("必須等待所有成員離開")
        except KeyboardInterrupt:
            sys.exit()
            break
        except:
            pass
    
def main():
    threading.thread = threading.Thread(target=command)
    threading.thread.setDaemon(True)
    threading.thread.start()
    # Create a TCP Server socket
    srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Starting up server on port: %s' % (PORT))
    srvSocket.bind(('', PORT))
    srvSocket.listen(backlog)
    i=0;
    while True:
        srvSocket.setblocking(False)
        try:
            if bb ==False:
                print ("server close")
                srvSocket.close()
                sys.exit()
                break
            try:
                client, (rip, rport) = srvSocket.accept()
                i=i+1;
                t_name = 'Thread ' + str(i)
                print('連線來自於',rip,rport)
                t = ServerThread(t_name, client, rip, rport)
            except:
                pass
        except KeyboardInterrupt:
            srvSocket.close()
            break;
    srvSocket.close()
# end of main

if __name__ == '__main__':
    main()
