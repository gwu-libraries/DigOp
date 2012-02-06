from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render_to_response
from books.models import LoginForm
from books.models import BookForm
from books.models import Book
from books.models import Book_Staff
from django.contrib.auth.models import User, UserManager
import urllib, urllib2
import sys
import suds
from optparse import OptionParser
from pprint import pprint
from datetime import datetime
from dateutil.parser import parse
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template import Library
from datetime import timedelta
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

import time
use = None
register = Library()


def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True   

def login(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.html', {
            'error' : error,
            'form' : form,
        })
    
    
       
              
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            use = authenticate(username=username, password=password)
            request.session['user_id'] = use
            if use is not None:
                # Redirect to a success page.
                auth_login(request, use)
                #bar = request.POST['barcode']
                #loc = WSBarcodePagesLocator()
                #port = loc.getWSBarcodePagesPort(url='http://128.164.212.164:8080/BarcodeService/WSBarcodePages',tracefile = sys.stdout)
                #msg = getPages()
                #msg.Value=bar
                #rsp = port.getPages(msg)
                #url='http://128.164.212.164:8080/BarcodeService/WSBarcodePages?wsdl'
                #client = suds.client.Client(url)
                return HttpResponseRedirect('/index/')
            else: # Return a 'disabled account' error message 
                error = 'account disabled' 
                return errorHandle(error)
        
        else: 
            error = 'form is invalid' 
            return errorHandle(error)
    else:
        form = LoginForm() # An unbound form
        return render_to_response('login.html', {
            'form': form,
        })    

def indexPage(request):
    if request.user.is_authenticated():
        if request.user.is_superuser == True:
            #b = Book.objects.all()
            #u = User.objects.all()
            #bs = list(Book_Staff.objects.all().select_related())
                    
            bs = list(User.objects.all())
            myList = []
            for item in bs:
                #barcode = item.book.barcode
                timediff =0
                #if item.book.end_time is not None:
                #    timediff = item.book.end_time - item.book.start_time
                #start = bs.book.start_time
                #end = bs.book.end_time
                us = item.username
                #if item.book.end_time is not None:
                #    seq = (barcode, str(item.book.end_time - item.book.start_time), item.pages, us)
                #else:
                #    seq = (barcode, None, None , item.pages , us)
                myList.append(us)
                        
                        
            return render_to_response('admin_login.html', {
                        'username':us,
                        'superuser': request.user.is_superuser,
                        'list' : myList,
            })
        else:
			return render_to_response('logged_in.html', {
                        'username': request.user.username,
                        'superuser': request.user.is_superuser,
                        'form' : BookForm(),
			})





def processForm(request):
    use=request.user
    def errorHandle(error):
        form = BookForm()
        return render_to_response('logged_in.html', {
            'error' : error,
            'form' : form,
        })
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            barcode = request.POST['barcode']
            pages = request.POST['pages']
            comments = request.POST['Comments']
            openingDate = request.POST['start_time']
            closingDate = request.POST['end_time']
            tasktype = request.POST['task']
            url='http://128.164.212.164:8080/BarcodeService/WSBarcodePages?wsdl'
            client = suds.client.Client(url)
            #t = Time.objects.create(start_time=parse(openingDate,yearfirst=True),end_time=parse(closingDate,yearfirst=True))
            #t = Time.objects.create(start_time=datetime.strptime(openingDate,'%Y-%m-%d %H:%M:%S'),end_time=datetime.strptime(closingDate,'%Y-%m-%d %H:%M:%S'),item.book.task)
            totalPages = client.service.getPages(barcode)
            b = Book.objects.create(barcode=barcode, pages=totalPages,Comments=comments,start_time=openingDate,end_time=closingDate,task=tasktype)
            bst = None
            if(int(pages) == int(totalPages)):
                bst = Book_Staff(book=b,user=use,pages=totalPages,book_complete=True)
            else:
                bst = Book_Staff(book=b,user=use,pages=pages,book_complete=False)
        
            b.save()
            bst.save()
            return render_to_response('pages.html', {
                        'totalPages': totalPages,
                        'pages' : pages,
                        'barcode' : barcode,
                        'comments' : comments,
                        'openingDate' : openingDate,
                        'closingDate' : closingDate,
                 })
            
            
        else: 
            error = 'form is invalid' 
            return errorHandle(error)
    else:
        form = BookForm() # An unbound form
        return render_to_response('logged_in.html', {
            'form': form,
        })        

    
def produceData(request):
    name = request.GET.get('user')
    start = request.GET.get('start')
    end = request.GET.get('end')
    myList = []
    if name != 'all':
        a = Book_Staff.objects.filter(user__username=name).filter(book__start_time__gte = start) 
        c = Book_Staff.objects.filter(user__username=name).filter(book__start_time__lte = end)
        b = a & c
        seq = None
    
        for item in b:
            #barcode = item.book.barcode
            #timediff =0
            #if item.book.end_time is not None:
            #    timediff = item.book.end_time - item.book.start_time
            #    start = bs.book.start_time
            #    end = bs.book.end_time
            us = item.user.username
            fmt = '%Y-%m-%d %H:%M:%S'
            d1 = datetime.strptime(str(item.book.end_time),fmt)
            d2 = datetime.strptime(str(item.book.start_time),fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            if item.book.end_time is not None:
                seq = (item.book.barcode, str(item.book.end_time - item.book.start_time), item.pages, us, item.book_complete,int(int(item.pages)/(float(d1_ts-d2_ts)/(60*60))),item.book.task,item.book.start_time )
            else:
                seq = (item.book.barcode, None , item.pages , us, item.book_complete,int(int(item.pages)/(float(d1_ts-d2_ts)/(60*60))),item.book.task,item.book.start_time)
            myList.append(seq)
    else:
        b = Book_Staff.objects.all();
        seq = None
        for item in b:
            #barcode = item.book.barcode
            #timediff =0
            #if item.book.end_time is not None:
            #    timediff = item.book.end_time - item.book.start_time
            #    start = bs.book.start_time
            #    end = bs.book.end_time
            us = item.user.username
            fmt = '%Y-%m-%d %H:%M:%S'
            d1 = datetime.strptime(str(item.book.end_time),fmt)
            d2 = datetime.strptime(str(item.book.start_time),fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            if item.book.end_time is not None:
                seq = (item.book.barcode, str(item.book.end_time - item.book.start_time), item.pages, us, item.book_complete,int(int(item.pages)/(float(d1_ts-d2_ts)/(60*60))),item.book.task )
            else:
                seq = (item.book.barcode, None , item.pages , us, item.book_complete,int(int(item.pages)/(float(d1_ts-d2_ts)/(60*60))),item.book.task)
            myList.append(seq)
        
    return render_to_response('data.html', {
                        'list': myList,
                        'user': name,
                 })
def logoutUser(request):
    logout(request)
    return render_to_response('Logout.html', {
                        
                 })