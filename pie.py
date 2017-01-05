from bokeh.charts import Donut
from bokeh.plotting import figure, curdoc
from pandas import DataFrame

pie_data = {'a':['Work', 'Eat', 'Commute', 'Sport', 'Watch TV','Sleep'],'b':[8, 2, 2, 4, 0, 8]}
data = DataFrame(pie_data,columns=('a','b'))
print data
p4 = Donut(data,label='a',values='b')
curdoc().add_root(p4)
