import pandas as pd
##test
from matplotlib import pyplot as plt
import numpy as np
class ExcleDataAnasis:

    # 파일 경로, 수수료 비중. 0.001 == 0.01%
    def __init__(self, handlingData):
        self.handlingData = handlingData


    def profitHistory(self,startMoney):
        #test
        tradeCount = 0
        maxMDD = 0
        maxPreMDD = 0
        ## 운용가능 <= 시작 머니 담기.
        orderableAmount = startMoney

        # 카탈로그 명칭 리스트에 담기.
        category = ["orderableAmount",      #주문가능 금액
                    "amountUsed",           #사용된 금액
                    "totalAssets",          #총 자산 = 주문가능금액 + 사용된 금액
                    "cumulative",           #누적 수익율
                    "newHigh",              #신고가
                    "MDD",                  #낙폭율.
                    "preHigh",              #전고q가(낙폭전 고점)
                    "preMDD"]               #전고가로 해당하는 낙폭.
        # 딕셔너리 자료구조에 카탈로그 정의하기.
        datas_dict = {}
        for categorys in category:
            # 딕셔너리 자료구조에 각 항목 배열 생성.
            datas_dict[categorys] = []

        # set dictionary정의 => 가지고있는 종목 입력. 보유수량 0이되면 삭제.
        holdingItem = {}

        # 딕셔너리 리스트을 dataFrame으로 만들기.
        df = pd.DataFrame(self.handlingData)

        #신고점 변수 선언.
        newHigh = 0
        #전고점 변수 선언.
        preHigh = 0
        #이전 자산 총합.
        preTotal = startMoney

        ## 주문가능금액, 사용된 금액, 총 자산 data만들기.
        for row in df.itertuples():
            tradeCount += 1
            ## 매수시 로직
            if row[3] == "매수":
                if holdingItem.get(row[2]) == None:
                    # 딕셔너리 구조에 종목이 없다면 종목에 돈 넣음.
                    holdingItem[row[2]] = row[8]
                else:
                    # 딕셔너리에 종목 있으면 기존 돈에 돈 또 넣음(거의 없음)
                    holdingItem[row[2]] = holdingItem[row[2]] + row[8]

                orderableAmount -= row[8]   # 총 매수금액
                orderableAmount -= row[9]   # 증권사 수수료
                print(f'매수 = 금액 : {row[8]}, 수수료 : {row[9]}')
            ## 매도시 로직
            elif row[3] == "매도":

                if row[10] == 0:
                    # 남은 수량이 0이라면 종목 삭제.
                    del holdingItem[row[2]]
                else:
                    # 매도 했는데도 남은 수량이 있다면 종목 전체 매수금액 - 거래금액 빼버리기.
                    holdingItem[row[2]] = holdingItem[row[2]] - row[8]

                orderableAmount += row[8]           # 총 매도금액
                orderableAmount -= row[9]           # 매도금액의 증권사 수수료
                orderableAmount -= (float(row[8] * 0.003))    #거래세금. 0.3%
                print(f'매도 = 금액 : {row[8]}, 수수료 : {row[9]}')

            ### 매수, 매도 종료 후 -- 남은돈, 주식 보유 돈, 전체돈 = 남은돈 + 주식 보유 돈
            datas_dict[category[0]].append(orderableAmount) # 남은돈..
            # 홀딩 아이템의 종목 돈 합하기.
            amountUsed = 0
            for item in holdingItem:
                amountUsed += holdingItem.get(item)
            # 주식에 보유한 입력
            datas_dict[category[1]].append(amountUsed)

            # 전체 돈..
            totalAssets = orderableAmount+amountUsed
            datas_dict[category[2]].append(totalAssets)

            # 누적수익율
            cumulative = ((totalAssets - startMoney) / startMoney) * 100
            datas_dict[category[3]].append(cumulative)

            #### 신고점 항목.
            if cumulative > newHigh:
                #신고점 돌파시!
                newHigh = cumulative
                newHighCheck = 1
            else:
                #돌파하지 않을경우.
                newHighCheck = 0
            datas_dict[category[4]].append(newHigh)

            ### MDD (신고점 돌파시 0으로 리셋, 아니면 최대하락폭 기록.)
            if newHighCheck == 1 :#신고점 돌파.
                MDD = 0
            else :      #돌파하지 못함.
                MDD = cumulative - newHigh

            # MDD 입력.
            datas_dict[category[5]].append(MDD)
            # 최대 MDD?
            if maxMDD > MDD :
                maxMDD = MDD

            ##전고가(낙폭전 고점)
            ### 전일 전체 금액보다 낮아질경우.
            ### 전고점이 아닌 저점을 찍고->올라온 고점 갱신해야함.
            #저점을 찍을때는 업데이트하지 않음 저점보다 올라갈떄부터 갱신.
            if preTotal <= totalAssets:
                #이전 자산보다 현재자산이 높을때.
                preHigh = cumulative
                preHighCkeck = 1
            else :
                preHighCkeck = 0
            datas_dict[category[6]].append(preHigh)
            #### 이전 자산 총합
            preTotal = totalAssets

            ###
            ### MDD (점고점 돌파시 0으로 리셋, 아니면 최대하락폭 기록.)
            if preHighCkeck == 1:  # 전고점 돌파.
                preMDD = 0
            else:  # 돌파하지 못함.
                preMDD = cumulative - preHigh

            # MDD 입력.
            datas_dict[category[7]].append(preMDD)
            # 최대 MDD?
            if maxPreMDD > preMDD:
                maxPreMDD = preMDD


        # print(datas_dict)

        #test
        plt.title('[gen port] trade_history Analsis')
        plt.xlabel('[day time]')
        plt.ylabel('[Cumulative return]')
        plt.xticks([0, 824], ['20170102', '20190201'])

        plt.plot(datas_dict["cumulative"])
        plt.plot(datas_dict["newHigh"])
        plt.plot(datas_dict["MDD"])
        plt.plot(datas_dict["preHigh"])
        plt.plot(datas_dict["preMDD"])
        plt.legend(["cumulative","newHigh","newMDD","preHigh","preMDD"])
        plt.savefig('genport.png')
        plt.show()

        #df + datas_dict
        datas = pd.DataFrame(datas_dict)
        df = df.join(datas)


        # print(df)


        errorRate = ((39166043 - totalAssets) / 39166043) * 100
        print(f'39166043원 <=%=> {totalAssets} ==> 오차율 {errorRate}%')
        print(f'maxMDD : {maxMDD}')
        print(f'preMaxMDD : {maxPreMDD}')

        return df
