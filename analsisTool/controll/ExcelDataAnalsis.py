import pandas as pd

class ExcleDataAnasis:

    # 파일 경로, 수수료 비중. 0.001 == 0.01%
    def __init__(self, handlingData):
        self.handlingData = handlingData

    def totalProfit(self,startMoney):

        tradeData = {}  #set dictionary정의
        i = 0

        df = pd.DataFrame(self.handlingData)

        for row in df.itertuples():
            print(f'현재금액 {startMoney}')
            i += 1
            if row[3] == "매수":
                if tradeData.get(row[2]) == None:
                    tradeData[row[2]] = row[8]
                else:
                    tradeData[row[2]] = tradeData[row[2]] + row[8]

                startMoney -= row[8] #총 매수금액
                startMoney -= row[9] #증권사 수수료
                print(f'매수 = 금액 : {row[8]}, 수수료 : {row[9]}')

            elif row[3] == "매도":
                if row[10] == 0:
                    del tradeData[row[2]]
                else:
                    tradeData[row[2]] = tradeData[row[2]] - row[8]

                startMoney += row[8] #총 매도금액
                startMoney -= row[9] #증권사 수수료
                startMoney -= int(float(row[8] * 0.003))    #거래수수료
                print(f'매도 = 금액 : {row[8]}, 수수료 : {row[9]}')
            print(row)
        print(startMoney)
        print(i)
        for row in tradeData:
            startMoney += tradeData.get(row)
        return startMoney

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