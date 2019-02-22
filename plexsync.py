#!/usr/bin/python3

import getpass
from plexapi.myplex import MyPlexAccount
import multiprocessing.dummy
username = input('Username: ')
password = getpass.getpass(prompt ='Password: ')
account = MyPlexAccount(username, password)

server_1_name = 'Hades'
server_2_name = 'Hades-Rack'
server_1 = account.resource(server_1_name)
server_2 = account.resource(server_2_name)
print('Connecting....')
conn_1 = server_1.connect()
conn_2 = server_2.connect()
print('Conncted to ',server_1_name,server_2_name)
allepisodess1 = 0
allepisodess2 = 0
allshows = 0

server_1_shows = set(list(map((lambda x: x.title), conn_1.library.section('TV Shows').search())))
server_2_shows = set(list(map((lambda x: x.title), conn_2.library.section('TV Shows').search())))

common_shows = server_1_shows & server_2_shows

def getwatched(shows):
    global allshows
    global allepisodess1
    global allepisodess2
    serverdict = {'s1':{}, 's2': {}}
    s1set = set()
    s2set = set()
    allshows += 1
    for ep in conn_1.library.section('TV Shows').get(shows).episodes():
        allepisodess1 += 1
        strep = str(ep).split(':')[2]
        serverdict['s1'][strep] = ep.title
        if ep.isWatched == True:
            s1set.add(strep)
        else:
            continue
    for ep2 in conn_2.library.section('TV Shows').get(shows).episodes():
        allepisodess2 += 1
        strep2 = str(ep2).split(':')[2]
        serverdict['s2'][strep2] = ep2.title
        if ep2.isWatched == True:
            s2set.add(strep2)
        else:
            continue
    set1diff = s1set.difference(s2set)
    set2diff = s2set.difference(s1set)
    s1 = 0
    s2 = 0
    if len(set1diff) > 0:
        for sdiff1 in set1diff:
            conn_2.library.section('TV Shows').get(shows).get(serverdict['s2'][sdiff1]).markWatched()
            s2 += 1
    else:
        pass
    if len(set2diff) > 0:
        for sdiff2 in set2diff:
            conn_1.library.section('TV Shows').get(shows).get(serverdict['s1'][sdiff2]).markWatched()
            s1 += 1
    else:
        pass
    print("Marked", s1 ,"episodes of",shows,"watched on",server_1_name)
    print("Marked", s2 ,"episodes of",shows,"watched on",server_2_name)

if __name__ == "__main__":
    pool = multiprocessing.dummy.Pool(10)
    pool.map(getwatched, common_shows)
    pool.close()
print('Checked ',allshows, 'shows with',allepisodess1,'episodes on',server_1_name,'and',allepisodess2,'episodes on',server_2_name)
