from numpy import dtype
from pykiwoom.kiwoom import *
import datetime
import time

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect()

# 전종목 종목코드
kospi = kiwoom.GetCodeListByMarket('0')
kosdaq = kiwoom.GetCodeListByMarket('10')


# 문자열로 오늘 날짜 얻기
now = datetime.datetime.now()
today = now.strftime("%Y%m%d")

# 전 종목의 일봉 데이터
for i, code in enumerate(kospi):
    print(f"kospi : {i}/{len(kospi)} {code}")
    df = kiwoom.block_request("opt10001",
                              종목코드=code,
                              output="주식기본정보",
                              next=0)

    out_name = f"kospi_{code}.csv"
    df.to_csv(out_name)
    time.sleep(3.6)

for i, code in enumerate(kosdaq):
    print(f"kosdaq : {i}/{len(kosdaq)} {code}")
    df = kiwoom.block_request("opt10001",
                              종목코드=code,
                              output="주식기본정보",
                              next=0)

    out_name = f"kosdaq_{code}.csv"
    df.to_csv(out_name)
    time.sleep(3.6)