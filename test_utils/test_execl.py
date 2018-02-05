#!/usr/bin/env python
#coding:utf-8


import sys

from numpy.random import random

from test_http import get_industry

reload(sys)

import pandas as pd
import numpy as np


def scop_del(x):
    if x is None:
        return str(-1)

    return str(get_industry(x))

    pass


if __name__ == '__main__':
    df_base = pd.read_excel("/home/wl/WLData/2018-01-11/inc_industry2018011 (copy).xlsx")

    # print df_base.index
    print 'base \n'
    print df_base.columns
    print df_base.head(1)
    # print df_base.describe()
    # print df_base[u'公司名']
    # print df_base.loc[:,[u'公司名', u'行业', u'行业.1']]

    df = pd.read_csv('/home/wl/WLData/2018-01-11/inc_industry_scope',sep='\x01')
    # print df.head(1)
    # print df.index
    # print df.columns


    # business_scope_value = pd.DataFrame({'industry_id_by_scope' : df['business_scope'].dropna().apply(scop_del)})
    business_scope_value = pd.DataFrame({'industry_id_by_scope' : df['business_scope'].apply(scop_del)})
    # print business_scope_value


    df = pd.merge(df,business_scope_value,left_index=True, right_index=True)
    # print df.columns
    # print df.head(1)
    df.to_csv('foo.csv',sep='\x01')
    # new_df = df.loc[:,['inc_name', 'business_scope', 'industry_id_by_scope']]
    new_df = df.loc[:,['inc_name','industry_id_by_scope']]
    print df.columns
    print df.head(1)

    df_combine = pd.merge(df_base, new_df,left_on=u'公司名', right_on='inc_name')

    # pass
