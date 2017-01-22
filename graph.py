import MySQLdb
from highcharts import Highchart
from datetime import datetime

start = datetime.now()

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="minion")

query = """
SELECT ts, t, lux FROM report WHERE id = 1 and ts >= now() - INTERVAL 14 DAY
"""

dictCursor = conn.cursor(MySQLdb.cursors.Cursor)
dictCursor.execute(query)
data = dictCursor.fetchall()

temperature = []
lux = []
for row in data:
    temperature.append([ int( row[0].strftime('%s')), float(row[1]), ])
    if row[2]:
        lux.append([ int( row[0].strftime('%s')), -float(row[2]), ])

chart = Highchart()

options = {
            'chart': {
                'zoomType': 'x'
            },
            'title': {
                'text': 'Minion 1'
            },
            'xAxis': {
                'type': 'datetime'
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

chart.add_data_set(temperature, series_type='line', name='m1.temp', yAxis=0)
chart.add_data_set(lux, series_type='line', name='m1.lux', yAxis=1)

chart.save_file()


duration = datetime.now() - start
print duration.seconds, 's'
