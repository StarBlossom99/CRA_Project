
class filter:
    det_min = [0,0,0,0,0,0,0,0,0,0,0,0]
    det_max = [0,0,0,0,0,0,0,0,0,0,0,0]

    def first(self):
        detail_filter = input("\nDo you want to use detail filter? (Y for yes , N for anything else) : ")
        self.detail_filter = detail_filter
    def return_filter(self, type):
        if type == "min":
            return self.det_min
        elif type == "max":
            return self.det_max
            
    def check(self):
        return self.detail_filter

    def make_filter(self):
        if self.detail_filter == "Y":
            print("\nDetailed filter is used.\n")
            #세부 필터 입력 받기
            while True:
                #필터 코드 입력 받기
                detail_code = 0
                while True:
                    print("%-15s\t%-15s\t%-15s\t%-15s\n%-15s\t%-15s\t%-15s\t%-15s\n%-15s\t%-15s\t%-15s\t%-15s\n" % ("1. Market Cap(시가 총액)", "2. PER(주가수익률)", "3. EPS(주당 순이익)", "4. ROE(자기자본 이익률)" , "5, PBR(주가 순 자산비율)", "6. EV(기업 가치)", "7. BPS(주당 순 자산가치)", "8. Sales(매출액)", "9. Operating Profit(영업 이익)", "10. Net Profit(당기 순이익)", "11. Dividends(배당금)", "12. Dividend Yield(배당 수익률)"))
                    detail_code = input("\nPlease enter the number of the filter you want to use (1 to 12) : ")
                    # 필터 코드 검사
                    if int(detail_code) >= 1 and int(detail_code) <= 12:
                        break;
                    else:
                        print("please input valid detail code (1 to 12)")
                        continue;

                detail_code = int(detail_code)       
                # 필터 코드 switch loop
                if detail_code == 1:
                    while True:
                        print("\nPlease enter the Market Cap(시가 총액) range. (unit : 100 million won)")
                        self.det_min[0] = input("\nPlease enter the minimum value : ")
                        self.det_max[0] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[0]) >= int(self.det_max[0]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 2:
                    while True:
                        print("\nPlease enter the PER(주가수익률) range.")
                        self.det_min[1] = input("\nPlease enter the minimum value : ")
                        self.det_max[1] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[1]) >= int(self.det_max[1]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 3:
                    while True:
                        print("\nPlease enter the EPS(주당 순이익) range. (unit : won)")
                        self.det_min[2] = input("\nPlease enter the minimum value : ")
                        self.det_max[2] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[2]) >= int(self.det_max[2]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 4:
                    while True:
                        print("\nPlease enter the ROE(자기자본 이익률) range. ")
                        self.det_min[3] = input("\nPlease enter the minimum value : ")
                        self.det_max[3] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[3]) >= int(self.det_max[3]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 5:
                    while True:
                        print("\nPlease enter the PBR(주가 순 자산비율) range.")
                        self.det_min[4] = input("\nPlease enter the minimum value : ")
                        self.det_max[4] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[0]) >= int(self.det_max[4]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 6:
                    while True:
                        print("\nPlease enter the EV(기업 가치) range.")
                        self.det_min[5] = input("\nPlease enter the minimum value : ")
                        self.det_max[5] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[5]) >= int(self.det_max[5]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 7:
                    while True:
                        print("\nPlease enter the BPS(주당 순 자산가치) range.")
                        self.det_min[6] = input("\nPlease enter the minimum value : ")
                        self.det_max[6] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[6]) >= int(self.det_max[6]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 8:
                    while True:
                        print("\nPlease enter the Sales(매출액) range. (unit : 100 million won)")
                        self.det_min[7] = input("\nPlease enter the minimum value : ")
                        self.det_max[7] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[7]) >= int(self.det_max[7]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 9:
                    while True:
                        print("\nPlease enter the Operating Profit(영업 이익) range. (unit : 100 million won)")
                        self.det_min[8] = input("\nPlease enter the minimum value : ")
                        self.det_max[8] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[8]) >= int(self.det_max[8]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 10:
                    while True:
                        print("\nPlease enter Net Profit(당기 순이익) range. (unit : 100 million won)")
                        self.det_min[9] = input("\nPlease enter the minimum value : ")
                        self.det_max[9] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[9]) >= int(self.det_max[9]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 11:
                    while True:
                        print("\nPlease enter the Dividends(배당금) range. (unit : won)")
                        self.det_min[10] = input("\nPlease enter the minimum value : ")
                        self.det_max[10] = input("\nPlease enter the maximum value : ")
                        if int(self.det_min[10]) >= int(self.det_max[10]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;
                elif detail_code == 12:
                    while True:
                        print("\nPlease enter the Dividends_Rate Yield(배당 수익률) range. ")
                        self.det_min[11] = input("\nPlease enter the minimum value : ")
                        self.det_max[11] = input("\nPlease enter the maximum value : ")
                        if float(self.det_min[11]) >= float(self.det_max[11]):
                            print("maximun value is less than minimum value, please enter valid input")
                            continue;
                        else:
                            break;

                # 추가 필터 사용할 것인지 묻기
                detail_filter_check = input("\nDo you want to use another filter? (Y for Yes) : ")
                if detail_filter_check == 'Y':
                    continue;
                else:
                    break;
                # 필터 입력 종료
        else:
            print("\nDetailed filter is not used.\n")



