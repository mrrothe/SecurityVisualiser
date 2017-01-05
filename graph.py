import sqlite3 as sql
from pandas import DataFrame
import datetime
from bokeh.layouts import row,column
from bokeh.charts import Bar, Line
from bokeh.plotting import figure, curdoc
from bokeh.models import Label, CustomJS, Slider, Button, TextInput


con = sql.connect('fwlog.db')
endDate=datetime.date.today()
one_day = datetime.timedelta(days=4)
startDate = endDate - one_day
with con:
    cur = con.cursor()
    topIPs=cur.execute("SELECT sourceIP,count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "' group by sourceIP order by count(id) desc LIMIT 15")
    cur = con.cursor()
    total=cur.execute("SELECT count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "'")
    cur = con.cursor()
    countries=cur.execute("SELECT geo,count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "' group by geo order by count(id) desc LIMIT 15")
    cur = con.cursor()
    rate=cur.execute("SELECT strftime('%Y-%m-%d %H:%M', timestamp),count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "' group by strftime('%Y-%m-%d %H:%M', timestamp) order by timestamp asc")
    cur = con.cursor()
    ratet=cur.execute("SELECT strftime('%Y-%m-%d %H', timestamp),count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "' group by strftime('%Y-%m-%d %H', timestamp) order by timestamp asc")
    cur = con.cursor()
#    rateh=cur.execute("SELECT substr(timestamp,0,14),count(id) FROM firewall group by substr(timestamp,0,14) order by timestamp asc")
dfIP = DataFrame(topIPs.fetchall(),columns=('IP','Count'))
dfGeo = DataFrame(countries.fetchall(),columns=('Country','Count'))
p = Bar(dfIP,label='IP',values='Count', legend=False, webgl=True)
data = DataFrame(rate.fetchall(),columns=('timestamp','rate'))
datat = DataFrame(ratet.fetchall(),columns=('timestamp','rate'))
#datah = DataFrame(rateh.fetchall(),columns=('timestamp','rate'))
p2 = Line(data, title="Attack Rate", xlabel='timestamp', ylabel='rate (60s Interval)', width=400, height=400)
p2t = Line(datat, title="Attack Rate", xlabel='timestamp', ylabel='rate (10m Interval)', width=400, height=400)
#p2h = Line(datah, title="Attack Rate", xlabel='timestamp', ylabel='rate (1h Interval)', width=400, height=400)
p3 = Bar(dfGeo,label='Country',values='Count', color='blue', legend=False)
#totaltext=''.join(total.fetchall())
totaltext=str(total.fetchall()[0])
def callback():
    print(hist_slider.value)
    endDate=datetime.date.today()
    one_day = datetime.timedelta(days=hist_slider.value)
    startDate = endDate - one_day
    with con:
        cur = con.cursor()
        topIPs=cur.execute("SELECT sourceIP,count(id) FROM firewall WHERE strftime('%Y-%m-%d', timestamp) BETWEEN '" + str(startDate) + "' AND '" + str(endDate) + "' group by sourceIP order by count(id) desc LIMIT 15")
    dfIP = DataFrame(topIPs.fetchall(),columns=('IP','Count'))
    p = Bar(dfIP,label='IP',values='Count', legend=False, webgl=True)
    curdoc().add_root(row(p))    


hist_slider = Slider(start=1, end=30, value=4, step=1, title="Previous Days to Show")
hist_button = Button(label="Update")
hist_button.on_click(callback)
#print(totaltext)
labels = Label(x=2, y=3850, text=totaltext)
p.add_layout(labels)
curdoc().add_root(row(p,p3,column(hist_slider,hist_button)))
curdoc().add_root(row(p2,p2t))
