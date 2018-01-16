ROOT = '/Users/banmo/personal/tmall/'

PROMOTION_CONSUMPTION_LAST2YEARS_2016 = ROOT + 'Algo_Challenge_Data_promotion_consumption_latest2years_2016.csv'
PROMOTION_CONSUMPTION_LAST2YEARS_2017 = ROOT + 'Algo_Challenge_Data_promotion_consumption_latest2years_2017.csv'

BROWSING_2016 = [ROOT + 'Algo_Challenge_Data_browsing_latest3months_2016_part_' + str(df) + '.csv' for df in xrange(1, 11)]
BROWSING_2017 = [ROOT + 'Algo_Challenge_Data_browsing_latest3months_2017_part_' + str(df) + '.csv' for df in xrange(1, 12)]

CARTING_2016 = [ROOT + 'Algo_Challenge_Data_carting_latest3months_2016_part_' + str(df) + '.csv' for df in xrange(1, 3)]
CARTING_2017 = [ROOT + 'Algo_Challenge_Data_carting_latest3months_2017_part_' + str(df) + '.csv' for df in xrange(1, 3)]

PURCHASING_2016 = [ROOT + 'Algo_Challenge_Data_purchasing_latest3months_2016_part_' + str(df) + '.csv' for df in xrange(1, 3)]
PURCHASING_2017 = [ROOT + 'Algo_Challenge_Data_purchasing_latest3months_2017_part_' + str(df) + '.csv' for df in xrange(1, 3)]

COLLECTION_2016 = ROOT + 'Algo_Challenge_Data_collection_latest3months_2016.csv'
COLLECTION_2017 = ROOT + 'Algo_Challenge_Data_collection_latest3months_2017.csv'

D11_CONSUMPTION_2016 = ROOT + 'Algo_Challenge_Data_2016_D11_user_consumption.csv'
D11_CONSUMPTION_UPDATE_2016 = ROOT + 'Algo_Challenge_Data_2016_D11_user_consumption_update.csv'

USER_2016 = ROOT + 'Algo_Challenge_Data_user_dim_2016.csv'
USER_2017 = ROOT + 'Algo_Challenge_Data_user_dim_2017.csv'

ITEMS_2016 = [ROOT + 'Algo_Challenge_Data_item_dim_2016_part_' + str(df) + '.csv' for df in xrange(1, 3)]
ITEMS_2017 = [ROOT + 'Algo_Challenge_Data_item_dim_2017_part_' + str(df) + '.csv' for df in xrange(1, 3)]

ACTION_CLICK_2016 = ROOT + 'Action_click_2016.csv'
ACTION_CLICK_2017 = ROOT + 'Action_click_2017.csv'

ACTION_CLICK_CART_5_2016 = ROOT + 'Action_click_cart_5_2016.csv'
ACTION_CLICK_CART_10_2016 = ROOT + 'Action_click_cart_10_2016.csv'
ACTION_CLICK_CART_20_2016 = ROOT + 'Action_click_cart_20_2016.csv'

ACTION_CLICK_BROWSING_5_2016 = ROOT + 'Action_click_browsing_5_2016.csv'
ACTION_CLICK_BROWSING_10_2016 = ROOT + 'Action_click_browsing_10_2016.csv'
ACTION_CLICK_BROWSING_20_2016 = ROOT + 'Action_click_browsing_20_2016.csv'

ACTION_CLICK_COLLECT_5_2016 = ROOT + 'Action_click_collect_5_2016.csv'
ACTION_CLICK_COLLECT_10_2016 = ROOT + 'Action_click_collect_10_2016.csv'
ACTION_CLICK_COLLECT_20_2016 = ROOT + 'Action_click_collect_20_2016.csv'

ACTION_CLICK_CART_5_2017 = ROOT + 'Action_click_cart_5_2017.csv'
ACTION_CLICK_CART_10_2017 = ROOT + 'Action_click_cart_10_2017.csv'
ACTION_CLICK_CART_20_2017 = ROOT + 'Action_click_cart_20_2017.csv'

ACTION_CLICK_BROWSING_5_2017 = ROOT + 'Action_click_browsing_5_2017.csv'
ACTION_CLICK_BROWSING_10_2017 = ROOT + 'Action_click_browsing_10_2017.csv'
ACTION_CLICK_BROWSING_20_2017 = ROOT + 'Action_click_browsing_20_2017.csv'

ACTION_CLICK_COLLECT_5_2017 = ROOT + 'Action_click_collect_5_2017.csv'
ACTION_CLICK_COLLECT_10_2017 = ROOT + 'Action_click_collect_10_2017.csv'
ACTION_CLICK_COLLECT_20_2017 = ROOT + 'Action_click_collect_20_2017.csv'

ACTION_CLICK_COLLECT_AND_CART_5_2016 = ROOT + 'Action_click_collect_and_cart_5_2016.csv'
ACTION_CLICK_COLLECT_AND_CART_10_2016 = ROOT + 'Action_click_collect_and_cart_10_2016.csv'
ACTION_CLICK_COLLECT_AND_CART_20_2016 = ROOT + 'Action_click_collect_and_cart_20_2016.csv'

ACTION_CLICK_COLLECT_AND_CART_5_2017 = ROOT + 'Action_click_collect_and_cart_5_2017.csv'
ACTION_CLICK_COLLECT_AND_CART_10_2017 = ROOT + 'Action_click_collect_and_cart_10_2017.csv'
ACTION_CLICK_COLLECT_AND_CART_20_2017 = ROOT + 'Action_click_collect_and_cart_20_2017.csv'



FEATURE_FILE = ROOT + 'feature.csv'
REAL_TEST_FILE = ROOT + 'test_fea.csv'

FEATURE_FILE_BEFORE = ROOT + 'feature_before.csv'
REAL_TEST_FILE_BEFORE = ROOT + 'test_fea_before.csv'

USER_COLLECTOR_PRICE_2016 = ROOT + 'user_collector_price_2016.csv'
USER_COLLECTOR_PRICE_2017 = ROOT + 'user_collector_price_2017.csv'

USER_COLLECTOR_PRICE_HOT_2016 = ROOT + 'user_collector_price_hot_2016.csv'
USER_COLLECTOR_PRICE_HOT_2017 = ROOT + 'user_collector_price_hot_2017.csv'

USER_ACTION_1_2016 = ROOT + 'user_before_d11_week_collection_count_2016.csv'
USER_ACTION_1_2017 = ROOT + 'user_before_d11_week_collection_count_2017.csv'

USER_ACTION_2_2016 = ROOT + 'user_before_d11_week_carting_count_2016.csv'
USER_ACTION_2_2017 = ROOT + 'user_before_d11_week_carting_count_2017.csv'


USER_ACTION_3_2016 = ROOT + 'user_before_d11_week_browsing_count_2016.csv'
USER_ACTION_3_2017 = ROOT + 'user_before_d11_week_browsing_count_2017.csv'

USER_ACTION_1_HOT_2016 = ROOT + 'user_before_d11_week_collection_count_hot_2016.csv'
USER_ACTION_1_HOT_2017 = ROOT + 'user_before_d11_week_collection_count_hot_2017.csv'

USER_ACTION_2_HOT_2016 = ROOT + 'user_before_d11_week_carting_count_hot_2016.csv'
USER_ACTION_2_HOT_2017 = ROOT + 'user_before_d11_week_carting_count_hot_2017.csv'


USER_ACTION_3_HOT_2016 = ROOT + 'user_before_d11_week_browsing_count_hot_2016.csv'
USER_ACTION_3_HOT_2017 = ROOT + 'user_before_d11_week_browsing_count_hot_2017.csv'

USER_MONTH1_GMV_2016 = ROOT + 'user_gmv_month1_2016.csv'
USER_MONTH2_GMV_2016 = ROOT + 'user_gmv_month2_2016.csv'
USER_MONTH3_GMV_2016 = ROOT + 'user_gmv_month3_2016.csv'

USER_MONTH1_GMV_2017 = ROOT + 'user_gmv_month1_2017.csv'
USER_MONTH2_GMV_2017 = ROOT + 'user_gmv_month2_2017.csv'
USER_MONTH3_GMV_2017 = ROOT + 'user_gmv_month3_2017.csv'

USER_LAST_ACTION_2016 = ROOT + 'user_before_d11_last_action_time_2016.csv'
USER_LAST_ACTION_2017 = ROOT + 'user_before_d11_last_action_time_2017.csv'

