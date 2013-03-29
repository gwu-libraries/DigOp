from datetime import datetime
import time

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import signals

from ui.signals import create_profile


# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)


TYPES = (
    ('Scan', 'Scan'),
    ('QC', 'QC'),
    ('QA', 'QA'),
)

ITEMS = (
    ('Book', 'Book'),
    ('Map', 'Map'),
    ('Microfilm', 'Microfilm'),
)

DEPTS = (
    ('LIT', 'LIT'),
    ('SPEC', 'SPEC'),
    ('CIRC', 'CIRC'),
    ('REF', 'REF'),
    ('RDG', 'RDG'),
    ('STG', 'STG'),
)

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    startDate = models.DateTimeField('Project Start Date', default=datetime.now)
    endDate = models.DateTimeField(null=True, blank=True)
    projectComplete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    project = models.ForeignKey(Project)
    barcode = models.CharField(max_length=50)
    totalPages = models.IntegerField(blank=True)
    itemType = models.CharField(max_length=10, choices=ITEMS)

    def __unicode__(self):
        return self.barcode


class ProcessingSession(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    identifier = models.CharField(max_length=30, blank=True, default="")
    pagesDone = models.IntegerField()
    comments = models.TextField(blank=True, default="")
    task = models.CharField(max_length=4, choices=TYPES)
    operationComplete = models.NullBooleanField()
    startTime = models.DateTimeField('Time started item', default=datetime.now)
    endTime = models.DateTimeField('Time finished item')

    def duration(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(str(self.endTime)[:19], fmt)
        d2 = datetime.strptime(str(self.startTime)[:19], fmt)
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        return (float(d1_ts - d2_ts))


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    department = models.CharField(max_length=10, choices=DEPTS, blank=True)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return unicode(self.user)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)
    #barcode = forms.CharField(max_length=20)

    class Media:
        js = ("static/jquery.js")


def make_custom_datefield(f, **kwargs):
    formfield = f.formfield(**kwargs)
    if isinstance(f, models.DateTimeField):
        formfield.widget.format = '%Y-%m-%d %H:%M:%S'
        formfield.widget.attrs.update({'class': 'AnyTime_picker',
                                       'readonly': 'true'})
    return formfield


def make_custom_charfield(f, **kwargs):
    formfield = f.formfield(**kwargs)
    if isinstance(f, models.CharField):
        formfield.widget.attrs.update({'id': 'autocomplete'})
    return formfield


class ProcessingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcessingForm, self).__init__(*args, **kwargs)
        self.fields['pagesDone'].error_messages['required'] = \
            'Enter a value for pagesDone field'
        self.fields['endTime'].error_messages['required'] = \
            'Enter a value for Time Finished item field'
    formfield_callback = make_custom_datefield
    item = forms.CharField(max_length=100)

    def save(self):
        item_name = self.cleaned_data['item']
        item = Item.objects.get_or_create(name=item_name)
        self.instance.item = item

    def clean_item(self):
        data = self.cleaned_data['item']
        obj = Item.objects.get(barcode=data)
        return obj

    class Meta:
        model = ProcessingSession
        exclude = ('identifier', 'user')
        fields = ('item', 'pagesDone', 'comments', 'task',
                  'operationComplete', 'startTime', 'endTime')


class ItemProcessingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemProcessingForm, self).__init__(*args, **kwargs)
        self.fields['pagesDone'].error_messages['required'] = \
            'Enter a value for PagesDone field'
        self.fields['endTime'].error_messages['required'] = \
            'Enter a value for Time Finished item field'
        self.fields['identifier'].error_messages['required'] = \
            'Enter a value for Identifier field'
    formfield_callback = make_custom_datefield
    item = forms.CharField(max_length=100)

    def save(self):
        item_name = self.cleaned_data['item']
        itemid = Item.objects.get_or_create(name=item_name)
        self.instance.item = itemid

    def clean_item(self):
        data = self.cleaned_data['item']
        obj = Item.objects.get(barcode=data)
        return obj

    class Meta:
        model = ProcessingSession
        exclude = ('user')
        fields = ('item', 'identifier', 'pagesDone', 'comments', 'task',
                  'operationComplete', 'startTime', 'endTime')


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['firstname'].initial = self.instance.user.first_name
            self.fields['lastname'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    email = forms.EmailField(label='Primary email', help_text='')
    firstname = forms.CharField(max_length=100, label='First Name')
    lastname= forms.CharField(max_length=100, label='Last Name')

    class Meta:
        model = UserProfile
        exclude = ('user')

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['firstname']
        u.last_name = self.cleaned_data['lastname']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

class BookForm(ModelForm):
    formfield_callback = make_custom_charfield

    class Meta:
        model = Item
        exclude = ('totalPages')


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['required'] = \
                'Enter a value for Project Name'
        self.fields['description'].error_messages['required'] = \
                'Enter a value for Project Description'
        self.fields['startDate'].error_messages['required'] = \
                'Enter a value for Project start Date'
    formfield_callback = make_custom_datefield

    class Meta:
        model = Project
        exclude = ('endDate', 'projectComplete')

class CloseProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CloseProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['required'] = \
                'Select a Project Name'
        self.fields['endDate'].error_messages['required'] = \
                'Please select an end date'
        self.fields['projectComplete'].error_messages['required'] = \
                'Please select an end date'
    formfield_callback = make_custom_datefield
    name = forms.ModelChoiceField(Project.objects.filter(projectComplete=False), initial=0)

    class Meta:
        model = Project
        exclude = ('description', 'startDate')
