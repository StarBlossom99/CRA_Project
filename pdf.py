import os
from fpdf import FPDF


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

    def page_body(self, image):
        self.image(image, 0, 25, self.WIDTH)
            
    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)

    def make_pdf(self):
        PLOT_DIR = "C:/Users/User/Desktop/Study/Test"
        os.chdir(PLOT_DIR)
        files = os.listdir(PLOT_DIR)
        print(files)


        for element in files:
            self.print_page(element)

        self.output('Stock_Analysis_Report.pdf', 'F')
        print("PDF is made")







