#!/usr/bin/python3

from plexapi.myplex import MyPlexAccount
import getpass
from multiprocessing.dummy import Pool as ThreadPool 

pool = ThreadPool(10) 
username = input('What is your username? ')
password = getpass.getpass(prompt ='What is your password? ')
account = MyPlexAccount(username, password)

server_1_name = 'Hades'
server_2_name = 'HadesCloud'
server_1 = account.resource(server_1_name)
server_2 = account.resource(server_2_name)
conn_1 = server_1.connect()
conn_2 = server_2.connect()

#print(len(conn_2.library.section('TV Shows').search()))

server_1_shows = set(list(map((lambda x: x.title), conn_1.library.section('TV Shows').search())))
server_2_shows = set(list(map((lambda x: x.title), conn_2.library.section('TV Shows').search())))

common_shows = server_1_shows & server_2_shows
def showshowname(show_name):
    print(show_name)

def checkshow(show_name):
    server_1_show = conn_1.library.section('TV Shows').get(show_name)
    server_2_show = conn_2.library.section('TV Shows').get(show_name)
    #print(show_name)
    i = 0
    for ep in server_1_show.episodes():
        for ep2 in server_2_show.episodes():
            if ep.title == ep2.title:
                if ep.isWatched and not ep2.isWatched:
                    ep2.markWatched()
                    i += 1
                elif ep2.isWatched and not ep.isWatched:
                    ep.markWatched()
                break
    print("Marked ", i ," episodes of ",show_name," watched")

#pool.map(showshowname, common_shows)
pool.map(checkshow, common_shows)
pool.close()
pool.join()
