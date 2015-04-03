import time
class Msg:
    def __init__(self, user, ts, text, subtype = 0):
        self.user = user
        self.ts = ts
        self.text = text
        self.subtype = subtype
    def getTextAs2CH(self):
        return self.text.replace('\n', '\n\t')
    def print(self, dic):
        print('名前: {0} : {1} ID:{2}'.format(dic[self.user], time.strftime("%Y/%m/%d %a %H:%M:%S", time.localtime(float(self.ts))), self.user))
        print('\t' + self.getTextAs2CH())
