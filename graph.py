import MySQLdb
from highcharts import Highchart
from datetime import datetime

start = datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="minion")

query = """
SELECT ts, t FROM report WHERE id = 1 and ts >= now() - INTERVAL 14 DAY;
"""

dictCursor = conn.cursor(MySQLdb.cursors.Cursor)
dictCursor.execute(query)
data = dictCursor.fetchall()

r = []
for row in data:
    r.append([row[0], float(row[1]), ])

chart = Highchart()

options = {
            'chart': {
                'zoomType': 'x'
            },
            'title': {
                'text': 'Minion 1 Temperature'
            },
    }

chart.set_dict_options(options)

chart.add_data_set(r, series_type='line', name='Example Series')
chart.save_file()

duration = datetime.now() - start
print duration.seconds, 's'
