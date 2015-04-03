# -*- coding: UTF-8 -*-
import sys       # working for arguments
import slacker
import time
from msg import Msg
import codecs    # File I/O with UTF-8


token = 'xoxp-2734280152-4137412349-4279772753-169911'
slack = slacker.Slacker(token)
channel = 'random'
#filename = '{}_backup_{:%Y%m%d}'.format(channel,date)
filename = 'backup.txt'
output_file = codecs.open(filename, "w", "utf-8-sig")
cnt = 0

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
response = slack.channels.history(_id, count = 1000)
if response.body['messages']:
    print('Message Exists. {0} message(s) found.'.format(len(response.body['messages'])))
ts = 0
dic = make_user_dict();
flag = True
l = []

# Reading File History
while(response.body['has_more'] == True):
    last_user = '';
    for msg in response.body['messages']:
        if 'subtype' in msg:
            l.append(Msg(msg.get('user'), msg['ts'], msg['text'], msg['subtype']))
        else:
            l.append(Msg(msg['user'], msg['ts'], msg['text']))
        ts = msg['ts']

    if flag:
        response = slack.channels.history(_id, latest = ts, count = 1)   #  2ch 1001 RULE
        flag = False
    else:
        # Output
        #print ('Len of l', len(l))
        l.reverse()
        for msg in l:
            if msg.user not in dic:
                dic[msg.user] = msg.user
            cnt = cnt + 1
            output_file.write(str(cnt) + '名前: {0} : {1} ID:{2} \n'.format(dic[msg.user], time.strftime("%Y/%m/%d %a %H:%M:%S", time.localtime(float(msg.ts))), msg.user))
            output_file.write('\t' + msg.getTextAs2CH() + '\n')
        l = []

        response = slack.channels.history(_id, latest = ts, count = 1000)
        flag = True
    #print('Latest Timestamp:', ts)
else:
    for msg in response.body['messages']:
        if 'subtype' in msg:
            pass
            #l.append(Msg(msg['user'], msg['ts'], msg['text'], msg['subtype']))
        else:
            l.append(Msg(msg['user'], msg['ts'], msg['text']))
    if l:
        l.reverse()
        for msg in l:
            if msg.user not in dic:
                dic[msg.user] = msg.user
            output_file.write('名前: {0} : {1} ID:{2}'.format(dic[msg.user], time.strftime("%Y/%m/%d %a %H:%M:%S", time.localtime(float(msg.ts))), msg.user) + '\n')
            output_file.write('\t' + msg.getTextAs2CH() + '\n')
            #msg.print(dic)
        l = []

output_file.close()
