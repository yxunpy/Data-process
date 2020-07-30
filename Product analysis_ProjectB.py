import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


data = pd.read_csv('.\订单表.csv', encoding='gbk')
data=data.sort_values (by='客户ID',ascending=True)

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

hot_encoded_df = data.groupby(['客户ID', '产品名称'])['产品名称'].count().unstack().reset_index().fillna(0).set_index('客户ID')
hot_encoded_df = hot_encoded_df.applymap(encode_units)
print(hot_encoded_df)
hot_encoded_df .to_csv('temp1.csv')
frequent_itemsets = apriori(hot_encoded_df, min_support=0.05, use_colnames=True)
frequent_itemsets=frequent_itemsets.sort_values(by='support',ascending= True)

rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.8)
rules=rules.sort_values(by='lift',ascending= True)
print("频繁项集：", frequent_itemsets)
print("关联规则：", rules[(rules['lift'] >= 0.9) & (rules['confidence'] >= 0.4)])

frequent_itemsets .to_csv('频繁项集.csv')
rules.to_csv('关联规则.csv')


