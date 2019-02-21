#!/usr/bin/python3

import getpass
from plexapi.myplex import MyPlexAccount
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(4)
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

#server_1_shows = set(list(map((lambda x: x.title), conn_1.library.section('TV Shows').search())))
#server_2_shows = set(list(map((lambda x: x.title), conn_2.library.section('TV Shows').search())))

#common_shows = server_1_shows & server_2_shows
common_shows = ['Ash vs Evil Dead']
#common_shows = ['Ash vs Evil Dead','Disenchantment', 'Justified', 'This Is Us', "Marvel's Iron Fist"]


def getwatched(watched):
    serverdict = {'s1':{}, 's2': {}}
    s1set = set()
    s2set = set()
    for ep in conn_1.library.section('TV Shows').get(watched).episodes():
        if ep.isWatched == True:
            strep = str(ep).split(':')[2]
            s1set.add(strep)
            serverdict['s1'][strep] = ep.title
        else:
            continue

    for ep2 in conn_2.library.section('TV Shows').get(watched).episodes():
        if ep2.isWatched == True:
            strep2 = str(ep2).split(':')[2]
            s2set.add(strep2)
            serverdict['s2'][strep] = ep2.title
            strep = str(ep2)
            serverdict['s2'][strep] = ep2.title
        else:
            continue
    set1diff = s1set.difference(s2set)
    set2diff = s2set.difference(s1set)
    print(len(set1diff))
    print(len(set2diff))
    print(set1diff)
    for i in serverdict['s1'][set1diff]:
        print(i)


def getepisodes(shownames):
    global allshows
    global allepisodess1
    global allepisodess2
    s1set = set()
    s2set = set()
    allshows += 1
    for ep in conn_1.library.section('TV Shows').get(shownames).episodes():
        allepisodess1 += 1
        if ep.isWatched == True:
            s1set.add(ep.title)
        else:
            continue
    for ep2 in conn_2.library.section('TV Shows').get(shownames).episodes():
        allepisodess2 += 1
        if ep2.isWatched == True:
            s2set.add(ep2.title)
        else:
            continue
    #print(s1set)
    #print(s2set)
    set1diff = s1set.difference(s2set)
    set2diff = s2set.difference(s1set)
    #print(set1diff)
    #print(set2diff)
    i = 0
    p = 0
    for s1show in set1diff:
        try:
            conn_2.library.section('TV Shows').get(shownames).get(s1show).markWatched()
            i += 1
        except:
            print('The show does not exist on both servers', shownames,"-",s1show)
            continue
    for s2show in set2diff:
        try:
            conn_1.library.section('TV Shows').get(shownames).get(s2show).markWatched()
            p += 1
        except:
            print('The show does not exist on both servers', shownames,"-",s2show)
            continue

    print("Marked", p ,"episodes of",shownames,"watched on",server_1_name)
    print("Marked", i ,"episodes of",shownames,"watched on",server_2_name)

pool.map(getwatched, common_shows)
#pool.map(getepisodes, common_shows)
pool.close()
#pool.close()
#print('Checked ',allshows, 'shows with',allepisodess1,'episodes on',server_1_name,'and',allepisodess2,'episodes on',server_2_name)
