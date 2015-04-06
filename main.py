# -*- coding: UTF-8 -*-
import slacker
from msg import Msg
import codecs  # File I/O with UTF-8

# User-defined Arguments
token = 'xoxp-2734280152-4137412349-4293823360-a7d3bf'
slack = slacker.Slacker(token)
channel = 'general'
# filename = '{}_backup_{:%Y%m%d}'.format(channel,date)
filename = 'backup.txt'
# end of the arguments

output_file = codecs.open(filename, "w", "utf-8-sig")
cnt = 0
# Real 2ch 1001 rule
_str1001 = '''
　　　　　　　　　　　　　　　　　　　　　　γ
　　　　　　　　　　　　　　　　　　　　　　（
　　　　　　　　　　　　　　　　　　　　　 _ノ

　　　　　　　　　　　　　　　　　　　／
　　　　　　　　　　　　　　　 ＿＿
　　　　　　　　　　　　　,､'" 　 ．　 `' ､
　　　　　　　　　　　　　i`ｰ　　_　　　　',
.　 　　　　　　　　　　　l|　!|　 　 　 i""!|
　 　 　 　　 　 　 　 　 }:　}ｉ　　　　|{ 　!ｊ
　 　 　 　 　 　　　　　〈| 'Ｊ　|!　　 }ｊ 　:｝
　　　　　　　　　　　　_ﾉ;し　 i｝　 ｛J　 |
　　　　　　　　　,､-,､'　　　　　　　　　ハ- ､
　　　　　　　 　（ .(　'､＿　　　 _ ,ノ　 ﾉ:i 　 ）
　　　　　　　　,､'""`ｰ---‐'"ﾌ､_　- _,､' -'"
　　　　　　　 （　　＿　　 ,､'"　　 ￣
　　　　　　　　 `ー--─'"
千本目の蝋燭が消えますた・・・
新しい蝋燭を立ててくださいです・・・
'''


def make_user_dict():
    l = slack.users.list()
    dic = {'USLACKBOT': 'slackbot'}
    for user in l.body['members']:
        dic[user['id']] = user['name']
    return dic


def out_1001(output_file):
    output_file.write('1001 ：１００１：Over 1000 Thread \n')
    output_file.write(_str1001)


def MessageReading(message, MessageList, UserDic):
    if 'subtype' not in message:
        MessageList.append(Msg(message['user'], message['ts'], message['text']))
    elif message['subtype'] == 'bot_message':
        print('Bot message Exists.')
        UserDic[message['bot_id']] = message['user_name']
        MessageList.append(Msg(message['bot_id'], message['ts'], message['text'], message['subtype']))
    elif message['subtype'] == 'me_message':
        MessageList.append(Msg(message['user'], message['ts'], message['text'], message['subtype']))
    elif message['subtype'] == 'message_changed':
        MessageList.append(Msg(message['user'], message['ts'], message['text'], message['subtype'], edit_user=message['edited']['user'], edit_ts=message['edited']['ts']))
    else:
        pass

# Getting Channel ID
re = slack.channels.list()
_id = 0
for chan in re.body['channels']:
    if (chan['name'] == channel):
        _id = chan['id']

print('Channel id = {}'.format(_id))

# Getting History
response = slack.channels.history(_id, count=1000)
if response.body['messages']:
    print('Message Exists. {0} message(s) found.'.format(len(response.body['messages'])))
else:
    print('No message exists.')

ts = 0
dic = make_user_dict()
l = []

# Reading File History
while(response.body['has_more'] is True):
    last_user = ''
    for msg in response.body['messages']:
        if 'subtype' in msg:
            l.append(Msg(msg.get('user'), msg['ts'], msg['text'], msg['subtype']))
        else:
            l.append(Msg(msg['user'], msg['ts'], msg['text']))
        ts = msg['ts']

        # Output
        # print ('Len of l', len(l))
        l.reverse()
        for msg in l:
            if msg.user not in dic:
                dic[msg.user] = msg.user
            cnt = cnt + 1
            msg.writeToFile(output_file, dic, cnt)
        out_1001(output_file)
        l = []
        response = slack.channels.history(_id, latest=ts, count=1000)
        # print('Latest Timestamp:', ts)
else:
    for msg in response.body['messages']:
        MessageReading(msg, l, dic)
    if l:
        l.reverse()
        for msg in l:
            if msg.user not in dic:
                dic[msg.user] = msg.user
            cnt = cnt + 1
            msg.writeToFile(output_file, dic, cnt)
            # msg.print_(dic, cnt)

        if len(l) == 1000:
            out_1001(output_file)

        l = []

output_file.close()
