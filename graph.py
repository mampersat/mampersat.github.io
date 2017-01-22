import MySQLdb
from highcharts import Highchart
from datetime import datetime

start = datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="minion")

query = """
SELECT ts, t FROM report WHERE id = 1 and ts >= now() - INTERVAL 1 DAY;
"""

dictCursor = conn.cursor(MySQLdb.cursors.Cursor)
dictCursor.execute(query)
data = dictCursor.fetchall()

r = []
for row in data:
    r.append([row[0], float(row[1]), ])

chart = Highchart()
chart.add_data_set(r, series_type='line', name='Example Series')
chart.save_file()

duration = datetime.now() - start
print duration.seconds, 's'
