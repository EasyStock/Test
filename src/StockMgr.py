'''
Created on Apr 8, 2019

@author: mac
'''
import pandas as pd
from StockItem import StockItem
import os

class CStockMgr(object):

    def __init__(self):
        pass
    
    def ReadfromHTM(self, fileName):
        dfs = pd.read_html(fileName,encoding='utf-8', header = 0)
        df =dfs[0]
        for index in range(len(df.columns)):
            print(index, df.columns[index])
#         path = fileName[:fileName.rfind('/')+1]
#         fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
#         newName = u'%s/%s.csv'%(path,fName)
#         df.to_csv(newName,encoding="utf_8_sig", index=False)
        return df
    
    def SplictToItems(self, df):
        stocks = []
        for _, row in df.iterrows():
            stock = self.FormatToStockItem(row)
            stocks.append(stock)
        
        return stocks
        
    def FormatToStockItem(self, row_item):
        item = StockItem()
        item_info = {}
        item_info[StockItem.stockID] = row_item[0]
        item_info[StockItem.stockName] = row_item[1]
        item_info[StockItem.stockZhangDieFu] = row_item[2]
        item_info[StockItem.stockGaiNian] = row_item[3]
        item_info[StockItem.stockMA5] = row_item[4]
        item_info[StockItem.stockMA8] = row_item[5]
        item_info[StockItem.stockMA13] = row_item[6]
        item_info[StockItem.stockBLower] = row_item[7]
        item_info[StockItem.stockMACD] = row_item[8]
        
        item_info[StockItem.stockOpenPrice] = row_item[9]
        item_info[StockItem.stockClosePrice] = row_item[10]
        item_info[StockItem.stockHighPrice] = row_item[11]
        item_info[StockItem.stockLowerPrice] = row_item[12]
        item_info[StockItem.stockVolumn] = row_item[13]
        
        item_info[StockItem.stockK] = row_item[14]
        item_info[StockItem.stockD] = row_item[15]
        item_info[StockItem.stockJ] = row_item[16]
        
        item_info[StockItem.stockShiZhi] = row_item[18]
        item_info[StockItem.stockXinHao] = row_item[19]
        item_info[StockItem.stockXinTai] = row_item[20]
        
        item_info[StockItem.stockBMid] = row_item[21]
        item_info[StockItem.stockBUpper] = row_item[22]
        
        item_info[StockItem.stockHangYe] = row_item[23]
        item_info[StockItem.stockDays] = row_item[24]
        
        item.initWithDict(item_info)
        return item

    def IsHighThanMA5(self, stocks):
        res = []
        for stock in stocks:
            if stock.IsLargeThanMA5():
                res.append(stock)
        print(len(res))
        return res
    
    def IsZhangFuMoreThan(self, stocks, threshold):
        res = []
        for stock in stocks:
            if stock.IsZhangFuMoreThan(threshold):
                res.append(stock)
        print(len(res))
        return res
    

    def IsLowerThanBollLower(self, stocks):
        res = []
        for stock in stocks:
            if stock.IsLowerThanBollLower():
                res.append(stock)
        
        return res
    
    
    def FormatResultToDataFrame(self, stocks):
        s = [t.ToDict() for t in stocks]
        columns = [StockItem.stockID, 
                   StockItem.stockName,
                   StockItem.stockGaiNian,
                   StockItem.stockOpenPrice,
                   StockItem.stockClosePrice,
                   StockItem.stockHighPrice,
                   StockItem.stockLowerPrice,
                   StockItem.stockVolumn,
                   StockItem.stockMA5,
                   StockItem.stockMA8,
                   StockItem.stockMA13,
                   StockItem.stockBLower,
                   StockItem.stockBMid,
                   StockItem.stockBUpper,
                   StockItem.stockZhangDieFu,
                   StockItem.stockMACD,
                   StockItem.stockK,
                   StockItem.stockD,
                   StockItem.stockJ,
                   StockItem.stockShiZhi,
                   StockItem.stockHangYe,
                   StockItem.stockDays,
                   StockItem.stockXinHao,
                   StockItem.stockXinTai,
                   
                    ]
        d = pd.DataFrame(s,columns=columns)
        return d
        
    def SaveToCSV(self,fileName, stocks):
        df = self.FormatResultToDataFrame(stocks)
        df.to_csv(fileName,encoding="utf_8_sig", index=False)

    def AnalyzerBanKuaiStocks(self, stocks):
        allKeys = []
        ret = {}
        for stock in stocks:
            allKeys.extend(stock.getBanKuai())
    
        allKeys=list(set(allKeys))
        print('with %d stocks and %d keys' % (len(stocks), len(allKeys)))
        for key in allKeys:
            if key not in ret:
                ret[key] = []
            for stock in stocks:
                if stock.isKeyIn(key):
                    ret[key].append(stock)
        return ret
                
    def AnalysisOneFile(self,fileName):
        fName = fileName[fileName.rfind('/')+1: fileName.rfind('.')]
        path = fileName[:fileName.rfind('/')+1]
        df = self.ReadfromHTM(fileName)
        stocks = self.SplictToItems(df)
        #stocks = self.IsHighThanMA5(stocks)
        stocks = self.IsZhangFuMoreThan(stocks, 7.0)
        
        fileName = u'%s/../out/%s.csv'%(path,fName)
        print(fileName)
        self.SaveToCSV(fileName, stocks)
        
        
        mapOfResult = self.AnalyzerBanKuaiStocks(stocks)
        res = sorted(mapOfResult.items(), key=lambda d:len(d[1]), reverse = True)
        key2 = u'%s' %(fName)
        ret ={
            u'板块':[r[0] for r in res],
            key2:[len(r[1]) for r in res],
        }
        df = pd.DataFrame.from_dict(ret)
        df = df[[u'板块', key2]]
        fileName1 = u'%s/../summary/%s.csv'%(path,fName)
        print(fileName1)
        df.to_csv(fileName1,encoding="utf_8_sig", index=False)
        self.mergeFiles(u'%s/../summary/'%(path))
        
    def mergeFiles(self,folder):
        datas = []
        filenames=os.listdir(folder)
        for f in filenames:
            fullPath = os.path.join(folder, f)
            df = pd.read_csv(fullPath, index_col = 0, encoding='utf_8_sig')
            datas.append(df)
        res = pd.concat(datas, axis=1,join='outer',sort=False)
        res = res.fillna(0)
        fileName = '%s/../out.csv'%(folder)
        print(fileName)
        res.to_csv(fileName,encoding='utf_8_sig')
    