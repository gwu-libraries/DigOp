from django.db import models
from django.contrib.auth.models import User, UserManager
from django import forms
from django.forms import ModelForm
from datetime import datetime

# Create your models here.

TYPES = (
    ('Scan','Scan'),
    ('QC','QC'),
    ('QA','QA'),
    ('OCR','OCR')
    )



class Book(models.Model):
    barcode = models.CharField(max_length=50)
    totalPages = models.IntegerField()
    bookComplete = models.NullBooleanField()
    def __unicode__(self):
        return self.barcode

class ProcessingSession(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)
    pagesDone = models.IntegerField()
    comments = models.TextField()
    task = models.CharField(max_length =4, choices = TYPES)
    startTime = models.DateTimeField('Time started book')
    endTime = models.DateTimeField('Time finished book')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    #barcode = forms.CharField(max_length=20)
    class Media:
        js = ("static/jquery.js")

def make_custom_datefield(f,**kwargs):
    formfield = f.formfield()
    if isinstance(f, models.DateTimeField):
        formfield.widget.format = '%Y-%m-%d %H:%M:%S'
        formfield.widget.attrs.update({'class':'AnyTime_picker', 'readonly':'true'})
    return formfield

class ProcessingForm(ModelForm):
    formfield_callback = make_custom_datefield
    
    
    class Meta:
        model = ProcessingSession
    #barcode = forms.CharField(max_length=20)
    #pages = forms.CharField(max_length=20)
    #comments = forms.CharField(max_length=100,required=False)
    #openingDate = forms.DateTimeField(label='Start Time',initial=datetime.now() )
    #closingDate = forms.DateTimeField(label='End Time',initial=datetime.now())


class BookForm(forms.Form):
    barcode = forms.CharField(max_length=50)

