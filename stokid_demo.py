#-*-coding: utf-8-*-
import pandas as pd
import pymysql 
import os
import datetime
import time
import price_chart
import DataLoad
import DetailFilter
import MySql_Filter
import Return_Expect
from pykiwoom.kiwoom import *

theme_code_list = ['141', '140','571','570','830','501','562','561','560','572','600','500','458','452','353','250','170','202','319','201','200','471','470','312','270','245','160','210','211','480','610','316','213','456','517','281','280','130','360','363','361','362','550','551','557','556',
'555','552','554','553','212','313','290','453','420','421','611','171','315','530','459','310','364','810','515','516','203','318','370','286','820','154','261','800','214','232','230','231','110','111','314','311','400','351','352','350','256','255','242','241','240','243','215','262',
'454','455','450','317','180','181','223','220','222','221','300','910','430','410','260','284','282','283','285','451','920','900','457','244','153','520','103','102','101','100','481','850','121','172','152','151','150','291','120','330','840','511','518','510','514','513','512','173']

print_sql_part = "종목코드 , 종목명, 연중최고, 연중최저, 시가총액, PER, EPS, ROE, PBR, EV, BPS, 매출액, 영업이익, 당기순이익, 현재가, Theme, Dividends, Dividends_Rate"


interest_rate = 0.0219

# 프로그램 시작
print("=" * 70)
print("Welcome to StocKid Program")
print("=" * 70)
#데이터 새로 불러올것인지(login 할지 안할지 여부)
data_load_check = input("Do you want to load new data? (Y for Yes) : ")
if data_load_check == 'Y':
    # Data 다운끝나면 프로그램 종료할지
    exit_check = input("End the program after downloading? (Y for Yes) : ")
    data = DataLoad.dataload()
    data.setdata()
    data.settoday("20220203")
    data.download()
    if exit_check == "Y":
        exit()


# #DB table csv 파일로 빼는 part

while True:
    # 투자 기간 입력
    period = input("Please enter the period(month) you want to invest in : ")
    # print(period)

    # 목표 수익률 입력
    target_rate = input("\nPlease enter your target rate(%) of return : ")
    # print(target_rate)

    theme_exist = input("\nIs there any field you want to invest in ? (Y for yes , N for anything else) : ")
    if theme_exist == 'Y':
        while True :
            #테마 코드 리스트 출력
            print("="*200)
            print("%-18s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-18s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-18s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-24s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-25s\t%s\t%-17s\t%s\t%-25s\t%s\t%-25s\t%s\n\n%-25s\t%s\t%-17s\t%s\t%-17s\t%s\t%-25s\t%s\t%-17s\t%s\n\n%-17s\t%s\t%-25s\t%s" % ('2차전지_소재(양극화물질등)','141','2차전지_완제품','140','AMOLED_소재','571','AMOLED_장비','570','Cheap-Chic_저가실용품','830','FPCB(연성회로기판)','501','LCD_부품                   ','562','LCD_소재','561','LCD_장비','560','LED','        572','LPG(액화석유가스)','600','PCB(인쇄회로기판)','500','SI(시스템통합)','458','SNS(Social Network Service)','452','U-헬스케어','353','가구','250','강관','170','거푸집','202','건강식품','319','건설_국내주택','201','건설_해외건설','200','게임_모바일','471','게임_온라인','470','곡물가공품_설탕/밀가루/유지','312','교육','270','그린카_하이브리드카/전기차','245','금형/몰드베이스','160','기계_건설기계','210','기계_공작기계','211','네트워크/광통신','480','도시가스','610','라면','316','로봇_지능형','213','모바일솔루션','456','무선충전기관련주','517','미디어_디지털방송전환','281','미디어_방송광고','280','바이오_디젤/에탄올','130','바이오_바이오시밀러/베터','360','바이오_유전체분석','363','바이오_줄기세포치료제','361','바이오_진단/백신','362','반도체_생산','550','반도체_설계(fabless)','551','반도체_시스템반도체','557','반도체_전공정소재','556','반도체_전공정장비','555','반도체_후공정','552','반도체_후공정소재','554','반도체_후공정장비','553','방위산업','212','배합사료','313','백화점','290','보안_인터넷','453','보험_생명보험','420','보험_손해보험','421','부탄가스','611','비철금속주','171','빙과','315','셋톱박스','530','소프트웨어_자동차용','459','수산물/수산가공품','310','슈퍼박테리아','364','스마트 그리드','810','스마트폰_삼성전자관련주','515','스마트폰_애플 관련주','516','시멘트','203','식자재유통','318','신약개발/기술수출','370','에니메이션','286','엔젤산업','820','엔지니어링 플라스틱','154','여행','261','온실가스배출저감','800','우주항공','214','운송_육상운송','232','운송_항공','230','운송_해운','231','원자력_기자재','110','원자력_설계시공','111','유가공','314','육계','311','은행','400','의료기기','351','의료기기_안과','352','의료기기_치아','350','의복_OEM','256','의복_아웃도어','255','자동차_블랙박스관련주','242','자동차_전장화 수혜','241','자동차_차량경량화 수혜','240','자동차_차량용 반도체','243','자원개발 E&P','215','전기자전거','262','전자결제','454','전자결제_B2B','455','전자책_e-book','450','제과스낵','317','제지_골판지','180','제지_기타','181','조선_Eco선','223','조선_LNG보냉재','220','조선_해양플랜트','222','조선_해양플랜트기자재','221','주류','300','중국_내수소비 확대','910','증권','430','창투','410','카지노','260','컨텐츠_메니지먼트','284','컨텐츠_영상','282','컨텐츠_음원','283','컨텐츠_한류','285','컴퓨터전화통합(CTI)','451','코스닥_라이징스타','920','코스닥_히든챔피언','900','클라우드 컴퓨팅','457','타이어','244','탄소섬유','153','태블릿 PC','520','태양광_발전/설치/운영','103','태양광_부품/소재/장비','102','태양광_잉곳/웨이퍼/셀/모듈','101','태양광_폴리실리콘','100','통신장비','481','폐기물처리','850','풍력_단조/기자재','121','합금철','172','합성고무','152','합성섬유_원료','151','합성수지','150','홈쇼핑','291','화력_발전기자재','120','화장품','330','환경산업','840','휴대폰_RF부품','511','휴대폰_베트남현지법인','518','휴대폰_수동부품','510','휴대폰_카메라','514','휴대폰_케이스/기구물','513','휴대폰_터치스크린','512','희소금속','173'))
            print("="*200)
            #테마 입력
            theme_code = input("\nLook at the theme code list and enter the code for the field you want to invest in. : ")
            if str(theme_code) in theme_code_list:
                break;
            else:
                print("\ntheme code %s doesn't exist in code list, please try again" % theme_code)
                continue;

    # 추천 받고 싶은 종목의 개수를 입력
    while True:
        count = input("\nHow many stocks would you like to recommend? (1 to 15) : ")
        if int(count) >= 1 and int(count) <= 15:
            break;
        else:
            print("\nplease input valid input (1 to 15)")
            continue;
    
    det = DetailFilter.filter()

    det.first()
    det.make_filter()

    min = det.return_filter("min")
    max = det.return_filter("max")

    sql_filter = MySql_Filter.filter()
    # sql_filter.table_show()

    #sql에서 검색하는 날짜 기준
    sql_filter.setdate("20220203")

    sql_filter.setdata(min, max, det.check(), count)

    if theme_exist == 'Y':
        sql_filter.getTheme(theme_exist, theme_code)
    else:
        sql_filter.getNoTheme(theme_exist)

    sql_filter.filtering()
    sql_filter.filtering_show()
    
    code_list = sql_filter.code_list
    name_list = sql_filter.name_list


    print("\n")
    # print(code_list)
    # print(name_list)

    # code list to chart// Chart 생성 함수 클래스로 구현 완료
    for index, code in enumerate(code_list, start= 1):
        today = "20220203" #sql 에서 가져오는 날짜의 기준
        inst = price_chart.graph()
        inst.setdata(code, today, name_list[index-1])
        inst.make_graph()

    print("The stock price chart of the selected stocks has been created.\n\n")

    print("<Expected Return Rate on the selected stocks>\n\n")
    # 기대 수익률 계산 후 출력
    return_expected = Return_Expect.Rt_expect()
    return_expected.setdata(interest_rate, today, code_list, float(target_rate))
    return_expected.make_return_expect()
    return_expected.make_return_list()
    return_expected.print_result()

    break;

print("program ends")

# GUI? Class 분리, 날짜 문제 해결(장 종료 후에 6시간 동안 돌려서 그 다음날 이용 가능하도록?)


