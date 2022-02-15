#-*-coding: utf-8-*-
import os
from fpdf import FPDF
import datetime
import Price_Expect
from time import localtime, strftime


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
    
    def setdata(self, stock_data, target_rate, expect_rate):
        self.stock_data = stock_data
        self.target_rate = target_rate
        self.expect_rate = expect_rate

    def data_print(self):
        for data in self.stock_data:
            print(data)
            print("\n")

    def header(self):
        self.image('C:/Users/User/Desktop/CRA_image.jpg', 10, 8, 15)
        self.set_font('Arial', 'B', 14)
        self.ln(5)
        self.cell(-10)
        self.cell(210, 1, 'Stock Analysis Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, image, data, profit):
        self.image(image, 0, 20, self.WIDTH)
        self.set_font('Arial', 'B', 10)

        start = 170
        for element in data:
            self.text(30, start, element)
            start += 7


        self.set_font('Arial', 'B', 12)

        self.text(135, 170, "Target rate of return : " + str(self.target_rate) + "%")
        self.text(135, 177, "Expected rate of return : " + str(round(profit,2)) + "%")

        if float(self.target_rate) <= round(profit,2) :
            self.set_text_color(71,200,62)
            self.text(135, 185, "Suitablilty : GOOD")
        else:
            self.set_text_color(255,0,0)
            self.text(135, 185, "Suitablilty : BAD")

        self.set_text_color(0,0,0)
            
    def print_page(self, images, data, profit):
        # Generates the report
        self.add_page()
        self.page_body(images, data, profit)

    def make_pdf(self, profit_list):
        PLOT_DIR = "C:/Users/User/Desktop/Study/Test/"
        os.chdir(PLOT_DIR)
        files = os.listdir(PLOT_DIR)
        print(files)

        for i in range(0, len(files)):
            for j in range(0, len(files)):
                if datetime.datetime.fromtimestamp(os.path.getmtime(PLOT_DIR + files[i])) < datetime.datetime.fromtimestamp(os.path.getmtime(PLOT_DIR+files[j])):
                    (files[i], files[j]) = (files[j], files[i])

        for element, data, profit in zip(files, self.stock_data, profit_list):
            self.print_page(element, data, profit)

        self.output('Stock_Analysis_Report.pdf', 'F')
        print("PDF is made")










