# -*- coding: utf-8 -*-
"""
Market Microstructure Finance functions
Python version: Python 3.7.1 
"""

    
def tick_bars(df, price_column, m):
    '''
    Compute index tick bars

    # args
        df: pandas data frame
        price_column: name for price data
        m: int(), threshold value for ticks
    # returns
        idx: list of indices
    # reference:
       https://github.com/BlackArbsCEO/Adv_Fin_ML_Exercises/blob/master/notebooks/Tick%2C%20Volume%2C%20Dollar%20Volume%20Bars.ipynb
    
    '''
    t = df[price_column]
    ts = 0
    idx = []
    for i, x in enumerate(t):
        ts += 1
        if ts >= m:
            idx.append(i)
            ts = 0
            continue
    return idx

def tick_bar_df(df, price_column, m):
    idx = tick_bars(df, price_column, m)
    return df.iloc[idx].drop_duplicates()

def atrib_p(df,price_column,idx,flag):
    '''
    Compute some values from tick bar range
    
    # args
        df: pandas dataframe
        price_column: Column price
        idx: Column with index location
        flag:   0 if Bar price is open
                1 if Bar price is average
                2 if Bar price is maximun
                3 if Bar price is minimun
    # returns
        returns a data frame with new column
    '''
    flag_p =[]
    for i in range(0,len(idx)):
        if i == 0:
            inf = 0
            sup = idx[i]
        else:
            inf = idx[i-1]+1
            sup = idx[i]
        if flag == 0:
            flag_p.append(df[price_column][inf])            
        if flag == 1:
            flag_p.append(df[price_column][inf:sup].mean())
        if flag == 2:
            flag_p.append(df[price_column][inf:sup].max())
        if flag == 3:
            flag_p.append(df[price_column][inf:sup].min())
    return flag_p



def tick_bar_dfx(df, price_column, m):
    '''
    
    Compute the thick bar with open bar price, average bar price,
    maximum bar price, and minimum  bar price.
    
    # args
        df: pandas dataframe
        idx: tick bar index
        dfn: pandas dataframe from tick bar index
        open_b: price from the begining of range
        avg_p: average price computed from the bar range
        max_p: maximum price computed from the bar range
        close_b: rename the price in order to get more consistent with others
                 variable notations
    # returns
        Return a pandas data frame with computed tick bars, and its respective
        open, close, high, and low bar prices.
    '''
    idx = tick_bars(df, price_column, m)
    dfn = df.iloc[idx].copy()
    dfn['open_b']= atrib_p(df,price_column,idx,0)
    dfn['avg_b']= atrib_p(df,price_column,idx,1)
    dfn['max_b']= atrib_p(df,price_column,idx,2)
    dfn['min_b']= atrib_p(df,price_column,idx,3)
    dfn.rename(columns={'price': 'close_b'}, inplace=True)
    return dfn
