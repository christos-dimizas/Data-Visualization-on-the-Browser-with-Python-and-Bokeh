from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select
from bokeh.plotting import figure
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians
from pytz import timezone
from bokeh.layouts import layout


# create web scraping function
def extract_value(marketname='bitmarketEUR'):
    print(marketname)
    r = requests.get("http://bitcoincharts.com/markets/" + marketname + ".html", headers={'User-Agent': 'Mozilla/5.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    value_raw = soup.find_all("p")
    value_net = float(value_raw[0].span.text)
    return value_net


# create periodic function
def update():
    new_data = dict(x=[datetime.now(tz=timezone('Europe/Moscow'))], y=[extract_value(select.value)])
    source.stream(new_data, rollover=200)
    print(source.data)


def selectupdate(attr, old, new):
    source.data = dict(x=[], y=[])
    update()


# create figure
f = figure()

f.xaxis.formatter = DatetimeTickFormatter(
    seconds=["%Y-%m-%d-%H-%m-%S"],
    minsec=["%Y-%m-%d-%H-%m-%S"],
    minutes=["%Y-%m-%d-%H-%m-%S"],
    hourmin=["%Y-%m-%d-%H-%m-%S"],
    hours=["%Y-%m-%d-%H-%m-%S"],
    days=["%Y-%m-%d-%H-%m-%S"],
    months=["%Y-%m-%d-%H-%m-%S"],
    years=["%Y-%m-%d-%H-%m-%S"],
)

f.xaxis.major_label_orientation = radians(45)

# create ColumnDataSource
source = ColumnDataSource(dict(x=[], y=[]))

# Create select Widget
options = [('bitmarketEUR', 'bitmarket EUR'), ('btcnCNY', 'btcn CNY')]
select = Select(title='Market name', value='bitmarketEUR', options=options)
select.on_change("value", selectupdate)

# create glyphs
f.circle(x='x', y='y', color='olive', line_color='brown', source=source)
f.line(x='x', y='y', source=source)

# add figure to curdoc and configure callback
lay_out = layout([[f], [select]])
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 2000)
