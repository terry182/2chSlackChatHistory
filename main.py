# -*- coding: UTF-8 -*-
import sys       # working for arguments
import slacker
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
output_file = codecs.open(filename, "w", "utf-8-sig")


while(response.body['has_more'] == True):
    last_user = '';
    for msg in response.body['messages']:
        if msg['type'] == 'message':
            if 'subtype' in msg:
                if msg['subtype'] == "file_share":
                    output_file.write(msg['text'] + '\n')
                else:
                    print('Subtype exists. Pass this line for later edit.')
            else:
                if msg['user'] != last_user:
                    last_user = msg['user']
                    output_file.write(dic[msg['user']] + ': \n')
                output_file.write('\t' + msg['text'] + '\n')
                ts = msg['ts']
    print('Latest Timestamp:', ts)
    break

output_file.close()

