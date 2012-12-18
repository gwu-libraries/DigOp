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
    startTime = models.DateTimeField('Time started item', default=datetime.now())
    endTime = models.DateTimeField('Time finished item')

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
    def __init__(self, *args, **kwargs):
        super(ProcessingForm, self).__init__(*args, **kwargs)
        self.fields['pagesDone'].error_messages['required'] = 'Enter a value for pagesDone field'
        self.fields['endTime'].error_messages['required'] = 'Enter a value for Time Finished item field'
        #if self.errors:
            #for f_name in self.fields:
                #if f_name in self.errors:
                    #classes = self.fields[f_name].widget.attrs.get('class', '')
                    #classes += 'error'
                    #self.fields[f_name].widget.attrs['class'] = classes
    formfield_callback = make_custom_datefield
    item = forms.CharField(max_length=100)
    def save(self):
        item_name = self.cleaned_data['item']
        item = Item.objects.get_or_create(name=item_name)[0]
        self.instance.item = item
        #if self.errors:
            #for f_name in self.fields:
                #if f_name in self.errors:
                    #classes = self.fields[f_name].widget.attrs.get('class', '')
                    #classes += 'error'
                    #self.fields[f_name].widget.attrs['class'] = classes
    class Meta:
        model = ProcessingSession
        exclude = ('identifier','user','item',)
        fields = ('item', 'pagesDone', 'comments', 'task', 'operationComplete', 'startTime', 'endTime')

class ItemProcessingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemProcessingForm, self).__init__(*args, **kwargs)
        self.fields['pagesDone'].error_messages['required'] = 'Enter a value for PagesDone field'
        self.fields['endTime'].error_messages['required'] = 'Enter a value for Time Finished item field'
        self.fields['identifier'].error_messages['required'] = 'Enter a value for Identifier field'
    formfield_callback = make_custom_datefield
    item = forms.CharField(max_length=100)
    def save(self):
        item_name = self.cleaned_data['item']
        item = Item.objects.get_or_create(name=item_name)[0]
        self.instance.item = item
    class Meta:
        model = ProcessingSession
        exclude = ('user','item')
        fields = ('item', 'identifier', 'pagesDone', 'comments', 'task', 'operationComplete', 'startTime', 'endTime')

class BookForm(ModelForm):
    formfield_callback = make_custom_charfield
    class Meta:
        model = Item
        exclude = ('totalPages',)

