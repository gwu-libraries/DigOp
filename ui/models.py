from datetime import datetime
from datetime import timedelta
import time

from django.db import models
from django import forms
from django.contrib.auth.models import User, UserManager
from django.forms import ModelForm


# Create your models here.

TYPES = (
    ('Scan','Scan'),
    ('QC','QC'),
    ('QA','QA'),
    )

ITEMS = (
    ('Book','Book'),
    ('Map','Map'),
    ('Microfilm','Microfilm'),
    )

class Item(models.Model):
    barcode = models.CharField(max_length=50)
    totalPages = models.IntegerField(blank = True )
    itemType = models.CharField(max_length = 10, choices = ITEMS)
    def __unicode__(self):
        return self.barcode



class ProcessingSession(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    identifier = models.CharField(max_length=30, blank = True, default = "")
    pagesDone = models.IntegerField()
    comments = models.TextField(blank = True, default ="")
    task = models.CharField(max_length =4, choices = TYPES)
    operationComplete = models.NullBooleanField()
    startTime = models.DateTimeField('Time started book')
    endTime = models.DateTimeField('Time finished book')

    def duration(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(str(self.endTime)[:19],fmt)
        d2 = datetime.strptime(str(self.startTime)[:19],fmt)
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        return (float(d1_ts-d2_ts))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    #barcode = forms.CharField(max_length=20)
    class Media:
        js = ("static/jquery.js")

def make_custom_datefield(f,**kwargs):
    formfield = f.formfield(**kwargs)
    if isinstance(f, models.DateTimeField):
        formfield.widget.format = '%Y-%m-%d %H:%M:%S'
        formfield.widget.attrs.update({'class':'AnyTime_picker', 'readonly':'true'})
    return formfield

def make_custom_charfield(f,**kwargs):
    formfield = f.formfield(**kwargs)
    if isinstance(f, models.CharField):
        formfield.widget.attrs.update({'id':'autocomplete'})
    return formfield

class ProcessingForm(ModelForm):
    formfield_callback = make_custom_datefield
    class Meta:
        model = ProcessingSession
        exclude = ('identifier',)

class ItemProcessingForm(ModelForm):
    #formfield_callback = make_custom_datefield
    class Meta:
        model = ProcessingSession

class BookForm(ModelForm):
    formfield_callback = make_custom_charfield
    class Meta:
        model = Item
        exclude = ('totalPages',)

