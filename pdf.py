#-*-coding: utf-8-*-
import os
from fpdf import FPDF
import datetime
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

    def page_body(self, image, data):
        self.image(image, 0, 20, self.WIDTH)
        self.set_font('Arial', 'B', 10)

        start = 170
        for element in data:
            self.text(30, start, element)
            start += 7
            
    def print_page(self, images, data):
        # Generates the report
        self.add_page()
        self.page_body(images, data)

    def make_pdf(self):
        PLOT_DIR = "C:/Users/User/Desktop/Study/Test/"
        os.chdir(PLOT_DIR)
        files = os.listdir(PLOT_DIR)
        print(files)

        for i in range(0, len(files)):
            for j in range(0, len(files)):
                if datetime.datetime.fromtimestamp(os.path.getmtime(PLOT_DIR + files[i])) < datetime.datetime.fromtimestamp(os.path.getmtime(PLOT_DIR+files[j])):
                    (files[i], files[j]) = (files[j], files[i])

        for element, data in zip(files, self.stock_data):
            self.print_page(element, data)

        self.output('Stock_Analysis_Report.pdf', 'F')
        print("PDF is made")







