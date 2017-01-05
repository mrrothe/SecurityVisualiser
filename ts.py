import pandas as pd
import sqlite3 as sql
from bokeh.charts import show, Line
from bokeh.layouts import column
from bokeh.plotting import curdoc
con = sql.connect('fwlog.db')
with con:
    cur = con.cursor()
    rate=cur.execute("SELECT substr(timestamp,0,16),count(id) FROM firewall group by substr(timestamp,0,17) order by timestamp asc")
data = pd.DataFrame(rate.fetchall(),columns=('timestamp','rate'))
#print(data)
p = Line(data, title="Attack Rate", xlabel='timestamp', ylabel='rate', width=400, height=400)

curdoc().add_root(p)