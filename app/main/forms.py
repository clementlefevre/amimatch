from flask.ext.wtf import Form
from wtforms import SubmitField
from wtforms.fields.html5 import DateField


class DateRangeForm(Form):
    date_from = DateField('DatePicker', format='%Y-%m-%d')
    date_to = DateField('DatePicker', format='%Y-%m-%d')

    submit = SubmitField('Search images')
