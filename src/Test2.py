'''
Created on Apr 3, 2019

@author: mac
'''
from StockMgr import CStockMgr

'''
概念,5日均线, 8日均线,13日均线,boll线下轨,macd,开盘价,收盘价,最高价,最低价,成交量,K,D J
'''
if __name__ == '__main__':
    fileName = u'/Volumes/Data/StockAnalysisData/raw/2019-04-12.xls'
    mgr = CStockMgr()
    mgr.AnalysisOneFile(fileName)
    

