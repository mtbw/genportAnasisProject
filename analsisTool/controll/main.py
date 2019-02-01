import controll.ExcelDataHandling as EDH
import controll.ExcelDataAnalsis as EDA
import pandas as pd

handlingData = EDH.ExcleDataHandling("trade_history_473953.csv",0.001).dataSetting()

if handlingData != 1:
    # df = pd.DataFrame(handlingData)
    # print(df)
    print("분석 시작..")
    anasisData = EDA.ExcleDataAnasis(handlingData).totalProfit(10000000)
    print(f'총손익{anasisData}')
else:
    print("파일이 없습니다.")