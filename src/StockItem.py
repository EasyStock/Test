'''
Created on Apr 7, 2019

@author: mac
'''

class StockItem(object):
    stockID = u'股票代码'
    stockName = u'股票简称'
    stockZhangDieFu = u'涨跌幅(%)'
    stockGaiNian = u' 所属概念'    
    stockOpenPrice = u'开盘价'
    stockClosePrice = u'收盘价'
    stockHighPrice = u'最高价'
    stockLowerPrice = u'最低价'
    stockVolumn = u'成交量'
    
    stockMA5 = u'5日均线'
    stockMA8 = u'8日均线'
    stockMA13 = u'13日均线'
    
    stockBLower = u'BOLL 下轨'
    stockBMid = u'BOLL 中轨'
    stockBUpper = u'BOLL 上轨'
    
    stockMACD = u'MACD'
    stockK = u'kdj(k值)'
    stockD = u'kdj(d值)'
    stockJ = u'kdj(j值)'
    stockShiZhi = u'a股流通市值'
    stockHangYe = u'所属行业'
    stockDays = u'上市天数'
    stockXinTai = u'技术形态'
    stockXinHao = u'买入信号'

    def __init__(self):
        self._stockInfo = {}
        self._banKuai = []
    
    def initWithDict(self, _dict):
        self._stockInfo = _dict
        words = self._stockInfo[StockItem.stockGaiNian].split(';')
        if words and len(words) >0:
            self._banKuai = words
        else:
            self._banKuai = []

    def isKeyIn(self, key):
        if self._stockInfo[StockItem.stockGaiNian].find(key) != -1:
            return True
        else:
            return False

    def isKeysIn(self, keys):
        res = [False for key in keys if not self.isKeyIn(key)]
        if not res:
            return True
        else:
            return False
        
    def getBanKuai(self):
        return self._banKuai
    
    def __str__(self, *args, **kwargs):
        msg = '''
        股票代码: %s
        股票名称:%s
        现价:%s
        涨跌幅:%s
        板块:%s
        5日均线:%s
        8日均线:%s
        13日均线:%s
        BOLL 上轨:%s
        BOLL 中轨:%s
        BOLL 下轨:%s
        '''% (
            self._stockInfo[StockItem.stockID], 
            self._stockInfo[StockItem.stockName],
            self._stockInfo[StockItem.stockClosePrice], 
            self._stockInfo[StockItem.stockZhangDieFu],
            self._stockInfo[StockItem.stockGaiNian],
            self._stockInfo[StockItem.stockMA5],
            self._stockInfo[StockItem.stockMA8],
            self._stockInfo[StockItem.stockMA13],
            self._stockInfo[StockItem.stockBUpper],
            self._stockInfo[StockItem.stockBMid],
            self._stockInfo[StockItem.stockBLower]
            )
        return msg
        
    def IsLargeThanMA5(self):
        try:
            ma5 = float(self._stockInfo[StockItem.stockMA5])
        except Exception as e:
            return False
        
        price = float(self._stockInfo[StockItem.stockClosePrice])
        if price >= ma5:
            return True
        else:
            return False
        
    def IsLowerThanBollLower(self):
        try:
            BLower = float(self._stockInfo[StockItem.stockBLower])
        except Exception as e:
            return False
        
        price = float(self._stockInfo[StockItem.stockClosePrice])
        if price < BLower:
            return True
        else:
            return False
        
    def IsZhangFuMoreThan(self,threshold):
        try:
            zhangdiefu = float(self._stockInfo[StockItem.stockZhangDieFu])
        except Exception as e:
            return False
        
        if zhangdiefu >= threshold:
            return True
        else:
            return False

        
    def ToDict(self):
        return self._stockInfo