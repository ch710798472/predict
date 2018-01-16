#coding=utf8

import sys
from config import *
import datetime
import math

class Features(object):
    def __init__(self):
        self.__features = {}
        # self.__date = "2016"
        self.__date = "2017"
        pass
    def get_gender(self,str):
        if str == 'M':
            return 2.0
        elif str == 'F':
            return 1.0
        else:
            return 0.0
    def get_suspended(self,str):
        if str != '0':
            return 2.0
        elif str == '1':
            return 1.0
        else:
            return 0.0
    def __inrange_date(self, date, range=7):
        d11 = self.__date + '1111'
        d1 = datetime.datetime.strptime(date, "%Y%m%d")
        d2 = datetime.datetime.strptime(d11, "%Y%m%d")
        if (d2 - d1).days <= range:
            return True
        return False

    def __getdateRange(self, days=7):
        d11 = self.__date + "1111"
        d1 = datetime.datetime.strptime(d11, "%Y%m%d")
        return [(d1 - datetime.timedelta(days = day)).strftime("%Y%m%d") for day in range(1, days + 1)]

    def __getPresaleDateRange(self, days=70):
        d11 = self.__date + "1020"
        d1 = datetime.datetime.strptime(d11, "%Y%m%d")
        return [(d1 - datetime.timedelta(days = day)).strftime("%Y%m%d") for day in range(1, days + 1)]

    def extract_user(self, date="2016"):
        with open(eval("USER_" + date), "r") as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]] = []

    def extract_y(self, date="2016"):
        with open(D11_CONSUMPTION_2016, "r") as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(items[1])

    def extract_feature_before(self, date='2016'):
        if date == '2016':
            with open(eval("FEATURE_FILE_BEFORE"), 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    user = items[0]
                    # 去掉test_y
                    for item in items[1:-1]:
                        self.__features[user].append(item)
        else:
            with open(eval("REAL_TEST_FILE_BEFORE"), 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    user = items[0]
                    for item in items[1:]:
                        self.__features[user].append(item)

        print >> sys.stderr, 'extract feature before done!'

    def extract_purser_gmv_gate(self, date="2016", range=7, gate=100000.0):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        for filename in eval("PURCHASING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[13] not in datelist:
                        continue
                    # gmv_map[items[10]] = gmv_map.get(items[10], 0) + float(items[7]) * float(items[1])
                    gmv_map[items[10]] = gmv_map.get(items[10], 0) + float(items[4])
        gate_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if float(items[2]) < gate:
                        pass
                    gate_price[items[0]] = gmv_map.get(items[0], 0)
        for user, fea in self.__features.iteritems():
            if user not in gmv_map or user not in gate_price:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(gate_price[user])
        print >> sys.stderr, 'extract purchase gmv gate done!'
        pass


    def extract_cart_gmv_gate(self, date="2016", range=7, gate=100000.0):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        for filename in eval("CARTING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[8] not in datelist:
                        continue
                    if items[3] not in gmv_map:
                        gmv_map[items[3]] = []
                    gmv_map[items[3]].append((items[1], int(items[2])))
        item_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if float(items[2]) < gate:
                        pass
                    item_price[items[0]] = items[3]
        user_gmv = {}
        for user, items in gmv_map.iteritems():
            total = 0
            for item, quantity in items:
                if item in item_price:
                    total += float(item_price[item]) * quantity
            user_gmv[user] = total
        for user, fea in self.__features.iteritems():
            if user not in user_gmv:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(user_gmv[user])
        print >> sys.stderr, 'extract cart gmv gate done!'
        pass


    def extract_collect_gmv_gate(self, date="2016", range=7, gate=100000.0):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        with open(eval("COLLECTION_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[4] not in datelist:
                    continue
                if items[0] not in gmv_map:
                    gmv_map[items[0]] = []
                gmv_map[items[0]].append(items[2])
        item_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if float(items[2]) < gate:
                        pass
                    item_price[items[0]] = items[3]
        user_gmv = {}
        for user, items in gmv_map.iteritems():
            total = 0
            for item in items:
                if item in item_price:
                    total += float(item_price[item])
            user_gmv[user] = total
        for user, fea in self.__features.iteritems():
            if user not in user_gmv:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(user_gmv[user])
        print >> sys.stderr, 'extract col gmv gate done!'
        pass


    def extract_click_fea_split(self, input, date="2016"):
        user_map = {}
        with open(input, 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split('\t')
                user = items[0]
                clicks = items[1].split(' ')
                item_score = {}
                N = len(clicks)
                if N <= 0:
                    continue
                for index, item in enumerate(clicks):
                    item_score[item] = item_score.get(item, 0.0) + math.exp(-1.0 * (N - index - 1) / N)
                item_score = sorted(item_score.iteritems(), key=lambda x:x[1], reverse=True)
                user_map[user] = item_score[:2]
        item_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    item_price[items[0]] = float(items[3])
        user_gmv = {}
        for user, items in user_map.iteritems():
            total = 0
            for item, score in items:
                total += score
            gmv = 0
            for item, score in items:
                if item not in item_price:
                    continue
                gmv += score / total * item_price[item]
            user_gmv[user] = gmv
        for user, fea in self.__features.iteritems():
            if user not in user_gmv:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(user_gmv[user])
        print >> sys.stderr, 'extract click fea spilt done!'

    def extract_click_fea_split_main(self, date='2016'):
        cart_5 = eval('ACTION_CLICK_CART_5_' + date)
        cart_10 = eval('ACTION_CLICK_CART_10_' + date)
        cart_20 = eval('ACTION_CLICK_CART_20_' + date)
        collect_5 = eval('ACTION_CLICK_COLLECT_5_' + date)
        collect_10 = eval('ACTION_CLICK_COLLECT_10_' + date)
        collect_20 = eval('ACTION_CLICK_COLLECT_20_' + date)
        browsing_5 = eval('ACTION_CLICK_BROWSING_5_' + date)
        browsing_10 = eval('ACTION_CLICK_BROWSING_10_' + date)
        browsing_20 = eval('ACTION_CLICK_BROWSING_20_' + date)
        cart_collect_5 = eval('ACTION_CLICK_COLLECT_AND_CART_5_' + date)
        cart_collect_10 = eval('ACTION_CLICK_COLLECT_AND_CART_10_' + date)
        cart_collect_20 = eval('ACTION_CLICK_COLLECT_AND_CART_20_' + date)
        self.extract_click_fea_split(cart_5, date)
        self.extract_click_fea_split(cart_10, date)
        self.extract_click_fea_split(cart_20, date)
        self.extract_click_fea_split(collect_5, date)
        self.extract_click_fea_split(collect_10, date)
        self.extract_click_fea_split(collect_20, date)
        self.extract_click_fea_split(browsing_5, date)
        self.extract_click_fea_split(browsing_10, date)
        self.extract_click_fea_split(browsing_20, date)
        self.extract_click_fea_split(cart_collect_5, date)
        self.extract_click_fea_split(cart_collect_10, date)
        self.extract_click_fea_split(cart_collect_20, date)

    def save(self, filename=FEATURE_FILE):
        with open(filename, 'w') as outfile:
            for userid, feature in self.__features.iteritems():
                fea_str = [str(fea) for fea in feature]
                outfile.write(('%s,%s\n' % (userid, ','.join(fea_str))).encode('utf8'))

    def extract(self):
        date = self.__date
        self.extract_user(date)
        self.extract_feature_before(date)
        self.extract_click_fea_split_main(date)
        # gmv热点商品统计在before中无需再加
        # self.extract_purser_gmv_gate(date, 1, 50000.0)
        # self.extract_purser_gmv_gate(date, 1, 10000.0)
        #
        # self.extract_purser_gmv_gate(date, 3, 50000.0)
        # self.extract_purser_gmv_gate(date, 3, 10000.0)
        #
        # self.extract_purser_gmv_gate(date, 7, 50000.0)
        # self.extract_purser_gmv_gate(date, 7, 10000.0)
        #
        # self.extract_cart_gmv_gate(date, 1, 50000.0)
        # self.extract_cart_gmv_gate(date, 1, 10000.0)
        #
        # self.extract_cart_gmv_gate(date, 3, 50000.0)
        # self.extract_cart_gmv_gate(date, 3, 10000.0)
        #
        # self.extract_cart_gmv_gate(date, 7, 50000.0)
        # self.extract_cart_gmv_gate(date, 7, 10000.0)
        #
        # self.extract_collect_gmv_gate(date, 1, 50000.0)
        # self.extract_collect_gmv_gate(date, 1, 10000.0)
        #
        # self.extract_collect_gmv_gate(date, 3, 50000.0)
        # self.extract_collect_gmv_gate(date, 3, 10000.0)
        #
        # self.extract_collect_gmv_gate(date, 7, 50000.0)
        # self.extract_collect_gmv_gate(date, 7, 10000.0)


        # 2016
        # self.extract_y(date)
        # self.save()
        # 2017
        self.save(REAL_TEST_FILE)

if __name__ == '__main__':
    Features().extract()
