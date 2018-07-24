# Import libraries
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

# Prepare data
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 10]

# Prepare the output file
# output_file("Line.html")

# Create a figure object
f = figure()

# Create line plot
f.line(x, y)

js, div = components(f)

cdn_js = CDN.js_files[0]
cdn_css = CDN.css_files[0]

# write the plot in the figure object
# show(f)
