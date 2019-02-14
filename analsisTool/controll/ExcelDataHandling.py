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
                # "orderableAmount",      #주문가능 금액
                # "amountUsed",           #사용된 금액
                # "totalAssets"]          #총 자산 = 주문가능금액 + 사용된 금액

    # 파일 경로, 수수료 비중. 0.001 == 0.01%
    def __init__(self, filePath,fee):
        self.filePath = filePath    # 파일 경로
        self.fee = fee              # 지정 수수료 (증권사 수수료)
        try:
            f = open(self.filePath, 'r', encoding='utf-8')  #파일경로 오픈
            self.rdr = csv.reader(f)                        #csv파일 읽기
            next((x for i, x in enumerate(self.rdr) if i == 0), None)   #첫줄 건너뛰기
        except:
            print("파일이 잘못 되었습니다.")

    # 인스턴스 메서드 선언
    def dataSetting(self):
        datas_dict = {}  #딕셔너리 생성
        posQuantity = {} #set 자료구조 생성
        for categorys in ExcleDataHandling.category:
            datas_dict[categorys] = [] #딕셔너리 자료구조에 각 항목 배열 생성.
        try:
            dataRemake = self.rdr
        except:
            return 1
        else:

            for line in dataRemake:
                i = 0
                for categorys in ExcleDataHandling.category :

                    if i <= 6 :
                        #기존 엑셀 데이터 입력.
                        datas_dict[categorys].append(line[i])
                    elif i == 7 :
                        #매매 가격 * 수량
                        transactionPrice = int(line[3]) * int(float(line[4]))
                        datas_dict[categorys].append(transactionPrice)
                    elif i == 8 :
                        #거래금액 * 수수료 퍼센트
                        fee = (float(int(line[3]) * int(float(line[4])) * self.fee))
                        datas_dict[categorys].append(fee)
                    elif i == 9 :
                        #dictionary 자료구조로 남은 보유 수량 검사
                        if line[2] == "매수" :
                            if posQuantity.get(line[1]) == None:
                                posQuantity[line[1]] = line[4]  #처음 매수한 종목이라면 매수량 만큼입력
                            else:
                                posQuantity[line[1]] = int(float(posQuantity[line[1]])) + int(float(line[4])) #매수후 또 매수(거의 없을듯..)
                        elif line[2] == "매도" :
                            if posQuantity.get(line[1]) == None:
                                posQuantity[line[1]] = line[4]  #매도할 종목이 없는데 매도? 에러코드 뿜어야할? 아니면 계좌에 이미 매수한 종목이 있을 경우..
                            else:
                                posQuantity[line[1]] = int(float(posQuantity[line[1]])) - int(float(line[4]))  #매수한 종목에서 매도수량만큼 빼기. 0되면 다 팔림.
                        datas_dict[categorys].append((posQuantity[line[1]]))

                    i += 1
            return datas_dict