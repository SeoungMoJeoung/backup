from read_segment import read_seg
from mapping import trajectory2segment
from convertToSpeed import convert2speed

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Pool
from queue import Queue

import threading
import socket
import time
import json
import sys
import datetime
import pymysql
import os
import gc
def main():
    global cell
    global link_id
    global F_NODE
    global que
    que = Queue()
    '''
    global traj_db
    traj_db = pymysql.connect(
        user='root', 
        passwd='1', 
        host='192.168.1.16', 
        db='testdb', 
        port=3306,
        charset='utf8')
    '''
    cell, link_id, F_NODE = read_seg()
    print("start server...")
    s_th = threading.Thread(target=server)
    s_th.daemon = True
    s_th.start()
    
    # pool = Pool(processes=10)

    # count = 0
    # while True:
    #     if que.qsize() != 0:
    #         #q=time.time()
    #         value = que.get()
    #         pool.apply_async(mapping, (value,))
    #         #print("q",time.time() -q)
    #         count += 1
    #         if count % 100 == 0:
    #             #gc.collect()
    #             print(count, que.qsize())
    
    count = 0
    print("main")
    while True:
        with Pool(processes=20) as pool:
            print("Pool create")
            while True:
                if count == 50000:
                    break
                if que.qsize() != 0:
                    count += 1
                    #q=time.time()
                    value = que.get()
                    pool.apply_async(mapping, (value,))
                    #print("q",time.time() -q)
                    if count % 1000 == 0:
                        #gc.collect()
                        print(count, que.qsize())

def mapping(value):
    
    try:
        start = time.time()
        #print("value:",sys.getsizeof(value))
        data = traj_info_db(value)
        #print("data:",sys.getsizeof(data))
        traj_point = extract_point(data)
        #print(os.getpid(),"traj_point")
        #print("traj_point:",sys.getsizeof(traj_point))
        mapping_data = trajectory2segment(traj_point, cell, link_id, F_NODE)
        #print(os.getpid(),"mapping_data")
        #print("mapping_data:",sys.getsizeof(mapping_data))
        speed_data = convert2speed(data, mapping_data)
        #print("speed_data:",sys.getsizeof(speed_data))
        #print(os.getpid(),"speed_data")
        update_db(speed_data)
        #print(os.getpid(),"end",time.time()-start)
    except Exception as e:
        print("프로세스 전사")
        print(os.getpid(),"error code :",e)

def extract_point(data):
    traj = []
    data = json.loads(data[0]["jsondata"])
    for i in data[0]["items"]:
        gps = []
        lat = i["lat"]
        lng = i["lng"]
        gps = [lat,lng]
        traj.append(gps)
    return traj

def traj_info_db(value):
    try:
        traj_db = pymysql.connect(
            user='root', 
            passwd='1', 
            host='192.168.1.16', 
            db='testdb', 
            port=3306,
            charset='utf8')
        uid_bt = json.loads(value)
        cursor = traj_db.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM TB_TRACKING2_DATA_" + uid_bt["time_begin"][:10].replace("-","") + " WHERE uuid = %s and time_begin = %s"
        cursor.execute(sql, (uid_bt["uuid"], uid_bt["time_begin"]))
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("traj_db 비정상 연결 끊김")
        print(e)
    finally:
        traj_db.close()

def update_db(speed):
    try:
        speed_db = pymysql.connect(
            user='root', 
            passwd='1', 
            host='192.168.1.16', 
            db='updatedb', 
            port=3306,
            charset='utf8')
        cursor = speed_db.cursor()
        #sql = "insert into LINK_SPEED_DATA(SPEED, LINK_ID) values (%s,%s)"
        sql = "update LINK_SPEED_DATA set SPEED = %s, UPDATE_TIME = %s where LINK_ID = %s"
        cursor.executemany(sql, speed)
        speed_db.commit()
    except Exception as e:
        print("update db 비정상 연결 끊김")
        print(e)
    finally:
        speed_db.close()

def accept(client_socket, addr):
    result = ""
    # 무한루프를 돌면서
    while True:
        
        # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
        data = client_socket.recv(1024)
        
        # 빈 문자열을 수신하면 루프를 중지합니다. 
        if not data:
            # 수신받은 문자열을 출력합니다.
#            print('Received from', addr, result)
            que.put(result)
#            print("que size:",que.qsize())

            break
    
        # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
        client_socket.sendall(data)

        result += data.decode()

    # 소켓을 닫습니다.
    client_socket.close()
    #server_socket.close()

def server():
    
    # 접속할 서버 주소입니다. 여기에서는 루프백(loopback) 인터페이스 주소 즉 localhost를 사용합니다. 
    HOST = '192.168.1.16'
    
    # 클라이언트 접속을 대기하는 포트 번호입니다.   
    PORT = 9990
    
    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 포트 사용중이라 연결할 수 없다는 
    # WinError 10048 에러 해결를 위해 필요합니다. 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
    # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
    # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다. 
    # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.  
    server_socket.bind((HOST, PORT))
        
    # 서버가 클라이언트의 접속을 허용하도록 합니다. 
    server_socket.listen()
    
    # while True:
    #     with ProcessPoolExecutor(max_workers=20) as pool:
    #         pool.submit(accept, server_socket)
    
    while True:
        client_socket, addr = server_socket.accept()
        # 접속한 클라이언트의 주소입니다.
#        print('Connected by', addr)
        accept(client_socket, addr)
        #th = threading.Thread(target=accept, args=(client_socket, addr))
        #th.daemon = True
        #th.start()

main()
