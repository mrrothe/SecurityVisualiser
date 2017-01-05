import sqlite3 as sql
from pandas import DataFrame
con = sql.connect('fwlog.db')
with con:
	cur = con.cursor() #Min
rate=cur.execute("SELECT timestamp,ip FROM firewall order by timestamp asc LIMIT 200")

ratedata=rate.fetchall()
print(ratedata)
data = DataFrame(ratedata,columns=('timestamp','rate'))
#p2 = Line(data, title="Attack Rate", xlabel='timestamp', ylabel='rate (60s Interval)', width=400, height=400)

