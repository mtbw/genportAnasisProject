import pandas as pd
import csv
class ExcleDataHandling:
    # 클래스 리스트 선언
    category = ["date",                 #날짜
                "itemName",             #종목이름
                "order",                #주문
                "tradePrice",           #매매가격(원)
                "quantity",             #수량(주)
                "reason",               #사유
                "profitRate",           #수익률
                "transactionPrice",     #거래금액
                "fee",                  #수수료
                "remainingQuantity"]    #남은 수량


    # 파일 경로, 수수료 비중. 0.001 == 0.01%
    def __init__(self, filePath,fee):
        self.filePath = filePath
        self.fee = fee
        try:
            f = open(self.filePath, 'r', encoding='utf-8')
            self.rdr = csv.reader(f)
            next((x for i, x in enumerate(self.rdr) if i == 0), None)
        except:
            print("파일이 잘못 되었습니다.")

    # 인스턴스 메서드 선언
    def dataSetting(self):
        datas_dict = {}
        posQuantity = {}
        for categorys in ExcleDataHandling.category:
            datas_dict[categorys] = []

        try:
            dataRemake = self.rdr
        except:
            return 1
        else:

            for line in dataRemake:
                i = 0
                for categorys in ExcleDataHandling.category :

                    if i <= 6 :
                        datas_dict[categorys].append(line[i])
                    elif i == 7 :
                        transactionPrice = int(float(line[3])) * int(float(line[4]))
                        datas_dict[categorys].append(transactionPrice)
                    elif i == 8 :
                        fee = int(float((int(float(line[3])) * int(float(line[4]))) * self.fee))
                        datas_dict[categorys].append(fee)
                    elif i == 9 :
                        #dictionary 자료구조로 남은 보유 수량 검사
                        if line[2] == "매수" :
                            if posQuantity.get(line[1]) == None:
                                posQuantity[line[1]] = line[4]
                            else:
                                posQuantity[line[1]] = int(float(posQuantity[line[1]])) + int(float(line[4]))
                        elif line[2] == "매도" :
                            if posQuantity.get(line[1]) == None:
                                posQuantity[line[1]] = line[4]
                            else:
                                posQuantity[line[1]] = int(float(posQuantity[line[1]])) - int(float(line[4]))
                        datas_dict[categorys].append(int(posQuantity[line[1]]))

                    i += 1
            return datas_dict





# def profitLoss(self):
#     thisMoney = 50000000
#     fee = 0.001
#     item = 0
#     for line in self.df:
#         print(f'현재금액 {thisMoney}')
#         if line[excleImport.category[2]] == "매수":
#             purchaseMoney = int(line[excleImport.category[3]]) * int(float(line[excleImport.category[4]]))
#             thisMoney -= purchaseMoney + int(purchaseMoney * fee)
#             print(f"매수 : {thisMoney} -= {line[excleImport.category[3]]} * {line[
#                 excleImport.category[4]]} --- 수수료 : {purchaseMoney * fee}")
#             item += 1
#         elif line[2] == "매도":
#             seleMoney = int(line[excleImport.category[3]]) * int(float(line[excleImport.category[4]]))
#             thisMoney += seleMoney - int(seleMoney * fee)
#             print(f"매도({line[excleImport.category[6]]}) : {thisMoney} += {line[excleImport.category[3]]} * {line[
#                 excleImport.category[4]]} --- 수수료 : {seleMoney * fee}")
#             item -= 1
#
#         print(item)
#     return thisMoney