import sqlite3 as sql
from pandas import DataFrame
con = sql.connect('logs.db')
with con:    
    cur = con.cursor()    
    rate=cur.execute("SELECT timestamp,count(id) FROM firewall group by timestamp order by timestamp desc limit 800")
df2 = DataFrame(rate.fetchall(),columns=('Time','Count'))
print(df2)

