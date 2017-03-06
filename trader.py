hello
from PyQt5.QAxContainer import *
import pandas as pd
from pandas import Series, DataFrame
import sqlite3


class Kiwoom(QAxWidget):


    def CommConnect(self):
        self.kiwoom.dynamicCall("CommConnect()")

    def OnEventConnect(self, errCode):
        if errCode == 0:
            print("로그인 성공")
        else:
            print("로그인 실패")


    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg):
        self.prev_next = PrevNext
        self.kiwoom.PreNext = PrevNext


        if RQName == "주식기본정보요청":
            _stock_code = self.CommGetData(TrCode, "", RQName, 0, "종목코드")
            _stock_name = self.CommGetData(TrCode, "", RQName, 0, "종목명")

            df = DataFrame(columns=('종목코드', '종목명'))

            df.loc[x] = [_stock_code, _stock_name, _iStockCount, _sDate, _sMasterConstruction]

            print(df.head())

            # 종목코드 .db
            con = sqlite3.connect("C:\WinPython\Sciprt\Bune_1.0\db\stock_info.db")
            df.to_sql('stock_info', con, if_exists='replace')

        elif RQName == "주식기관요청":
            Count = self.GetRepeatCnt(TrCode, RQName)
            print(TrCode, RQName, Count)

            _temp1 = self.CommGetData(TrCode, "", RQName, 0, "날짜")
            # _temp2 = self.CommGetData(sTrCode, "", RQName, 0, "종가")
            _temp2 = "hello"
            _temp3 = self.CommGetData(TrCode, "", RQName, 0, "대비")
            _temp4 = self.CommGetData(TrCode, "", RQName, 0, "기관기간누적")
            _temp5 = self.CommGetData(TrCode, "", RQName, 0, "기관일변순매매")
            _temp6 = self.CommGetData(TrCode, "", RQName, 0, "외국인일변순매매")
            _temp7 = self.CommGetData(TrCode, "", RQName, 0, "외국인지분율")

            print(_temp1, _temp2, _temp3, _temp4, _temp5, _temp6, _temp7)

        elif RQName == "주식외국인요청":
            Count = self.GetRepeatCnt(TrCode, RQName)
            print(TrCode, RQName, Count)


            print(self.CommGetData(TrCode, "", RQName, 0, "일자"),
                  self.CommGetData(TrCode, "", RQName, 0, "외국인한도"))


            if self.kiwoom.PreNext == "2":
                print("recall")
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005380")
                self.CommRqData("주식외국인요청", "OPT10009", 0, "0001")

        elif RQName == "주식호봉데이터":
            Count = self.GetRepeatCnt(TrCode, RQName)
            print(TrCode, RQName, Count)

            if Count > 0:
                tempDay = 0

                for idx in range(Count):

                    tempCurrentPrice = self.CommGetData(TrCode, "", RQName, idx, "현재가")
                    tempVolume = self.CommGetData(TrCode, "", RQName, idx, "거래량")
                    tmepTotalMoney = self.CommGetData(TrCode, "", RQName, idx, "거래대금")
                    tempDay = self.CommGetData(TrCode, "", RQName, idx, "일자")
                    tempStartPrice = self.CommGetData(TrCode, "", RQName, idx, "시가")
                    tempTopPrice = self.CommGetData(TrCode, "", RQName, idx, "고가")
                    tempLowPrice = self.CommGetData(TrCode, "", RQName, idx, "저가")
                    print(tempDay, tempCurrentPrice, self.kiwoom.PreNext)

            if self.kiwoom.PreNext == "2":
                print("recall")
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005380")
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기준일자", (tempDay))
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
                self.CommRqData("주식호봉데이터", "OPT10081", 2, "0001")



        else:
            print("일치하는 항목이 없습니다.")

        if RQName == "opt10081_req":
            cnt = self.GetRepeatCnt(TrCode, RQName)

            for i in range(cnt):
                date = self.CommGetData(TrCode, "", RQName, i, "일자")
                open = self.CommGetData(TrCode, "", RQName, i, "시가")
                high = self.CommGetData(TrCode, "", RQName, i, "고가")
                low  = self.CommGetData(TrCode, "", RQName, i, "저가")
                close  = self.CommGetData(TrCode, "", RQName, i, "현재가")
                volume  = self.CommGetData(TrCode, "", RQName, i, "거래량")

                self.ohlcv['date'].append(date)
                self.ohlcv['open'].append(int(open))
                self.ohlcv['high'].append(int(high))
                self.ohlcv['low'].append(int(low))
                self.ohlcv['close'].append(int(close))
                self.ohlcv['volume'].append(int(volume))

        if RQName == "opw00001_req":
            estimated_day2_deposit = self.CommGetData(TrCode, "", RQName, 0, "d+2추정예수금")
            estimated_day2_deposit = self.change_format(estimated_day2_deposit)
            self.data_opw00001 = estimated_day2_deposit

        if RQName == "opw00018_req":
            # Single Data
            single = []

            total_purchase_price = self.CommGetData(TrCode, "", RQName, 0, "총매입금액")
            total_purchase_price = self.change_format(total_purchase_price)
            single.append(total_purchase_price)

            total_eval_price = self.CommGetData(TrCode, "", RQName, 0, "총평가금액")
            total_eval_price = self.change_format(total_eval_price)
            single.append(total_eval_price)

            total_eval_profit_loss_price = self.CommGetData(TrCode, "", RQName, 0, "총평가손익금액")
            total_eval_profit_loss_price = self.change_format(total_eval_profit_loss_price)
            single.append(total_eval_profit_loss_price)

            total_earning_rate = self.CommGetData(TrCode, "", RQName, 0, "총수익률(%)")
            total_earning_rate = self.change_format(total_earning_rate, 1)
            single.append(total_earning_rate)

            estimated_deposit = self.CommGetData(TrCode, "", RQName, 0, "추정예탁자산")
            estimated_deposit = self.change_format(estimated_deposit)
            single.append(estimated_deposit)

            self.data_opw00018['single'] = single

            # Multi Data
            cnt = self.GetRepeatCnt(TrCode, RQName)
            for i in range(cnt):
                data = []

                item_name = self.CommGetData(TrCode, "", RQName, i, "종목명")
                data.append(item_name)

                quantity = self.CommGetData(TrCode, "", RQName, i, "보유수량")
                quantity = self.change_format(quantity)
                data.append(quantity)

                purchase_price = self.CommGetData(TrCode, "", RQName, i, "매입가")
                purchase_price = self.change_format(purchase_price)
                data.append(purchase_price)

                current_price = self.CommGetData(TrCode, "", RQName, i, "현재가")
                current_price = self.change_format(current_price)
                data.append(current_price)

                eval_profit_loss_price = self.CommGetData(TrCode, "", RQName, i, "평가손익")
                eval_profit_loss_price = self.change_format(eval_profit_loss_price)
                data.append(eval_profit_loss_price)

                earning_rate = self.CommGetData(TrCode, "", RQName, i, "수익률(%)")
                earning_rate = self.change_format(earning_rate, 2)
                data.append(earning_rate)

                self.data_opw00018['multi'].append(data)



    def go_func1(self):
        if self.GetConnectState() == 1:
            con = sqlite3.connect("C:\WinPython\Sciprt\Bune_1.0\db\stock_info.db")
            df = pd.read_sql("SELECT * FROM stock_info", con, index_col='index')

            for df:
                self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005380")
                self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "주식기본정보요청", "OPT10001", 0, "0001")
                print('request')

    def go_func2(self):
        if self.GetConnectState() == 1:
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005380")
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기준일자", "20170210")
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
            self.CommRqData("주식호봉데이터", "OPT10081", 0, "0001")

    def go_func3(self):
        if self.GetConnectState() == 1:
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", "005380")
            self.CommRqData("주식기관요청", "OPT10009", 0, "0001")

    def go_func4(self):
        if self.GetConnectState() == 1:
            self.CommRqData("주식기관요청", "OPT10009", 0, "0001")

    def go_func5(self):
        if self.GetConnectState() == 1:

            # 0 : 장내, 10 : 코스닥
            ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])

            # 서버에서 각 코드에 구분자로 ; 으로 전달됨
            _stock_code_list = ret.split(';')

            df = DataFrame(columns=('종목코드', '종목이름', '상장주식수', '상장일', '감리구분'))

            for x in _stock_code_list:
                _sCode = x
                _sName = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
                _iStockCount = self.kiwoom.dynamicCall("GetMasterListedStockCnt(QString)", [x])
                _sDate = self.kiwoom.dynamicCall("GetMasterListedStockDate (QString)", [x])
                _sMasterConstruction = self.kiwoom.dynamicCall("GetMasterConstruction (QString)", [x])

                df.loc[x] = [_sCode, _sName, _iStockCount, _sDate, _sMasterConstruction]

            print(df.head())

            con = sqlite3.connect("C:\WinPython\Sciprt\Bune_1.0\db\stock_info.db")
            df.to_sql('stock_info', con, if_exists='replace')

            print("save done.")












