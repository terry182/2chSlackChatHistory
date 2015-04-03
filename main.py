# -*- coding: UTF-8 -*-
import sys       # working for arguments
import slacker
from msg import Msg
import datetime
import codecs    # File I/O with UTF-8


token = 'xoxp-2734280152-4137412349-4279772753-169911'
slack = slacker.Slacker(token)
date = datetime.datetime.now()
channel = 'general'
#filename = '{}_backup_{:%Y%m%d}'.format(channel,date)
filename = 'backup.txt'

def make_user_dict():
    l = slack.users.list()
    dic = {}
    for user in l.body['members']:
        dic[user['id']] = user['name']
    return dic


# Getting Channel ID
re = slack.channels.list()
_id = 0
for chan in re.body['channels']:
    if (chan['name'] == channel):
        _id = chan['id']

print('id = {}'.format(_id))

# Getting History
response = slack.channels.history(_id, count = 10)
ts = 0
dic = make_user_dict();
flag = True
l = []

# Reading File History
while(response.body['has_more'] == True):
    last_user = '';
    for msg in response.body['messages']:
        if 'subtype' in msg:
            l.append(Msg(msg['user'], msg['ts'], msg['text'], msg['subtype']))
        else:
            l.append(Msg(msg['user'], msg['ts'], msg['text']))
        ts = msg['ts']

    #if flag:
    #    response = slack.channels.history(_id, count = 1)   #  2ch 1001 RULE
    #    flag = False
    #else:
    #    response = slack.channel.history(_id, count = 1000)
    #    flag = True
    print('Latest Timestamp:', ts)
    break
#else:
#    for msg in response.body['messages']:
#        if 'subtype' in msg:
#            Msg.l.append(Msg(msg['user'], msg['ts'], msg['text'], msg['subtype']))
#        else:
#            Msg.l.append(Msg(msg['user'], msg['ts'], msg['text']))

print ('Len of l', len(l))
l.reverse()
for msg in l:
    msg.print(dic)
l.c

# Output
#output_file = codecs.open(filename, "w", "utf-8-sig")
#cnt = 0


#output_file.close()

