import os
from fpdf import FPDF
PLOT_DIR = "C:/Users/User/Desktop/Study/Test"
os.chdir(PLOT_DIR)
files = os.listdir(PLOT_DIR)
print(files)

pages_data = []
temp = []
counter = 0

for fname in files:
        # We want 3 per page
        if counter == 3:
            pages_data.append(temp)
            temp = []
            counter = 0

        temp.append(f'{fname}')
        counter += 1

file_zip =[files]
print(file_zip)
print(temp)
print(pages_data)
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        self.image('IU.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Sales report', 0, 0, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            
    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)

pdf = PDF()

for element in pages_data:
    pdf.print_page(element)

pdf.output('SalesReport.pdf', 'F')

print("PDF is made")
