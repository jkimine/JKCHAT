# -*- encoding: cp949 -*-
import socket,threading,os
from time import ctime
sem = threading._Semaphore()
count = 0 #클라이언트 순서번호 매기기
name=""
usrs=[]
nickname=""
name_admin=False
Msg=""
admin = False
logo ="""\
   ___  _   __ _____  _   _   ___   _____ 
  |_  || | / //  __ \| | | | / _ \ |_   _|
    | || |/ / | /  \/| |_| |/ /_\ \  | |  
    | ||    \ | |    |  _  ||  _  |  | |  
/\__/ /| |\  \| \__/\| | | || | | |  | |  
\____/ \_| \_/ \____/\_| |_/\_| |_/  \_/  Ver.1

                                         """
th = []; conns = [];cth=[] #쓰레드 집어넣을 리스트,

def listen(s):
    global text,Msg
    try:
        while 1:
            read = s.recv(1000)
            if read=='-1':
                exit(0)
            print unicode(read,'cp949')
    except:
        print "[*] 서버와 연결이 끊겼습니다."
        a=raw_input("")
        exit(0)
        
def to_client(conn,addr,count):
    cnt = count
    global conns,name_admin,usrs
    name = conn.recv(1024)
    usrs.append(name)
    usrs = list(set(usrs))
    print "\n==== User Info ====\nID : %d\nIP : %s\nNICK : %s\nTime : %s\n===============\n"%(cnt,addr[0],name,ctime())
    for each in conns:
        if conn!=each:
            each.sendall('[*] %s(%s)님이 접속하였습니다.' %(name,addr[0]))
    conn.sendall('[*] 서버에 접속하셨습니다.')
    try:
        while 1:
            read = conn.recv(1000)
            if read=='-1':
                conn.sendall('-1')
                exit(0)
            if "@Console_Anon" in read:
                anon = (read.split(":"))
                read = '??? : %s' %(anon[1])
                print "%s님이 익명 명령어를 사용했습니다"%name
                print read
                for each in conns:
                    if conn!=each:
                        each.sendall(read)
                continue
            if "@Admin" in read:
                print "%s님이 관리자가 되었습니다."%name
                name_admin = True
                continue
            if "@Console_Clear" in read:
                print "%s님이 콘솔 화면 지우기 명령어를 사용했습니다."%name
                continue
            ############수정필요############
            if "@Console_Ban" in read and name_admin==True:
                anon = (read.split(":"))
                print "%s님이 밴 명령어를 사용했습니다."%name
                for i in range(len(usrs)):
                    if usrs[i]==anon[1]:
                        for each in conns:
                            if conns[i]!=each:
                                each.sendall("%s님이 강퇴당하셨습니다."%anon[1])
                            else:
                                each.sendall("당신은 강퇴당했습니다.")
                                usrs.remove(usrs[i])
                                conns.remove(each)
                                break
                continue
            ###################################
            if "@Console_Message" in read:
                anon = (read.split(":"))
                print "%s님이 귓속말 명령어를 사용했습니다."%name
                print "[귓속말]%s >> %s : %s"%(name,anon[1],anon[2])
                for i in range(len(usrs)):
                    if usrs[i]==anon[1]:
                        for each in conns:
                            if conns[i]==each or conn==each:
                                each.sendall("[귓속말]%s >> %s : %s"%(name,anon[1],anon[2]))
                continue
            if "@Console_Show_List" in read:
                print "%s님이 목록보기 명령어를 사용했습니다."%name
                for each in conns:
                    if conn==each:
                        each.sendall("=========List=========\n")
                for i in range(len(usrs)):
                    for each in conns:
                        if conn==each:
                            each.sendall(usrs[i]+"\n")
                for each in conns:
                    if conn==each:
                        each.sendall("\n=======================")
                continue
            if "@Console_Help" in read:
                print "%s님이 도움말을 사용했습니다."%name
                continue
            if "@Console_Say" in read and name_admin ==True:
                anon = (read.split(":"))
                read = '[*] : %s' %(anon[1])
                print "%s님이 관리자 명령어(공지)를 사용했습니다."%name
                print read
                for each in conns:
                    if conn!=each:
                        each.sendall(read)
                continue
            else:
                read = '%s : %s' %(name,read)
                print read
            for each in conns:
                if conn!=each:
                    each.sendall(read)
    except (Exception) as e:
        print(e)
        print '[INFO][%s] %s님이 나가셨습니다.'%(ctime(),name)
        usrs.remove(name)
        conns.remove(conn)
        for i in conns:
            if conn!=each:
                each.sendall('[*] %s 님이 나가셨습니다.' %name)
                exit(0)
        
while 1:
    global Msg,admin
    os.system('cls')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print logo
    print "1. 서버 만들기"
    print "2. 서버 접속하기"
    print "3. 종료"
    try:
        choice = input(">> ")
    except:
        print("[!] 잘못된 값입니다.")
        continue
    if(choice==1):
        #port =input("[*] 개방할 포트 입력 : ")
        port=1234
        try:
            s.bind(('127.0.0.1',port))
        except:
            print("[!] 잘못된 값 또는 이미 사용중인 포트입니다.")
            a=raw_input("")
            continue
        print("[*] 서버가 %d포트로 열렸습니다. 클라이언트를 기다립니다."%port)
        s.listen(1)

        while 1:
            conn,addr = s.accept()
            conns.append(conn)
            sem.acquire(); count += 1; sem.release()
            client = threading.Thread(target=to_client,args=(conn,addr,count))
            client.start()
            th.append(client);
        for t in th:
            t.join()
    elif(choice==2):
        #ip = raw_input("[*] 접속 IP 입력 : ")
        #port = input("[*] 접속 Port 입력 : ")
        ip='localhost'
        port=1234
        try:
            s.connect((ip,port))
        except Exception as e:
            print('[*] 채팅 서버에 연결 할 수 없습니다.')
            a=raw_input("")
            continue
        try:
            l = threading.Thread(target=listen,args=(s,))      #스레드 생성
            cth.append(l)
            l.start()
            while 1:
                nickname = raw_input("[*] 이름을 입력해주세요 : ")
                if ":" in nickname or "[*]" in nickname or "/" in nickname or "[!]" in nickname:
                    print "[!] 이 이름은 사용할 수 없습니다. 다시 입력해주세요."
                    continue
                else:
                    break
            s.sendall(nickname)
            while 1:
                Msg = raw_input("")
                if not Msg:
                    continue
                elif (Msg =="/목록" or Msg == "/list"or Msg == "/l"):
                    s.send("@Console_Show_List")
                elif (Msg =="/화면" or Msg == "/cls"or Msg == "/clear" or Msg =="/c"):
                    os.system('cls')
                    print logo
                    print "[*] 화면을 지웠습니다."
                    s.send("@Console_Clear")
                elif Msg =="/help" or Msg =="/헬프" or Msg =="/도움말" or Msg == "/?" or Msg=="/명령어":
                    s.send("@Console_Help")
                    if admin==False:
                        print """\
                                                    [ 명령어 도움말 ]
                                                    
                                    /help | /헬프 | /도움말 | /? | /명령어 | : 명령어 도움말 열기
                                    /c | /clear | /화면 | /cls |: 콘솔 화면 창 지우기
                                    /anon:할말 | /익명:할말 | /a:할말 : '할말' 을 익명으로 띄웁니다.
                                    /귓속말:이름:할말 | /귓:이름:할말 | /m:이름:할말 : '이름' 에게 '할말'을 보냅니다.
                                    /목록 | /list | /l : 접속자 목록을 봅니다.
                                    """
                    elif admin==True:
                        print """\
                                                    [ 명령어 도움말 ]
                                                    
                                    /help | /헬프 | /도움말 | /? | /명령어 | : 명령어 도움말 열기
                                    /c | /clear | /화면 | /cls |: 콘솔 화면 창 지우기
                                    /anon:할말 | /익명:할말 | /a:할말 : '할말' 을 익명으로 띄웁니다.
                                    /귓속말:이름:할말 | /귓:이름:할말 | /m:이름:할말 : '이름' 에게 '할말'을 보냅니다.
                                    /say:할말 | /s:할말 | /시스템:할말 : 시스템의 명칭으로 '할말'을 공지합니다.
                                    /목록 | /list | /l : 접속자 목록을 봅니다.
                                    /강퇴:이름 | /ban:이름 | /b:이름: '이름'을 강퇴시킵니다.
                                    """
                elif Msg =="#admin":
                    if admin==False:
                        print "[*] 관리자권한을 실행하기 위해선 관리자 암호가 필요합니다."
                        password = raw_input("Password : ")
                        if password=="P@ssw0rd":
                            s.send("@Admin")
                            print "[*] 관리자모드가 활성화되었습니다."
                            admin = True
                        else:
                            print "[*] 암호가 틀렸습니다."
                    else:
                        print "[!] 이미 관리자 입니다."
                elif "/anon" in Msg or "/익명" in Msg or "/a" in Msg:
                    s.send("@Console_Anon"+Msg)
                elif ("/b" in Msg or "/강퇴" in Msg or "/ban" in Msg) and admin==True:
                    s.send("@Console_Ban"+Msg)
                elif ("/시스템" in Msg or "/say" in Msg or "/s" in Msg) and admin==True:
                    s.send("@Console_Say"+Msg)
                elif "/귓속말" in Msg or "/귓" in Msg or "/m" in Msg:
                    s.send("@Console_Message"+Msg)
                else: s.send(Msg)
            s.close()
        except:
            pass
            exit(0)

        for t in th2:
            t.join()
    elif(choice==3):
        exit(0)
    else:
        print("[!] 잘못된 값입니다.")
        a=raw_input("")
        continue

if __name__ == "__main__":
    main()
