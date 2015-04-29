# -*- coding: UTF-8 -*-
import slacker
import time
from msg import Msg
import codecs  # File I/O with UTF-8


# User-defined Arguments
token = 'your-token'
slack = slacker.Slacker(token)
channel = 'general'
CurrentTime = time.strftime("%Y%m%d", time.localtime(float(time.time())))
filename = '{0}_backup_{1}'.format(channel, CurrentTime)
# filename = 'backup.txt'
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


def MessageReading(msg, msgList, UserDic):
    if 'subtype' not in msg:
        msgList.append(Msg(msg['user'], msg['ts'], msg['text']))
    subtype = msg.get('subtype', None)
    if subtype == 'bot_message':
        print('Bot message Exists.')
        UserDic[msg['bot_id']] = msg['user_name']
        msgList.append(Msg(msg['bot_id'], msg['ts'],
                           msg['text'], msg['subtype']))
    elif subtype == 'me_message':
        msgList.append(Msg(msg['user'], msg['ts'],
                           msg['text'], msg['subtype']))
    elif subtype == 'message_changed':
        msgList.append(Msg(msg['user'], msg['ts'], msg['text'],
                       msg['subtype'], edit_user=msg['edited']['user'],
                       edit_ts=msg['edited']['ts']))
    elif subtype == 'message_deleted':
        msgList.append(Msg(msg['user'], msg['ts'],
                       'Message deleted at {}'.format(
                       time.strftime("%Y/%m/%d %a %H:%M:%S",
                                     time.localtime(float(msg['deleted_ts'])))
                                     )))
    elif subtype == 'channel_join':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has joined the channel'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'channel_leave':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has left the channel'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'channel_topic':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} set the channel purpose to: {}'.format(
                            dic[msg['user']], msg['topic']
                            ), msg['subtype']))
    elif subtype == 'channel_purpose':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} set the channel topic: {}'.format(
                            dic[msg['user']], msg['purpose']
                            ), msg['subtype']))
    elif subtype == 'channel_name':
        pass
    elif subtype == 'channel_archive':
        # untested
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has archived the channel'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'channel_unarchive':
        # untested
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has unarchived the channel'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'group_join':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has joined the group'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'group_leave':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} has left the group'.format(
                            dic[msg['user']]
                            ), msg['subtype']))
    elif subtype == 'group_topic':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} set the group topic to: {}'.format(
                            dic[msg['user']], msg['topic']
                            ), msg['subtype']))
    elif subtype == 'group_purpose':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} set the group purpose to: {}'.format(
                            dic[msg['user']], msg['purpose']
                            ), msg['subtype']))
    elif subtype == 'group_name':
        pass
    elif subtype == 'group_archive':
        pass
    elif subtype == 'group_unarchive':
        pass
    elif subtype == 'file_share':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} shared a file: {}'.format(
                            dic[msg['user']], msg['file']['url']
                            ), msg['subtype']))
    elif subtype == 'file_comment':
        pass
    elif subtype == 'file_mention':
        pass
    elif subtype == 'pinned_item':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} pinned their post: {}'.format(
                            dic[msg['user']], msg['item']['url']
                            ), msg['subtype']))
    elif subtype == 'unpinned_item':
        msgList.append(Msg(msg['user'], msg['ts'],
                           '{} unpinned their post: {}'.format(
                            dic[msg['user']], msg['item']['url']
                            ), msg['subtype']))
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
    print('Message Exists. {0} message(s) found.'.format(
                                        len(response.body['messages'])))
else:
    print('No message exists.')

ts = 0
file_count = 0
dic = make_user_dict()
l = []

# Reading File History
while response.body['has_more'] is True:
    for msg in response.body['messages']:
        MessageReading(msg, l, dic)
        ts = msg['ts']
    # Output
    print('Len of l', len(l))
    l.reverse()
    for msg in l:
        if msg.user not in dic:
            dic[msg.user] = msg.user
        cnt = cnt + 1
        msg.writeToFile(output_file, dic, cnt)
    out_1001(output_file)
    l = []

    response = slack.channels.history(_id, latest=ts, count=1000)
    print('File {} Latest Timestamp:'.format(file_count), ts)
    file_count = file_count + 1
    output_file.close()
    output_file = codecs.open('{}_{}'.format(filename, file_count),
                              "w", "utf-8-sig")

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
