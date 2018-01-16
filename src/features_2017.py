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

    def extract_promotation_comsume(self, date='2016'):
        with open(eval("PROMOTION_CONSUMPTION_LAST2YEARS_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[0] not in self.__features or (items[7] == 0 and items[8] == 0):
                    continue
                user = items[0]
                for item in items[1:]:
                    self.__features[user].append(item)
        print >> sys.stderr, 'extracr promation consume done!'

    def extract_purser_fea(self, date="2016", range=7):
        """提取双十一用户在双十一前7天，购买量"""
        datelist = self.__getdateRange(7)
        day7_purser_map = {}
        for filename in eval("PURCHASING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[13] not in datelist:
                        continue
                    day7_purser_map[items[10]] = day7_purser_map.get(items[10], 0) + 1
        for user, fea in self.__features.iteritems():
            if user not in day7_purser_map:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(day7_purser_map[user])
        print >> sys.stderr, 'extracr purser fea done!'



    def extract_purser_gmv(self, date="2016", range=7):
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
        for user, fea in self.__features.iteritems():
            if user not in gmv_map:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(gmv_map[user])
        print >> sys.stderr, 'extract purchase gmv done!'
        pass

    def extract_before_presale_purser_gmv(self, date="2016", range=20):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        for filename in eval("PURCHASING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[13] not in datelist and len(items[13]) > 0:
                        gmv_map[items[10]] = gmv_map.get(items[10], 0) + float(items[4])
                    # gmv_map[items[10]] = gmv_map.get(items[10], 0) + float(items[7]) * float(items[1])

        for user, fea in self.__features.iteritems():
            if user not in gmv_map:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(gmv_map[user])
        pass

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

    def extract_cart_fea(self, date="2016", range=7):
        """提取双十一用户在双十一前7天，加购量"""
        datelist = self.__getdateRange(range)
        day7_cart_map = {}
        for filename in eval("CARTING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[8] not in datelist:
                        continue
                    day7_cart_map[items[3]] = day7_cart_map.get(items[3], 0) + 1
        for user, fea in self.__features.iteritems():
            if user not in day7_cart_map:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(day7_cart_map[user])
        print >> sys.stderr, 'extracr cart fea done!'

    def extract_cart_gmv(self, date="2016", range=7):
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
        print >> sys.stderr, 'extract cart gmv done!'
        pass

    def extract_before_presale_cart_gmv(self, date="2016", range=20):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        for filename in eval("CARTING_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
                    if items[8] not in datelist and len(items[8]) > 0:
                        if items[3] not in gmv_map:
                            gmv_map[items[3]] = []
                        gmv_map[items[3]].append((items[1], int(items[2])))

        item_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
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

    def extract_collect_fea(self, date="2016", range=7):
        """提取双十一用户在双十一前7天，收藏量"""
        datelist = self.__getdateRange(range)
        day7_coll_map = {}
        with open(eval("COLLECTION_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[4] not in datelist:
                    continue
                day7_coll_map[items[0]] = day7_coll_map.get(items[0], 0) + 1
        for user, fea in self.__features.iteritems():
            if user not in day7_coll_map:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(day7_coll_map[user])
        print >> sys.stderr, 'extracr coll fea done!'

    def extract_collect_gmv(self, date="2016", range=7):
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
        print >> sys.stderr, 'extract col gmv done!'
        pass

    def extract_before_presale_collect_gmv(self, date="2016", range=20):
        datelist = self.__getdateRange(range)
        gmv_map = {}
        with open(eval("COLLECTION_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[4] not in datelist and len(items[4]) >0:
                    if items[0] not in gmv_map:
                        gmv_map[items[0]] = []
                    gmv_map[items[0]].append(items[2])

        item_price = {}
        for filename in eval("ITEMS_" + date):
            with open(filename, 'r') as infile:
                for line in infile:
                    items = line.decode('utf8').strip('\r\n').split(',')
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


    def extract_user_fea(self, date="2016"):
        """提取用户自身特征"""
        with open(eval("USER_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                if items[0] not in self.__features:
                    continue
                self.__features[items[0]].append(self.get_gender(items[1]))
                self.__features[items[0]].append(self.get_gender(items[2]))
                if len(items[3]) > 0:
                    self.__features[items[0]].append(float(items[3]))
                else:
                    self.__features[items[0]].append(1.0)
                if len(items[4]) > 0:
                    self.__features[items[0]].append(float(items[4]))
                else:
                    self.__features[items[0]].append(1.0)
                if len(items[5]) > 0:
                    self.__features[items[0]].append(self.get_suspended(items[5]))
                else:
                    self.__features[items[0]].append(0.0)
                if len(items[7]) > 0:
                    self.__features[items[0]].append(1.0 if items[7] == 'Y' else 0.0)
                else:
                    self.__features[items[0]].append(-1.0)
                self.__features[items[0]].append(float(items[8]))
                self.__features[items[0]].append(float(items[9]))
                self.__features[items[0]].append(float(items[10]))
                self.__features[items[0]].append(float(items[11]))
                if len(items[14]) > 0:
                    self.__features[items[0]].append(float(items[14]))
                else:
                    self.__features[items[0]].append(-1.0)
                if len(items[15]) > 0:
                    self.__features[items[0]].append(float(items[15]))
                else:
                    self.__features[items[0]].append(-1.0)
                if len(items[17]) > 0:
                    self.__features[items[0]].append(1.0 if items[17] == 'Y' else 0.0)
                else:
                    self.__features[items[0]].append(-1.0)
                if len(items[18]) > 0:
                    self.__features[items[0]].append(1.0 if items[18] == 'Y' else 0.0)
                else:
                    self.__features[items[0]].append(-1.0)
                if len(items[19]) > 0:
                    self.__features[items[0]].append(1.0 if items[19] == 'Y' else 0.0)
                else:
                    self.__features[items[0]].append(-1.0)
                self.__features[items[0]].append(float(items[20]))
                if len(items[21]) > 0:
                    self.__features[items[0]].append(float(items[21]))
                else:
                    self.__features[items[0]].append(-1.0)
        print >> sys.stderr, 'extracr user fea done!'


    def extract_click_fea(self, date="2016"):
        user_map = {}
        with open(eval("ACTION_CLICK_" + date), 'r') as infile:
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
                if item not in item_price:continue
                gmv += score / total * item_price[item]
            user_gmv[user] = gmv
        for user, fea in self.__features.iteritems():
            if user not in user_gmv:
                self.__features[user].append(1.0)
            else:
                self.__features[user].append(user_gmv[user])
        print >> sys.stderr, 'extracr click fea done!'

    def extract_collector_price(self, date='2016'):
        with open(eval("USER_COLLECTOR_PRICE_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        print >> sys.stderr, 'extract collector price fea done!'

    def extract_collector_price_hot(self,date='2016'):
        with open(eval("USER_COLLECTOR_PRICE_HOT_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        print >> sys.stderr, 'extract collector price hot fea done!'

    def extract_action_count(self,date='2016'):
        # with open(eval("USER_ACTION_1_" + date), 'r') as infile:
        #     for line in infile:
        #         items = line.decode('utf8').strip('\r\n').split(',')
        #         self.__features[items[0]].append(float(items[1]))
        # with open(eval("USER_ACTION_2_" + date), 'r') as infile:
        #     for line in infile:
        #         items = line.decode('utf8').strip('\r\n').split(',')
        #         self.__features[items[0]].append(float(items[1]))
        with open(eval("USER_ACTION_3_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        with open(eval("USER_ACTION_1_HOT_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))
        with open(eval("USER_ACTION_2_HOT_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))
        with open(eval("USER_ACTION_3_HOT_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        with open(eval("USER_MONTH1_GMV_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))
        with open(eval("USER_MONTH2_GMV_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))
        with open(eval("USER_MONTH3_GMV_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        with open(eval("USER_LAST_ACTION_" + date), 'r') as infile:
            for line in infile:
                items = line.decode('utf8').strip('\r\n').split(',')
                self.__features[items[0]].append(float(items[1]))

        print >> sys.stderr, 'extract action count fea done!'

    def save(self, filename=FEATURE_FILE):
        with open(filename, 'w') as outfile:
            for userid, feature in self.__features.iteritems():
                fea_str = [str(fea) for fea in feature]
                outfile.write(('%s,%s\n' % (userid, ','.join(fea_str))).encode('utf8'))

    def extract(self):
        date = self.__date
        self.extract_user(date)
        self.extract_user_fea(date)
        # self.extract_collector_price(date)
        self.extract_collector_price_hot(date)
        self.extract_action_count(date)
        self.extract_promotation_comsume(date)
        self.extract_purser_fea(date, 1)
        self.extract_purser_fea(date, 3)
        self.extract_purser_fea(date, 5)
        self.extract_purser_fea(date, 7)
        self.extract_purser_fea(date, 9)
        self.extract_purser_gmv(date, 1)
        self.extract_purser_gmv(date, 3)
        self.extract_purser_gmv(date, 5)
        self.extract_purser_gmv(date, 7)
        self.extract_purser_gmv(date, 9)
        self.extract_before_presale_purser_gmv(date)
        self.extract_purser_gmv_gate(date, 1, 100000.0)
        # self.extract_purser_gmv_gate(date, 1, 50000.0)
        # self.extract_purser_gmv_gate(date, 1, 10000.0)
        self.extract_purser_gmv_gate(date, 3, 100000.0)
        # self.extract_purser_gmv_gate(date, 3, 50000.0)
        # self.extract_purser_gmv_gate(date, 3, 10000.0)
        self.extract_purser_gmv_gate(date, 7, 100000.0)
        # self.extract_purser_gmv_gate(date, 7, 50000.0)
        # self.extract_purser_gmv_gate(date, 7, 10000.0)
        self.extract_cart_fea(date, 1)
        self.extract_cart_fea(date, 3)
        self.extract_cart_fea(date, 5)
        self.extract_cart_fea(date, 7)
        self.extract_cart_fea(date, 9)
        self.extract_cart_gmv(date, 1)
        self.extract_cart_gmv(date, 3)
        self.extract_cart_gmv(date, 5)
        self.extract_cart_gmv(date, 7)
        self.extract_cart_gmv(date, 9)
        self.extract_before_presale_cart_gmv(date)
        self.extract_cart_gmv_gate(date, 1, 100000.0)
        # self.extract_cart_gmv_gate(date, 1, 50000.0)
        # self.extract_cart_gmv_gate(date, 1, 10000.0)
        self.extract_cart_gmv_gate(date, 3, 100000.0)
        # self.extract_cart_gmv_gate(date, 3, 50000.0)
        # self.extract_cart_gmv_gate(date, 3, 10000.0)
        self.extract_cart_gmv_gate(date, 7, 100000.0)
        # self.extract_cart_gmv_gate(date, 7, 50000.0)
        # self.extract_cart_gmv_gate(date, 7, 10000.0)
        self.extract_collect_fea(date, 1)
        self.extract_collect_fea(date, 3)
        self.extract_collect_fea(date, 5)
        self.extract_collect_fea(date, 7)
        self.extract_collect_fea(date, 9)
        self.extract_collect_gmv(date, 1)
        self.extract_collect_gmv(date, 3)
        self.extract_collect_gmv(date, 5)
        self.extract_collect_gmv(date, 7)
        self.extract_collect_gmv(date, 9)
        self.extract_before_presale_collect_gmv(date)
        self.extract_collect_gmv_gate(date, 1, 100000.0)
        # self.extract_collect_gmv_gate(date, 1, 50000.0)
        # self.extract_collect_gmv_gate(date, 1, 10000.0)
        self.extract_collect_gmv_gate(date, 3, 100000.0)
        # self.extract_collect_gmv_gate(date, 3, 50000.0)
        # self.extract_collect_gmv_gate(date, 3, 10000.0)
        self.extract_collect_gmv_gate(date, 7, 100000.0)
        # self.extract_collect_gmv_gate(date, 7, 50000.0)
        # self.extract_collect_gmv_gate(date, 7, 10000.0)
        self.extract_click_fea(date)

        # 2016
        # self.extract_y(date)
        # self.save()
        # 2017
        self.save(REAL_TEST_FILE)

if __name__ == '__main__':
    Features().extract()
