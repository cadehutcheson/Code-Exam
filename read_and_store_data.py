#firestore method
import firebase_admin
#method 1
from firebase_admin import db
#method 2
from firebase_admin import firestore

from firebase_admin import credentials

#realtime method
from firebase import firebase


#from os import times_result
from socket import *
#from time import ctime
#import struct
import threading
import time
from queue import Queue
import sys

#firestore method
#method 2
#get firebase private key file
cred = firebase_admin.credentials.Certificate("./Python/pythonServiceAccountKey.json")
#initialize firebase
firebase_admin.initialize_app(cred)

db = firestore.client()

#Reatime Method
#firebase = firebase.FirebaseApplication("https://codeexamdata-default-rtdb.firebaseio.com/", None)

q = Queue(maxsize = 10)


HOST = ''
#port for listening
PORT = 21567
#max size for packet
BUFSIZE = 1024
ADDR = (HOST, PORT)

def send_Firebase(data):
    
    # firstData = {
    #     'name' : "Lebron James",
    #     'points': 100
    # }
    print(data[0])
    print(data[1])
    #firestore method
    db.collection('chartData').add(data[0])
    db.collection('timeData').add(data[1])

def read_data(): #process for app control
    
    while True:
        #create server side tcp socket to listen for incoming data from app
        sock = socket(AF_INET, SOCK_STREAM)
        #sock.setblocking(0)
        #sock.settimeout(0.5)
        sock.bind(ADDR)
        print("a1")
        sock.listen(5)
        
    
        while True:
            print("Begin reading data")
            # data sent in multiple sends will be parsed together by recive if not handled yet
            try:
                client,addr = sock.accept()
                data_bytes = ''
                data_bytes = client.recv(BUFSIZE)
                if not data_bytes:
                    print("not data, break")
                    break
                else:
                    print("command recieved:" + str(data_bytes))
                    #time.sleep(3)
                    data_str = data_bytes.decode()
                    split_data = data_str.split('/')
                    data_career = split_data[0].split('_')
                    data_seasons = split_data[1].split('_')
                    data_seasons_seasonID = data_seasons[0].split(',')
                    data_seasons_seasonPTS = data_seasons[1].split(',')
                    data_seasons_seasonID.pop()
                    data_seasons_seasonPTS.pop()
                    data_seasons_seasonPTS =list(map(int,data_seasons_seasonPTS))
                    data_dict_career = {
                        'name': data_career[0],
                        'points': data_career[1],
                        'assists': data_career[2]
                    }
                    data_dict_season = {
                        'name': data_career[0],
                        'years': data_seasons_seasonID,
                        'points': data_seasons_seasonPTS
                    }
                    q.put([data_dict_career,data_dict_season])
                    print("end")
                    #Thread?
                    #store_data()
            except KeyboardInterrupt:
                print("exitedd")
                exit()
        print("read loop broke")

def store_data():
    #store to firebase
    while True:
        #while statement redundant if q.get is blocking?
        #print("looping store")
        #time.sleep(1)
        
        #while q.empty() is False:
        #print("Waiting to store")
        if q.empty() is False:
            data = q.get()
            print("Storing " + str(data) + " to Firebase")
            send_Firebase(data)

        


t_read = threading.Thread(target=read_data)
t_store = threading.Thread(target=store_data)

#main function starts and joins both threads
if __name__ == '__main__':

    try:
        t_read.start()
        t_store.start()
        t_read.join()
        t_store.join()
    except KeyboardInterrupt:
        print("Closing program")
        sys.exit(0)