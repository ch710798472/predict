#coding=utf8

from config import *

class PreProcess(object):
    """
    过滤大促消费金额 == 0的数据
    """
    def __init__(self):
        pass

    def get_user_set(self, filename):
        users = set()
        with open(filename, 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if float(items[7]) <= 0.0 or float(items[8]) <= 0:
                    continue
                users.add(items[0])
        return users

    def filt_promotion_consumation(self, filename):
        with open(filename, 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if float(items[7]) <= 0.0 or float(items[8]) <= 0:
                    continue
                print ','.join(items)

if __name__ == "__main__":
    pp = PreProcess()
    pp.filt_promotion_consumation(PROMOTION_CONSUMPTION_LAST2YEARS_2016)

