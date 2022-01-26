import py_compile
import price_chart

a = price_chart.graph()
a.setdata("005930", "20220119", "삼성전자")
a.make_graph()


