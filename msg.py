import time
import re       # Regular Expression


class Msg:
    def __init__(self, user, ts, text, subtype=0, **kwargs):
        self.user = user
        self.ts = ts
        self.text = text
        self.subtype = subtype
        if subtype == 'message_changed':
            self.edit_user = kwargs['edit_user']
            self.edit_ts = kwargs['edit_ts']

    def getTextAs2CH(self, dic):
        self.text = re.sub('<@([A-Z0-9]+)>',
                           lambda x: '{}'.format(dic[x.group(1)]), self.text)
        return self.text.replace('\n', '\n\t')

    def writeToFile(self, out, dic, cnt):
        out.write(str(cnt) + ' 名前: {0} : {1} ID:{2}\n'.format(
                  dic[self.user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                                time.localtime(float(self.ts))), self.user))

        if self.subtype == 'bot_message':
            out.write(str(cnt) + ' BOT名前: {0} : {1} ID:{2}\n'.format(
                     dic[self.user],
                      time.strftime("%Y/%m/%d %a %H:%M:%S",
                      time.localtime(float(self.ts))), self.user))
            out.write('\t' + self.getTextAs2CH(dic) + '\n')
        elif self.subtype == 'me_message':
            out.write('Type: /me message')
            out.write('\t' + self.getTextAs2CH(dic) + '\n')
        elif self.subtype == 'message_changed':
            out.write('\t' + self.getTextAs2CH(dic) + '\n')
            out.write('Edited by {0} at {1}\n'.format(dic[self.edit_user],
                      time.strftime("%Y/%m/%d %a %H:%M:%S",
                      time.localtime(float(self.edit_ts)))))
        else:
            out.write('\t' + self.getTextAs2CH(dic) + '\n')

    def print_(self, dic, cnt):
        if self.subtype == 'bot_message':
            print(str(cnt) + ' BOT名前: {0} : {1} ID:{2}\n'.format(
                  dic[self.user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                                time.localtime(float(self.ts))), self.user))
            print('\t' + self.getTextAs2CH(dic) + '\n')
        elif self.subtype == 'me_message':
            print(str(cnt) + ' 名前: {0} : {1} ID:{2}\n'.format(dic[self.user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                  time.localtime(float(self.ts))), self.user) +
                  'Type: /me message')
            print('\t' + self.getTextAs2CH(dic) + '\n')
        elif self.subtype == 'message_changed':
            print(str(cnt) + ' 名前: {0} : {1} ID:{2}\n'.format(dic[self.user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                  time.localtime(float(self.ts))), self.user) +
                  'Type: /me message')
            print('\t' + self.getTextAs2CH(dic) + '\n')
            print('Edited by {0} at {1}\n'.format(
                  dic[self.edit_user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                                time.localtime(float(self.edit_ts)))))
        else:
            print(str(cnt) + ' 名前: {0} : {1} ID:{2}\n'.format(dic[self.user],
                  time.strftime("%Y/%m/%d %a %H:%M:%S",
                  time.localtime(float(self.ts))), self.user))
            print('\t' + self.getTextAs2CH(dic) + '\n')
