import urllib, urllib2
import sys
from optparse import OptionParser
from pprint import pprint
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, UserManager
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template import Library
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.template import Library, Node
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.core.context_processors import csrf
from django.conf import settings
from django.shortcuts import render
import suds

from ui.models import LoginForm
from ui.models import BookForm
from ui.models import ProcessingForm
from ui.models import ItemProcessingForm
from ui.models import Item
from ui.models import ProcessingSession

#django-qsstats-magic Should be install before running the app
#python-dateutil

import time
use = None
register = Library()

def login(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.html', {
            'error' : error,
            'form' : form,
        },context_instance=RequestContext(request))
    c = {}
    c.update(csrf(request))
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            use = authenticate(username=username, password=password)
            request.session['user_id'] = use
            if use is not None:
                auth_login(request, use)
                return HttpResponseRedirect('/indexPage/')
            else: # Return a 'disabled account' error message
                error = 'account disabled'
                return errorHandle(error)

        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = LoginForm() # An unbound form
        return render_to_response('login.html',  {
            'form': form,
	    'c' : c,
        },context_instance=RequestContext(request))

@login_required
def indexPage(request):
    form = BookForm()

    if request.user.is_superuser == True:
        return render_to_response('admin_page.html', {
        },context_instance=RequestContext(request))
    else:
        return render_to_response('user_page.html', {
                        'form' : form,
        },context_instance=RequestContext(request))

def adminSessionData(request):
    form = BookForm()
    return render_to_response('getbarcode.html', {
                        'form' : form,
            },context_instance=RequestContext(request))

def showUsers(request):
    return render_to_response('admin_login.html', {
            'users':User.objects.all(),
            },context_instance=RequestContext(request))

def showGraph(request):
    userObjects = User.objects.all()
    users = []
    colors= ['Blue','Red','Green','Black','Brown','Pink','Beige','Coral','Chocolate','Grey','Cyan','DarkRed','Violet','Gold','Magneta','Khaki','Ivory','Lavender','Lime','Yellow',    'GoldenRed','Navy','Olive','orchid','Linen','Orange','Peru','Purple','Plum','RoyalBlue','SandyBrown','Salmon','Silver','Tan','Teal','Thistle','Tomato','Violet','Wheat','Turqu    oise','Sienna','PaleGreen','PaleVioletRed','OliveDrab','MintCream','MediumPurple','RosyBrown','SeaGreen','skyBlue','IndianRed','HotPink','GreenYellow','ForestGreen','DarkViol    et','Aqua'] 
    low = 100
    high = 0
    values = []
    valuesList=[]
    
    entryList = []
    for u in userObjects:
	users.append(u.username)
	userrows = ProcessingSession.objects.filter(user=u)
	pages = 0
	for row in userrows: 
	    pages = pages + row.pagesDone
	if pages < low:
	    low = pages
	if pages > high:
	    high = pages
	valuesList.append(u.username+'('+str(pages)+')')
	entryList.append(pages)
    values.append(entryList)
    return render_to_response('showGraph.html', {
            'users':users,
	    'low':low,
	    'high':high,
	    'values':valuesList,
	    'testValues':values,
	    'entries' : entryList,
	    'colors':colors[:len(valuesList)],
            },context_instance=RequestContext(request))


def barcodePage(request):
    return render_to_response('barcodereportform.html', {
    },context_instance=RequestContext(request))

def barcodeReport(request):
    if request.method == 'POST': # If the form has been submitted...
	bar = request.POST['barcode']
	dictionary = None
	values = []
	try:
	    book = Item.objects.get(barcode=bar)
	except Item.DoesNotExist:
	    messages.add_message(request, messages.ERROR, 'Barcode does not exist ')
	    return render_to_response('barcoderesult.html', {
	    'list' : values,
	    },context_instance=RequestContext(request))
	result = ProcessingSession.objects.filter(book=book)
	for item in result:
	    dictionary = {'barcode':item.book.barcode, 'duration':str(item.endTime - item.startTime), 'objects':item.pagesDone, 'user':item.user, 'isFinished':item.operationComplete,'rate':int(int(item.pagesDone)/(item.duration()/(60*60))),'task':item.task,'startTime':item.startTime}
	    values.append(dictionary)
	messages.add_message(request, messages.SUCCESS, 'Results of Barcode '+ bar + ' are as follows: ')
	return render_to_response('barcoderesult.html', {
	'list' : values,
        },context_instance=RequestContext(request))


def reportMenu(request):
    return render_to_response('reportmenu.html', {

            },context_instance=RequestContext(request))

def processBookForm(request):
    use=request.user
    def errorHandle(error):
        form = BookForm()
        return render_to_response('getbarcode.html', {
            'error' : error,
            'form' : form,
        },context_instance=RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        if request.POST['itemType'] in ['Book','Map']:
            book = None
            form = BookForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    client = suds.client.Client(settings.SERVER_URL)
                    pages = client.service.getPages(bar)
		    if pages is None:
		        pages=0
                    book = Item.objects.create(barcode=bar, totalPages=pages)
                    book.save()
                    messages.add_message(request, messages.SUCCESS, 'Item object with barcode '+ bar + ' created successfully')
                    return render_to_response('processingForm.html', {
                        'form' : ProcessingForm(initial={'book': book,
                                                        'user':request.user,}),
						},context_instance=RequestContext(request))
                else:
		    messages.add_message(request, messages.ERROR, 'Item object with barcode '+ bar + ' exists')
		    return render_to_response('processingForm.html', {
                        'form' : ProcessingForm(initial={'book': book,
                                                        'user':request.user,}),
			},context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
        else:
            book = None
            form = BookForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    client = suds.client.Client(settings.SERVER_URL)
                    pages = client.service.getPages(bar)
                    if pages is None:
                        pages=0
                    book = Item.objects.create(barcode=bar, totalPages=pages)
                    book.save()
                    messages.add_message(request, messages.SUCCESS, 'Item object with barcode '+ bar + ' created successfully')
                    return render_to_response('itemProcessingForm.html', {
                        'form' : ItemProcessingForm(initial={'book': book,
                                                        'user':request.user,}),
                                                },context_instance=RequestContext(request))
                else:
                    messages.add_message(request, messages.ERROR, 'Item object with barcode '+ bar + ' exists')
                    return render_to_response('itemProcessingForm.html', {
                        'form' : ItemProcessingForm(initial={'book': book,
                                                        'user':request.user,}),
                        },context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
    else:
        form = BookForm() # An unbound form
        return render_to_response('getbarcode.html', {
            'form': form,
        },context_instance=RequestContext(request))

def processProcessingForm(request):
    use=request.user
    def errorHandle(error):
        form = ProcessingForm()
        return render_to_response('processingForm.html', {
            'error' : error,
            'form' : form,
        },context_instance=RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        form = ProcessingForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    complete = False
            bookid = request.POST['item']
            bookObject = Item.objects.get(id = bookid)
            pages = request.POST['pagesDone']
            comm = request.POST['comments']
            if request.POST['operationComplete'] == '2':
		complete = True
            elif request.POST['operationComplete'] == '3':		
		complete = False
	    elif request.POST['operationComplete'] == '1':
		complete = None
            openingDate = request.POST['startTime']
            closingDate = request.POST['endTime']
            tasktype = request.POST['task']
            bst = None
            bst = ProcessingSession(item=Item.objects.get(id =request.POST['item']),user=User.objects.get(id=request.POST['user']),pagesDone=pages,comments=comm,operationComplete            =complete,startTime=openingDate,endTime=closingDate,task=tasktype)
            bst.save()
            messages.add_message(request, messages.SUCCESS, 'record added successfully')
            return render_to_response('pages.html', {
                 },context_instance=RequestContext(request)
                 )


        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ProcessingForm() # An unbound form
        return render_to_response('processingForm.html', {
            'form': form,
        },context_instance=RequestContext(request))

def itemProcessingForm(request):
    use=request.user
    def errorHandle(error):
        form = ItemProcessingForm()
        return render_to_response('itemProcessingForm.html', {
            'error' : error,
            'form' : form,
        },context_instance=RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        form = ProcessingForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    complete = False
            bookid = request.POST['item']
            bookObject = Item.objects.get(id = bookid)
            pages = request.POST['pagesDone']
            comm = request.POST['comments']
            if request.POST['operationComplete'] == '2':
		complete = True
            elif request.POST['operationComplete'] == '3':		
		complete = False
	    elif request.POST['operationComplete'] == '1':
		complete = None
            openingDate = request.POST['startTime']
            closingDate = request.POST['endTime']
            tasktype = request.POST['task']
            bst = None
            bst = ProcessingSession(item=Item.objects.get(id =request.POST['item']),user=User.objects.get(id=request.POST['user']),pagesDone=pages,comments=comm,operationComplete            =complete,startTime=openingDate,endTime=closingDate,task=tasktype)
            bst.save()
            messages.add_message(request, messages.SUCCESS, 'record added successfully')
            return render_to_response('pages.html', {
                 },context_instance=RequestContext(request)
                 )


        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ItemProcessingForm() # An unbound form
        return render_to_response('itemProcessingForm.html', {
            'form' : form,
        },context_instance=RequestContext(request))


def produceData(request):
    name = request.GET.get('user')
    start = request.GET.get('start')
    end = request.GET.get('end')
    myList = []
    totalPages = 0
    totalHours = 0


    if name != 'all':
        a = ProcessingSession.objects.filter(user__username=name).filter(startTime__gte = start)
        c = ProcessingSession.objects.filter(user__username=name).filter(endTime__lte = end)
        b = a & c
        dictionary = None


        for item in b:
            if item.endTime is not None:
		dictionary = {'barcode':item.book.barcode, 'duration':str(item.endTime - item.startTime), 'objects':item.pagesDone, 'user':name, 'isFinished':item.operationComplete,'rate':int(int(item.pagesDone)/(item.duration()/(60*60))),'task':item.task,'startTime':item.startTime,'comments':item.comments }
		delta = item.endTime - item.startTime
		totalHours = totalHours + ( (delta.days * 86400 + delta.seconds) / 3600.0 )
		totalPages = totalPages + item.pagesDone
            else:
		dictionary = {'barcode':item.book.barcode, 'duration':None, 'objects':item.pagesDone, 'user':name, 'isFinished':item.operationComplete,'rate':int(int(item.pagesDone)/(item.duration()/(60*60))),'task':item.task,'startTime':item.startTime,'comments':item.comments  }
		delta = item.endTime - item.startTime
		totalHours = totalHours + ( ( delta.days * 86400 + delta.seconds ) / 3600.0)
                totalPages = totalPages + item.pagesDone
            myList.append(dictionary)
    else:
        b = ProcessingSession.objects.all();
        dictionary = None
        for item in b:
            us = item.user.username
            if item.endTime is not None:
		dictionary = {'barcode':item.book.barcode, 'duration':str(item.endTime - item.startTime), 'objects':item.pagesDone, 'user':us, 'isFinished':item.operationComplete		  ,'rate':int(int(item.pagesDone)/(item.duration()/(60*60))),'task':item.task,'startTime':item.startTime,'comments':item.comments  }
		delta = item.endTime - item.startTime
		totalHours = totalHours + ( ( delta.days * 86400 + delta.seconds ) / 3600.0 )
                totalPages = totalPages + item.pagesDone
            else:
		dictionary = {'barcode':item.book.barcode, 'duration':None, 'objects':item.pagesDone, 'user':us, 'isFinished':item.operationComplete,'rate':int(int(item.pagesDone		  )/(item.duration()/(60*60))),'task':item.task,'startTime':item.startTime,'comments':item.comments  }
		delta = item.endTime - item.startTime
		totalHours = totalHours + ( ( delta.days * 86400 + delta.seconds ) / 3600.0 )
                totalPages = totalPages + item.pagesDone
            myList.append(dictionary)

    return render_to_response('data.html', {
                        'list': myList,
                        'user': name,
			'totalHours':totalHours,
			'totalPages':totalPages,
                 })
def workGraph(request):
    stats = {'name': [], 'rate': []}
    return render_to_response('data.html', {
                        'list': myList,
                        'user': name,
                 })
def logoutUser(request):
    logout(request)
    return render(request,'logout.html')
