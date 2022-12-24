import firebase_admin
#method 1
from firebase_admin import db
#method 2
from firebase_admin import firestore
from firebase_admin import credentials
from firebase import firebase

#from os import times_result
from socket import *

import threading
import time
from queue import Queue
import sys

#firestore method
#get firebase private key file
cred = firebase_admin.credentials.Certificate("./pythonServiceAccountKey.json")
#initialize firebase
firebase_admin.initialize_app(cred)

db = firestore.client()

#Reatime Method
#firebase = firebase.FirebaseApplication("https://codeexamdata-default-rtdb.firebaseio.com/", None)

#queue will push and pop data to be sent to database, stored elements are lists of 2 dictionaries
q = Queue(maxsize = 10)


HOST = ''
#port for listening
PORT = 21567
#max size for packet
BUFSIZE = 1024
ADDR = (HOST, PORT)

player_name = ''

#send data to database
def send_Firebase(data):

    #send respective data to specified collection within db
    db.collection('chartData').add(data[0])
    db.collection('timeData').add(data[1])

def read_data(): #process for listening for data through port
    
    while True:
        #create socket to listen for incoming data
        sock = socket(AF_INET, SOCK_STREAM)
        #sock.setblocking(0)
        #sock.settimeout(0.5)
        sock.bind(ADDR)
        sock.listen(5)
        
    
        while True:
            print("Begin reading data")
            try:
                #accept data when recognized, name sender addr
                client,addr = sock.accept()
                data_bytes = ''
                data_bytes = client.recv(BUFSIZE)
                if not data_bytes:
                    print("not data, break")
                    break
                else:
                    print("command recievedf from: ", addr)
                    #decode byte data to string
                    data_str = data_bytes.decode()

                    #convert data for proper storage in db
                    #data for chart 1 and chart 2 are separated by "/"
                    split_data = data_str.split('/')

                    #data fields are separated by "_"
                    data_career = split_data[0].split('_')
                    data_seasons = split_data[1].split('_')
                    player_name = data_career[0]

                    #array values are separated by ","
                    data_seasons_seasonID = data_seasons[0].split(',')
                    data_seasons_seasonPTS = data_seasons[1].split(',')
                    data_seasons_seasonAST = data_seasons[2].split(',')

                    #pts and ast array converted from string to int for storage
                    data_seasons_seasonPTS =list(map(int,data_seasons_seasonPTS))
                    data_seasons_seasonAST =list(map(int,data_seasons_seasonAST))

                    #package all fields into single array to be sent to db collections
                    data_dict_career = {
                        'name': data_career[0],
                        'points': data_career[1],
                        'assists': data_career[2]
                    }
                    data_dict_season = {
                        'name': data_career[0],
                        'years': data_seasons_seasonID,
                        'points': data_seasons_seasonPTS,
                        'assists': data_seasons_seasonAST
                    }
                    q.put([data_dict_career,data_dict_season])
            except KeyboardInterrupt:
                print("exited")
                exit()
        #print("read loop broke")

def store_data():
    #store to firebase
    while True:
        #Enter if queue receives an item
        if q.empty() is False:
            #pop data to be store, run storage function
            data = q.get()
            print("Storing ", player_name, " stats to Firebase")
            send_Firebase(data)

        

#thread allow to read and store simultaneously 
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