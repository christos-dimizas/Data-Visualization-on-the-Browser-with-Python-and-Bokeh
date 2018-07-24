# importing libraries
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.annotations import LabelSet
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Select, RadioButtonGroup, Slider
from bokeh.layouts import layout

# crate columndatasource
source_original = ColumnDataSource(dict(average_grades=[7, 8, 10],
                                        exam_grades=[6, 9, 8],
                                        student_names=["Stephan", "Helder", "Riazudidn"]))

source = ColumnDataSource(dict(average_grades=[7, 8, 10],
                               exam_grades=[6, 9, 8],
                               student_names=["Stephan", "Helder", "Riazudidn"]))
# create the figure
f = figure(
    x_range=Range1d(start=0, end=12),
    y_range=Range1d(start=0, end=12)
)

# add labels for glyphs
labels = LabelSet(x="average_grades", y="exam_grades", text="student_names", x_offset=5, y_offset=5, source=source)
f.add_layout(labels)

# create glyphs
f.circle(x="average_grades", y="exam_grades", source=source, size=8)


# create on select change function
def select_update_labels(attr, old, new):
    labels.text = select.value
    print(attr, old, new)


# Create on radio change function
def radio_update_labels(attr, old, new):
    labels.text = radioOptions[radio_button_group.active]
    print(attr, old, new)


# Create on slider change function
def filter_grades(attr, old, new):
    for key in source_original.data:
        source.data[key] = []
        for (i, value) in enumerate(source_original.data[key]):
            if source_original.data['exam_grades'][i] >= slider.value:
                source.data[key] += [value]

    # Below is a more elaborate technique
    # source.data = {
    #     key: [
    #         value for i, value in enumerate(source_original.data[key])
    #         if source_original.data['exam_grades'][i] >= slider.value
    #     ]
    #     for key in source_original.data
    # }

    print(source.data)


# Select widget
selectOptions = [("average_grades", "Average Grades"), ("exam_grades", "Exam Grades"),
                 ("student_names", "Student Names")]
select = Select(title="Attribute", options=selectOptions)
select.on_change("value", select_update_labels)

# Radio Group Widget
radioOptions = ["average_grades", "exam_grades", "student_names"]
radio_button_group = RadioButtonGroup(labels=radioOptions)
radio_button_group.on_change("active", radio_update_labels)

# Slider Widget
slider = Slider(
    start=min(source_original.data['exam_grades']) - 1,
    end=max(source_original.data["exam_grades"]) + 1,
    value=8,
    step=0.1,
    title="Exam Grade: "
)
slider.on_change("value", filter_grades)

# Slider widget

# create layout and add to curdoc
lay_out = layout([[select], [radio_button_group], [slider]])
curdoc().add_root(f)
curdoc().add_root(lay_out)
