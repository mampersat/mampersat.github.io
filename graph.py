import MySQLdb
from highcharts import Highchart
from datetime import datetime

start = datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="minion")

query = """
SELECT id, ts, t, lux FROM report WHERE ts >= now() - INTERVAL 5 DAY
"""

dictCursor = conn.cursor(MySQLdb.cursors.Cursor)
dictCursor.execute(query)
data = dictCursor.fetchall()

t1 = []
t2 = []
lux = []
for row in data:
    if row[0] == 1:
        t1.append([ int( row[1].strftime('%s'))*1000, float(row[2]), ])
        if row[3]:
            lux.append([ int( row[1].strftime('%s'))*1000, -float(row[3]), ])

    if row[0] == 2:
        t2.append([ int( row[1].strftime('%s'))*1000, float(row[2]), ])

chart = Highchart()

options = {
            'chart': {
                'zoomType': 'x'
            },
            'title': {
                'text': 'Minions'
            },
            'xAxis': {
                'type': 'datetime',
            },
            'yAxis': [{
                    'title': {
                        'text':'temperature'
                    },
                },{
                    'title': {
                        'text': 'lux',
                    },
                    'opposite': 'true'
                } ]
        }

chart.set_dict_options(options)

chart.add_data_set(t1, series_type='line', name='m1.temp', yAxis=0)
chart.add_data_set(t2, series_type='line', name='m2.temp', yAxis=0)
chart.add_data_set(lux, series_type='line', name='m1.lux', yAxis=1)

chart.save_file()


duration = datetime.now() - start
print duration.seconds, 's'
