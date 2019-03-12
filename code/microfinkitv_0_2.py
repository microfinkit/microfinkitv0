# -*- coding: utf-8 -*-
"""
Market Microstructure Finance functions
Python version: Python 3.7.1 
version 0.2
"""
import pandas as pd
import numpy as np
    
def bar(df, bar_column, treshold, flag):
    '''
    Compute index for bar's kind

    # args
        df: pandas dataframe
        bar_column: Column name for bar's kind
        treshold: int(), Threshold value for bar's kind
        flag:   0 if is a tick bar
                1 if is a volume bar 
                2 if is a dollar bar        
    # returns
        idx: List of indices
    # reference:
       https://github.com/BlackArbsCEO/Adv_Fin_ML_Exercises/blob/master/notebooks/Tick%2C%20Volume%2C%20Dollar%20Volume%20Bars.ipynb  
    '''
    t = df[bar_column]
    ts = 0
    idx = []
    if flag == 0:
        for i, x in enumerate(t):
            ts += 1
            if ts >= treshold:
                idx.append(i)
                ts = 0
                continue
    else:
        for i, x in enumerate(t):
            ts += x
            if ts >= treshold:
                idx.append(i)
                ts = 0
                continue        
    # Ensures that the last index is included within the selected indexes
    #if idx[-1] != len(t)-1:
    #    idx.append(len(t)-1)
    return idx


def vwap(df, vol_column,dollar_column,idx):
    '''
    Compute the Volume Weighted Average Price
    # args
        df: Pandas dataframe
        dollar_column: Transaction amount column (price x quantity)
        vol_column: Stock quantity transactions
        idx: list of indices   
    # returns
        list with wwap computed
    '''
    vwap = []
    for i in range(0,len(idx)):
        if i == 0:
            inf = 0
            sup = idx[i]+1
        else:
            inf = idx[i-1]+1
            sup = idx[i]+1
        vwap.append(sum(df[dollar_column][inf:sup])/
                    sum(df[vol_column][inf:sup]))
    return vwap



def attribute(df, att_column, idx, flag):
    '''
    Compute some values from tick bar range
    
    # args
        df: Pandas dataframe
        bar_column: Column price
        idx: Column with index location
        flag:   0 if bar range price is open
                1 if bar range price is average
                2 if bar range price is maximun
                3 if bar range price is minimun
                4 if volume bar range or dollar bar  range is added
    # returns
        returns a new data frame column according to the attribute flag
    '''
    flag_p =[]
    for i in range(0,len(idx)):
        if i == 0:
            inf = 0
            sup = idx[i]+1
        else:
            inf = idx[i-1]+1
            sup = idx[i]+1     
        if flag == 0:
            flag_p.append(df[att_column][inf])
        if flag == 1:
            flag_p.append(df[att_column][inf:sup].mean())
        if flag == 2:
            flag_p.append(df[att_column][inf:sup].max())
        if flag == 3:
            flag_p.append(df[att_column][inf:sup].min())
        if flag == 4:
            flag_p.append(df[att_column][inf:sup].sum())
            continue
    return flag_p



def bar_df(df, price_column,vol_column, dollar_column, treshold, flag):
    '''
    Compute the bar's kind selected with open bar price, average bar price,
    maximum bar price,minimum  bar price and vwap.
    
    # args
        df: Pandas dataframe
        idx: Tick bar index
        dfn: Pandas dataframe from tick bar index
        bar_column: Column name for bar's kind
        dollar_column: Transaction amount column (price x quantity)
        vol_column: Stock quantity transactions
        treshold: int(), Threshold value for bar's kind
        flag:   0 if is a tick bar
                1 if is a volume bar o dollar bar             

    # returns
        Return a pandas data frame with computed tick bars and:
            open_b: Price from the begining of range
            avg_b: Average price computed from the bar range
            max_b: Maximum price computed from the bar range
            close_b: Rename the price in order to get more consistent with others
                     variable notations
    '''
    if flag ==0:
        bar_column = price_column
    elif flag == 1:
        bar_column = vol_column
    else:
        bar_column = dollar_column
    
    idx = bar(df, bar_column, treshold, flag)
    dfn = df.iloc[idx].copy()   
    dfn['open_b'] = attribute(df,price_column,idx,0)
    dfn['avg_b'] = attribute(df,price_column,idx,1)
    dfn['max_b'] = attribute(df,price_column,idx,2)
    dfn['min_b'] = attribute(df,price_column,idx,3)
    dfn['vol_acum_b'] = attribute(df,vol_column,idx,4)
    dfn['dollar_acum_b'] = attribute(df,dollar_column,idx,4)
    dfn['vwap_b'] = vwap(df, vol_column,dollar_column,idx)
    dfn = dfn.drop([vol_column, dollar_column], axis = 1)
    dfn.rename(columns={'price': 'close_b'}, inplace=True)
    return dfn


def tick_rule(df,price_column):
    '''
    Compute the tick rule proposed by Lopez del Prado in AMLF
    # args
        df: Pandas dataframe
        price_column: price column name
    
    # returns 
        Returns a panda dataframe column, with delta price sing
        bt =  abs(dp)/dp
        if bt == 0 then bt = bt-1
        In order to get information at series begin, the bt takes bt+1 sing.
    
    '''
    # For some reaon panda gets a warning message.  The next code
    # disable this message
    pd.options.mode.chained_assignment = None
    dfn = df.copy()
    dfn[price_column] = dfn[price_column] - dfn[price_column].shift(1)
    dfn[price_column] = dfn[price_column].apply(np.sign)
    dfn[price_column][dfn[price_column]==0] = np.nan
    dfn[price_column] = dfn[price_column].fillna(method='ffill')
    dfn[price_column] = dfn[price_column].fillna(method='bfill')
    dfn.rename(columns={price_column: 'tick_rule'},inplace=True)
    return dfn['tick_rule']
    return dfn