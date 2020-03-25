#!/usr/bin/env python3
# *-* coding:utf-8 *-*

import getpass
from plexapi.myplex import PlexServer
from plexapi.myplex import MyPlexAccount
import multiprocessing.dummy
import argparse
import yaml

parser = argparse.ArgumentParser(description='Sync Watched Between 2 Servers')
parser.add_argument('-s1', '--server1', help='Server 1 Name from Plex', required=True)
parser.add_argument('-s2', '--server2', help='Server 2 Name from Plex', required=True)
parser.add_argument('-u', '--username', help='Username for Plex')
parser.add_argument('-t', '--token', help='Token for plex')
# parser.add_argument('-p', '--password', help='Password for Plex')
# parser.add_argument('-pf', '--file', help='Password for Plex in file')


args = parser.parse_args()

print("Server1: {}".format(args.server1))
print("Server2: {}".format(args.server2))

if args.username:
    username = args.username
    password = getpass.getpass(prompt='Password: ')
    account = MyPlexAccount(username, password)
    server_1_name = args.server1
    server_2_name = args.server2
    server_1 = account.resource(server_1_name)
    server_2 = account.resource(server_2_name)
    print('Connecting....')

    conn_1 = server_1.connect()
    conn_2 = server_2.connect()
    print('Conncted to ', server_1_name, server_2_name)


elif args.token:
    conn_1 = PlexServer(args.server1,args.token)
    conn_2 = PlexServer(args.server2,args.token)

else:
    print('plexsync.py --help')



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
    s1set = set()
    s2set = set()
    allshows += 1
    for ep1 in conn_1.library.section('TV Shows').get(shows).watched():
        s1set.add(str(ep1.parentIndex) + ':' + str(ep1.index))

    for ep2 in conn_2.library.section('TV Shows').get(shows).watched():
        s2set.add(str(ep2.parentIndex) + ':' + str(ep2.index))
    '''
    with open('watched1.yml', 'a+') as f:
        yaml.dump(serverdict['s1'], f, default_flow_style=False)
    with open('watched2.yml', 'a+') as g:
        yaml.dump(serverdict['s2'], g, default_flow_style=False)
    '''

    set1diff = s1set.difference(s2set)
    set2diff = s2set.difference(s1set)
    s1 = 0
    s2 = 0

    if len(set1diff) > 0:
        for i in set1diff:
            a = i.partition(':')
            try:
                conn_2.library.section('TV Shows').get(shows).episode(title=None, season=int(a[0]),
                                                                      episode=int(a[2])).markWatched()
                s2 += 1
            except:
                print('ERROR--Can\'t mark:{} watched'.format(shows + ' ' + i))
                continue
    else:
        pass
    if len(set2diff) > 0:
        for i2 in set2diff:
            a2 = i2.partition(':')
            try:
                conn_1.library.section('TV Shows').get(shows).episode(title=None, season=int(a2[0]),
                                                                      episode=int(a2[2])).markWatched()
            except:
                print('ERROR--Can\'t mark:{} watched'.format(shows + ' ' + i2))
                continue
    else:
        pass
    if s1 or s2 > 0:
        print("\nMarked {} episodes of {} watched on {}".format(s1,shows,args.server1))
        print("Marked {} episodes of {} watched on {}".format(s2,shows,args.server2))
    else:
        pass

if __name__ == "__main__":
    #for i in common_shows:
    #    getwatched(i)
    pool = multiprocessing.dummy.Pool(30)
    pool.map(getwatched, common_shows)
    pool.close()
print('\nChecked ', allshows, 'shows with', allepisodess1, 'episodes on', args.server1, 'and', allepisodess2, 'episodes on', args.server2)
