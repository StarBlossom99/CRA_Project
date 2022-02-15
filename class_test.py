import py_compile
import Price_Chart
import Data_Load
import Detail_Filter

# a = price_chart.graph()
# a.setdata("005930", "20220119", "삼성전자")
# a.make_graph()


# sample = DataLoad.dataload()
# sample.setdata(2, "C:\CRAproject/test/")
# sample.download()

det = Detail_Filter.filter()

det.first()
det.make_filter()

min = det.return_filter("min")
max = det.return_filter("max")

print(min)
print(max)