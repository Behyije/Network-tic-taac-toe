# import the pygame module, so you can use it
import pygame
import python.button
import sys
import socket
import time
PORT = 6666
BUF_SIZE = 1024
pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((900,720))

single_img = pygame.image.load('pic\\single.png').convert_alpha()
multi_img = pygame.image.load('pic\\multi.png').convert_alpha()
table_img=pygame.image.load('pic\\table.png')
circle=pygame.image.load('pic\\circle.png')
ex=pygame.image.load('pic\\exit.png')
xxx=pygame.image.load('pic\\xx.png')
login=pygame.image.load('pic\\login.png')
reg=pygame.image.load('pic\\reg.png')

single_button = python.button.Button(200, 100, single_img, 0.8)
multi_button = python.button.Button(200, 400, multi_img, 0.8)
ex_button = python.button.Button(800, 650, ex, 0.8)
login_button = python.button.Button(100, 300, login, 0.8)
reg_button = python.button.Button(300, 300, reg, 0.8)

font = pygame.font.SysFont("Arial", 30)
pp1=font.render("Player1:", 1, (0,0,0))
pp2=font.render("Player2:", 1, (0,0,0))
error=font.render("FAIL connect", 1, (0,0,0))
wait=font.render("Waiting connect", 1, (0,0,0))
enemytext=font.render("Enemy Turn",1,(0,0,0))
yourtext=font.render("Your Turn",1,(0,0,0))

tablelist=((230, 231),(363, 363),(387, 232),(518, 366),(541, 235),(673, 364)
              ,(231, 384),(364, 523),(383, 381),(517, 523),(542, 388),(668, 520)
              ,(232, 546),(365, 667),(386, 543),(520, 667),(536, 538),(670, 668))
tablelist=list(tablelist)

tablelist2=[0,0,0,
            0,0,0,
            0,0,0]
            
location=      ((260,260),(410,260),(570,260),
               (260,414),(410,414),(570,414),
               (260,576),(410,576),(570,576))
playertype=1
conct=0
playername=''
def start(waiting):
    screen.fill((202, 228, 241))
    if waiting == 1:
        screen.blit(yourtext,(400,0))
    else:
        screen.blit(enemytext,(400,0))
        
    screen.blit(table_img,(200,200))
    screen.blit(pp1,(10,10))
    screen.blit(pp2,(600,10))
    
    if ex_button.draw(screen):
        return 1;
    for i in range (0,9):
        if tablelist2[i] !=0:
            if tablelist2[i] == 1:
                screen.blit(circle,location[i])
            else :
                screen.blit(xxx,location[i])
    pygame.display.update()
    return 0
def checkwin():
    for i in range(0,9,3):
        if tablelist2[i]==tablelist2[i+1]and tablelist2[i+1]==tablelist2[i+2]:
            return tablelist2[i]
    for i in range(0,3):
        if tablelist2[i]==tablelist2[i+3]and tablelist2[i+3]==tablelist2[i+6]:
            return tablelist2[i]
    if tablelist2[0]==tablelist2[4]and tablelist2[4]==tablelist2[8]:
            return tablelist2[0]
    if tablelist2[2]==tablelist2[4]and tablelist2[4]==tablelist2[6]:
            return tablelist2[2]
    for i in range(0,9):
        if tablelist2[i] == 0:
            break
        if i == 8:
            return 3
def mouse_event(no):
    
    if tablelist2[no] == 0:
        tablelist2[no] = playertype
# define a main function
def faillogin():
    screen.fill((202, 228, 241))
    titleText=font.render("Fail login or register", 1, (0,0,0))
    screen.blit(titleText,(250,200))
    pygame.display.update()
    time.sleep(1)
def circlewin():
    if playertype == 1:
        screen.fill((202, 228, 241))
        titleText=font.render("You WIN!!!!!", 1, (0,0,0))
        screen.blit(titleText,(250,200))
        pygame.display.update()
        time.sleep(1)
    else:
        screen.fill((202, 228, 241))
        titleText=font.render("You LOSE!!!!!", 1, (0,0,0))
        screen.blit(titleText,(250,200))
        pygame.display.update()
        time.sleep(1)
def xxwin():
    if playertype == 2:
        screen.fill((202, 228, 241))
        titleText=font.render("You WIN!!!!!", 1, (0,0,0))
        screen.blit(titleText,(250,200))
        pygame.display.update()
        time.sleep(1)
    else:
        screen.fill((202, 228, 241))
        titleText=font.render("You LOSE!!!!!", 1, (0,0,0))
        screen.blit(titleText,(250,200))
        pygame.display.update()
        time.sleep(1)
def draw():
    if True:
        screen.fill((202, 228, 241))
        titleText=font.render("DRAW!!!!!", 1, (0,0,0))
        screen.blit(titleText,(250,200))
        pygame.display.update()
        time.sleep(1)
def main():
    global playertype,playername,conct
    serverIP = socket.gethostbyname(sys.argv[1])
    
    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server
    print('Connecting to %s port %s' % (serverIP, PORT))
    #cSocket.setblocking(False)
    pygame.display.set_caption("井字琪")
    running = True
     
    # main loop
    while running:
        screen.fill((202, 228, 241))
        #screen.blit(image, (0,0))
        if single_button.draw(screen):
            try:
                if conct ==0:
                    cSocket.connect((serverIP, PORT))
                    conct=1
                while True:
                    try:
                        screen.fill((202, 228, 241))
                        if login_button.draw(screen):
                            msg='login'
                            try:
                                cSocket.send(msg.encode('utf-8'))
                            except:
                                continue
                            msg=playername
                            try:
                                cSocket.send(msg.encode('utf-8'))
                            except:
                                continue
                            try:
                                server_reply = cSocket.recv(BUF_SIZE)
                            except:
                                continue
                            if server_reply.decode('utf-8') == 'success':
                                msg='start'
                                try:
                                    cSocket.send(msg.encode('utf-8'))
                                except:
                                    continue
                                break;
                            elif server_reply.decode('utf-8') == 'fail':
                                faillogin()
                        if reg_button.draw(screen):
                            msg='register'
                            try:
                                cSocket.send(msg.encode('utf-8'))
                            except:
                                continue
                            msg=playername
                            try:
                                cSocket.send(msg.encode('utf-8'))
                            except:
                                continue
                            try:
                                server_reply = cSocket.recv(BUF_SIZE)
                            except:
                                continue
                            if server_reply.decode('utf-8') == 'success':
                                msg='start'
                                try:
                                    cSocket.send(msg.encode('utf-8'))
                                except:
                                    continue
                                break;
                            elif server_reply.decode('utf-8') == 'fail':
                                faillogin()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                break;
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    playername=playername[:-1]
                                else:
                                    playername+=event.unicode
                        enternm=font.render(playername,1,(0,0,0))
                        nm=font.render("name:",1,(0,0,0))
                        screen.blit(nm,(0,0))
                        screen.blit(enternm,(100,0))
                        pygame.display.update()
                    except Exception as err:
                        print(err)
                num=0
                while True:
                    cSocket.setblocking(False)
                    screen.fill((202, 228, 241))
                    screen.blit(wait,(num/3,350))
                    num+=1
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            break
                    if num>2700:
                        num=0
                    pygame.display.update()
                    try:
                        server_reply = cSocket.recv(BUF_SIZE)
                    except:
                        continue
                    if server_reply.decode('utf-8')=='1' or server_reply.decode('utf-8')=='2' :
                        playertype=int(server_reply.decode('utf-8'))
                        break
                waiting=0
                if playertype ==1:
                    waiting=1
                else:
                    waiting=0
                try:
                    while running:
                        if waiting == 1:
                            for event in pygame.event.get():
                                if event.type==pygame.QUIT:
                                    running=False
                                if event.type==pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    for i in range(0,18,2):
                                        if pos[0] >tablelist[i][0] and pos[0] <tablelist[i+1][0]:
                                            if pos[1] >tablelist[i][1] and pos[1] <tablelist[i+1][1]:
                                                case = int(i/2)
                                                mouse_event(case)
                                                waiting=0
                                                try:
                                                    cSocket.send(str(case).encode('utf-8'))
                                                except:
                                                    continue
                        else:
                            for event in pygame.event.get():
                                # only do something if the event is of type QUIT
                                if event.type == pygame.QUIT:
                                    msg='exit'
                                    cSocket.send(msg.encode('utf-8'))
                                    running= False
                                    # change the value to False, to exit the main loop
                                    running = False
                            try:
                                server_reply = cSocket.recv(BUF_SIZE)
                                if playertype == 1:
                                    playertype =2
                                else:
                                    playertype=1
                                case = int(server_reply.decode('utf-8'))
                                mouse_event(case)
                                waiting=1
                                
                                if playertype == 1:
                                    playertype =2
                                else:
                                    playertype=1
                                
                            except:
                                pass
                        if start(waiting):
                            msg='exit'
                            cSocket.send(msg.encode('utf-8'))
                            running= False
                            break;
                        
                        pygame.display.update()
                        if checkwin() == 1:
                            circlewin()
                            for i in range (0,9):
                                tablelist2[i]=0
                        elif checkwin() == 2:
                            xxwin()
                            for i in range (0,9):
                                tablelist2[i]=0
                        elif checkwin() == 3:
                            draw()
                            for i in range (0,9):
                                tablelist2[i]=0
                except:
                    pass
            except Exception as er:
                screen.fill((202, 228, 241))
                screen.blit(error,(0,0))
                pygame.display.update()
                print("無法連接",er)
                time.sleep(3)
            
        if multi_button.draw(screen):
            running = False
        pygame.display.flip()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()