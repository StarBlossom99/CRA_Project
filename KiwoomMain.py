import sys
from PyQt5.QtWidgets import *
import KiwoomAPI
from Config import *

class KiwoonMain:
    def __init__(self):
        self.kiwoom = KiwoomAPI.KiwoomAPI()
        self.kiwoom.CommConnect()

    def OPT10001(self):
        self.kiwoom.output_list = output_list['OPT10001']

        self.kiwoom.SetInputValue("종목코드", "005930")
        self.kiwoom.CommRqData("OPT10001", "OPT10001", 0, "0101")

        return self.kiwoom.ret_data['OPT10001']


app = QApplication(sys.argv)
api_con = KiwoonMain()

result = api_con.OPT10001()
print(result['Data'][0])