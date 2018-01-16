
from config import *
from preprocess import PreProcess
import matplotlib.pyplot as plt
import datetime

class StaticByDay(object):
    def __init__(self):
        pass

    def calc_browser_data(self, userset, date="2016"):
        self.__browser_day_map = {}
        for filename in eval("BROWSING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[2] not in userset or len(items[3]) <= 0:
                        continue
                    self.__browser_day_map[int(items[3])] = self.__browser_day_map.get(int(items[3]), 0) + 1
        self.__browser_day_map = sorted(self.__browser_day_map.iteritems(), key=lambda x: x[0])
        print self.__browser_day_map

    def cal_collect_data(self, userset, date="2016"):
        self.__collect_day_map = {}
        with open(eval("COLLECTION_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[0] not in userset or len(items[4]) <= 0:
                    continue
                self.__collect_day_map[int(items[4])] = self.__collect_day_map.get(int(items[4]), 0) + 1
        self.__collect_day_map =  sorted(self.__collect_day_map.iteritems(), key=lambda x: x[0])
        print self.__collect_day_map

    def cal_cart_data(self, userset, date="2016"):
        self.__cart_day_map = {}
        for filename in eval("CARTING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[3] not in userset or len(items[8]) <= 0:
                        continue
                    self.__cart_day_map[int(items[8])] = self.__cart_day_map.get(int(items[8]), 0) + 1
        self.__cart_day_map =  sorted(self.__cart_day_map.iteritems(), key=lambda x: x[0])
        print self.__cart_day_map

    def cal_purchase_data(self, userset, date='2016'):
        self.__purchase_day_map = {}
        for filename in eval("PURCHASING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[10] not in userset or len(items[13]) <= 0:
                        continue
                    self.__purchase_day_map[int(items[13])] = self.__purchase_day_map.get(int(items[13]), 0) + 1
        self.__purchase_day_map = sorted(self.__purchase_day_map.iteritems(), key=lambda x: x[0])
        print self.__purchase_day_map

    def get_dis(self, date):
        a = datetime.datetime.strptime("20160810", "%Y%m%d")
        b = datetime.datetime.strptime(str(date), "%Y%m%d")
        return (b - a).days

    def display(self):
        plt.figure()
        ax1 = plt.subplot(4, 1, 1)
        ax2 = plt.subplot(4, 1, 2)
        ax3 = plt.subplot(4, 1, 3)
        ax4 = plt.subplot(4, 1, 4)
        plt.sca(ax1)
        plt.plot([self.get_dis(x[0]) for x in self.__purchase_day_map], [x[1] for x in self.__purchase_day_map])
        plt.sca(ax2)
        plt.plot([self.get_dis(x[0]) for x in self.__cart_day_map], [x[1] for x in self.__cart_day_map])
        plt.sca(ax3)
        plt.plot([self.get_dis(x[0]) for x in self.__collect_day_map], [x[1] for x in self.__collect_day_map])
        plt.sca(ax4)
        plt.plot([self.get_dis(x[0]) for x in self.__browser_day_map], [x[1] for x in self.__browser_day_map])
        plt.show()


if __name__ == '__main__':
    std = StaticByDay()
    userset = PreProcess().get_user_set(PROMOTION_CONSUMPTION_LAST2YEARS_2016)
    std.cal_cart_data(userset, '2017')
    std.cal_purchase_data(userset, '2017')
    std.cal_collect_data(userset, '2017')
    std.calc_browser_data(userset, '2017')
    std.display()



