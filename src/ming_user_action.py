#coding=utf8

from config import *
import datetime

class MingAction(object):
    def __init__(self, date="2016"):
        self.__click_map = {}
        self.__date = date
        pass

    def __getdateRange(self, days=7):
        d11 = self.__date + "1111"
        d1 = datetime.datetime.strptime(d11, "%Y%m%d")
        return [(d1 - datetime.timedelta(days = day)).strftime("%Y%m%d") for day in range(1, days + 1)]

    def __append(self, user, item, date):
        if user not in self.__click_map:
            self.__click_map[user] = {}
        if date not in self.__click_map[user]:
            self.__click_map[user][date] = []
        self.__click_map[user][date].append(item)

    def mining_browsing(self, days=7):
        datelist = self.__getdateRange(days)
        for filename in eval("BROWSING_" + self.__date):
            with open(filename) as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[3] not in datelist or len(items[1]) <= 0 or len(items[2]) <= 0 or len(items[0]) <= 0:
                        continue
                    user = items[2]
                    item = items[1]
                    ds = int(items[3])
                    self.__append(user, item, ds)

    def mining_collect(self, days=7):
        datelist = self.__getdateRange(days)
        with open(eval('COLLECTION_' + self.__date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                user = items[0]
                item = items[2]
                ds = items[4]
                if ds not in datelist or len(ds) <= 0 or len(user) <= 0 or len(item) <= 0:
                    continue
                self.__append(user, item, int(ds))

    def mining_cart(self, days=7):
        datelist = self.__getdateRange(days)
        for filename in eval("CARTING_" + self.__date):
            with open(filename) as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    user = items[3]
                    item = items[1]
                    ds = items[8]
                    dt = items[6]
                    if ds not in datelist or len(ds) <= 0 or len(user) <= 0 or len(item) <= 0 or len(dt) > 0:
                        continue
                    self.__append(user, item, int(ds))

    def cal_action(self, outfile):
        with open(outfile, 'w') as outf:
            for user, click_map in self.__click_map.iteritems():
                clicks_list = []
                for date, clicks in sorted(click_map.iteritems()):
                     clicks_list.extend(clicks)
                outf.write(('%s\t%s\n' % (user, ' '.join(clicks_list))).encode('utf8'))

if __name__ == "__main__":
    date = "2016"
    ma = MingAction(date)
    ma.mining_cart(5)
    ma.mining_collect(5)
    ma.mining_browsing(5)
    ma.cal_action(eval('ACTION_CLICK_' + date))



