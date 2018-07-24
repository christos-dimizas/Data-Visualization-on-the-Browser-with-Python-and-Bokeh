# Import Libraries
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from random import randrange

# Create figure
f = figure(x_range=(0, 11), y_range=(0, 11))

# Create Column data source
source = ColumnDataSource(dict(x=[], y=[]))

# Create glyphs
f.circle(x='x', y='y', color='olive', line_color='yellow', source=source)
f.line(x='x', y='y', source=source)


def update():
    new_data = dict(x=[randrange(1, 10)], y=[randrange(1, 10)])
    source.stream(new_data, rollover=15)
    print(source.data)


# Add figure to curdoc and configure callback
curdoc().add_root(f)
curdoc().add_periodic_callback(update, 1000)
