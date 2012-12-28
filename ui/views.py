from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import Library
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.views import password_reset, password_change_done as auth_password_change_done

from ui.models import LoginForm
from ui.models import BookForm
from ui.models import ProcessingForm
from ui.models import ItemProcessingForm
from ui.models import Item
from ui.models import ProcessingSession
from ui.models import UserProfile
from ui.models import ProfileForm

from profiles import views as profile_views
#django-qsstats-magic Should be install before running the app
#python-dateutil

use = None
register = Library()

def add_csrf(request, **kwargs):
    """Add CSRF to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def login(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.html', {
            'error': error,
            'form': form,
        }, context_instance=RequestContext(request))
    c = {}
    c.update(csrf(request))
    if request.user.is_authenticated():
        return HttpResponseRedirect('/indexPage/')
    if request.method == 'POST':  # If the form has been submitted...
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            use = authenticate(username=username, password=password)
            request.session['user_id'] = use
            if use is not None:
                auth_login(request, use)
                return HttpResponseRedirect('/indexPage/')
            else:  # Return a 'disabled account' error message
                error = 'account disabled'
                return errorHandle(error)

        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = LoginForm()  # An unbound form
        return render_to_response('login.html',  {
            'form': form,
            'c': c,
        }, context_instance=RequestContext(request))


@login_required
def edit_profile(request, pk):
    return profile_views.edit_profile(request, form_class=ProfileForm)


@login_required
def password_change_done(request, template='accounts/my_password_change_done.html'):
    return auth_password_change_done(request,template_name=template)


@login_required
def profile_menu(request):
    return render(request,'profile_menu.html')


def reset_done(request):
    return render(request,'reset_done.html')


@login_required
def view_profile(request):
        return render(request,'view_profile.html', {
            'profile': UserProfile.objects.get(user=request.user),
        })

def reset_password(request, template_name='reset_password.html'):
        return password_reset(request, template_name)

@login_required
def indexPage(request):
    if request.user.is_superuser:
        return render_to_response('admin_page.html', {
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('user_page.html', {
        }, context_instance=RequestContext(request))


@login_required
def adminSessionData(request):
    form = BookForm()
    return render_to_response('getbarcode.html', {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def displayItemProcessingForm(request):
    form = BookForm()
    return render(request, 'process_item_form.html', {
        'form': form,
    })


@login_required
def showUsers(request):
    return render_to_response('admin_login.html', {
        'users': User.objects.all(),
    }, context_instance=RequestContext(request))


@login_required
def showGraph(request):
    userObjects = User.objects.all()
    users = []
    colors = ['Blue', 'Red', 'Green', 'Black', 'Brown', 'Pink', 'Beige']
    colors.extend(['Chocolate', 'Grey', 'Cyan', 'DarkRed', 'Violet', 'Gold'])
    colors.extend(['Magneta', 'Khaki', 'Ivory', 'Lavender', 'Lime', 'Yellow'])
    colors.extend(['GoldenRed', 'Navy', 'Olive', 'orchid', 'Linen', 'Orange'])
    colors.extend(['Peru', 'Purple', 'Plum', 'RoyalBlue', 'SandyBrown'])
    colors.extend(['Silver', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Violet'])
    colors.extend(['Turquoise', 'Sienna', 'PaleGreen', 'PaleVioletRed'])
    colors.extend(['MintCream', 'MediumPurple', 'RosyBrown', 'SeaGreen'])
    colors.extend(['IndianRed', 'HotPink', 'GreenYellow', 'ForestGreen'])
    colors.extend(['DarkViolet', 'Aqua', 'Coral', 'Salmon', 'Wheat'])
    colors.extend(['OliveDrab', 'skyBlue'])
    low = 100
    high = 0
    values = []
    valuesList = []
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
        valuesList.append(u.username + '(' + str(pages) + ')')
        entryList.append(pages)
    values.append(entryList)
    return render_to_response('showGraph.html', {
        'users': users,
        'low': low,
        'high': high,
        'values': valuesList,
        'testValues': values,
        'entries': entryList,
        'colors': colors[:len(valuesList)],
    }, context_instance=RequestContext(request))


@login_required
def barcodePage(request):
    return render_to_response('barcodereportform.html', {
    }, context_instance=RequestContext(request))


@login_required
def barcodeReport(request):
    if request.method == 'POST':  # If the form has been submitted...
        bar = request.POST['barcode']
        dictionary = {}
        values = []
        try:
            book = Item.objects.filter(barcode=bar)
        except Item.DoesNotExist:
            err_msg = 'Barcode does not exist '
            messages.add_message(request, messages.ERROR, err_msg)
            return render_to_response('barcoderesult.html', {
                'list': values,
            }, context_instance=RequestContext(request))
        result = ProcessingSession.objects.filter(item=book)
        for rec in result:
            dictionary['itemType'] = rec.item.itemType
            dictionary['barcode'] = rec.item.barcode
            dictionary['duration'] = str(rec.endTime - rec.startTime)
            dictionary['objects'] = rec.pagesDone
            dictionary['user'] = rec.user
            dictionary['isFinished'] = rec.operationComplete
            rate_of_work = int(int(rec.pagesDone) / (rec.duration() / 3600))
            dictionary['rate'] = rate_of_work
            dictionary['task'] = rec.task
            dictionary['startTime'] = rec.startTime
            values.append(dictionary)
        return render_to_response('barcoderesult.html', {
            'list': values,
        }, context_instance=RequestContext(request))


@login_required
def barcode(request, identifier):
    dictionary = {}
    values = []
    book = None
    try:
        book = Item.objects.filter(barcode=identifier)
    except Item.DoesNotExist:
        return render_to_response('barcoderesult.html', {
            'list': values,
            'barcode': identifier,
        }, context_instance=RequestContext(request))
    result = ProcessingSession.objects.filter(item=book)
    for rec in result:
        dictionary['itemType'] = rec.item.itemType
        dictionary['barcode'] = rec.item.barcode
        dictionary['duration'] = str(rec.endTime - rec.startTime)
        dictionary['objects'] = rec.pagesDone
        dictionary['user'] = rec.user
        dictionary['isFinished'] = rec.operationComplete
        rate_of_work = int(int(rec.pagesDone) / (rec.duration() / 3600))
        dictionary['rate'] = rate_of_work
        dictionary['task'] = rec.task
        dictionary['startTime'] = rec.startTime
        values.append(dictionary)
    return render_to_response('barcoderesult.html', {
        'list': values,
    }, context_instance=RequestContext(request))


@login_required
def reportMenu(request):
    return render_to_response('reportmenu.html', {
    }, context_instance=RequestContext(request))


@login_required
def processItemForm(request):
    def errorHandle(error):
        form = BookForm()
        return render_to_response('getbarcode.html', {
            'error': error,
            'form': form,
        }, context_instance=RequestContext(request))
    if request.method == 'POST':  # If the form has been submitted...
        if request.POST['itemType'] in ['Book', 'Map']:
            book = None
            form = BookForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    pages = 0
                    item_type = request.POST['itemType']
                    book = Item.objects.create(barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    err_msg = 'Item with barcode ' + bar + ' created'
                    messages.add_message(request, messages.SUCCESS, err_msg)
                    task_type = request.POST['taskType']
                    return render_to_response('processingForm.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': task_type,
                                                        }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
                else:
                    task_type = request.POST['taskType']
                    return render_to_response('processingForm.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': task_type,
                                                        }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
        else:
            book = None
            form = BookForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    #client = suds.client.Client(settings.SERVER_URL)
                    #pages = client.service.getPages(bar)
                    #if pages is None:
                    pages = 0
                    item_type = request.POST['itemType']
                    book = Item.objects.create(barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    err_msg = 'Item object with barcode '
                    err_msg = err_msg + bar + ' created successfully'
                    messages.add_message(request, messages.SUCCESS, err_msg)
                    task_type = request.POST['taskType']
                    user = request.user
                    return render_to_response('itemProcessingForm.html', {
                        'form': ItemProcessingForm(initial={'item': book,
                                                            'user': user,
                                                            'task': task_type,
                                                            }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
                else:
                    err_msg = 'Item object with barcode ' + bar + ' exists'
                    task_type = request.POST['taskType']
                    user = request.user
                    messages.add_message(request, messages.ERROR, err_msg)
                    return render_to_response('itemProcessingForm.html', {
                        'form': ItemProcessingForm(initial={'item': book,
                                                            'user': user,
                                                            'task': task_type,
                                                            }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
    else:
        form = BookForm()  # An unbound form
        return render_to_response('getbarcode.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def processBookForm(request):
    def errorHandle(error):
        form = BookForm(request.POST)
        return render_to_response('getbarcode.html', {
            'error': error,
            'form': form,
        }, context_instance=RequestContext(request))
    if request.method == 'POST':  # If the form has been submitted...
        if request.POST['itemType'] in ['Book', 'Map']:
            book = None
            form = BookForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    #client = suds.client.Client(settings.SERVER_URL)
                    #pages = client.service.getPages(bar)
                    #if pages is None:
                    pages = 0
                    item_type = request.POST['itemType']
                    book = Item.objects.create(barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    return render_to_response('processingForm.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': 'Scan',
                                                        }),
                        'itemType': request.POST['itemType'],
                        'task': 'Scan',
                        'item': book,
                    }, context_instance=RequestContext(request))
                else:
                    return render_to_response('processingForm.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': 'Scan',
                                                        }),
                        'task': 'Scan',
                        'item': book,
                    }, context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
        else:
            book = None
            form = BookForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                bar = request.POST['barcode']
                try:
                    book = Item.objects.get(barcode=bar)
                except Item.DoesNotExist:
                    book = None
                if book is None:
                    #client = suds.client.Client(settings.SERVER_URL)
                    #pages = client.service.getPages(bar)
                    #if pages is None:
                    pages = 0
                    item_type = request.POST['itemType']
                    book = Item.objects.create(barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    user = request.user
                    return render_to_response('itemProcessingForm.html', {
                        'form': ItemProcessingForm(initial={'item': book,
                                                            'user': user,
                                                            'task': 'Scan',
                                                            }),
                        'itemType': request.POST['itemType'],
                        'task': 'Scan',
                        'item': book,
                    }, context_instance=RequestContext(request))
                else:
                    user = request.user
                    return render_to_response('itemProcessingForm.html', {
                        'form': ItemProcessingForm(initial={'item': book,
                                                            'user': user,
                                                            'task': 'Scan'
                                                            }),
                        'task': 'Scan',
                        'item': book,
                    }, context_instance=RequestContext(request))
            else:
                error = 'form is invalid'
                return errorHandle(error)
    else:
        form = BookForm()  # An unbound form
        return render_to_response('getbarcode.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def processProcessingForm(request):
    def errorHandle(error):
        if request.POST['itemType'] in ['Book', 'Map']:
            form = ProcessingForm(request.POST)
            return render_to_response('processingForm.html', {
                'error': error,
                'form': form,
                'task': request.POST['task'],
                'itemType': request.POST['itemType'],
            }, context_instance=RequestContext(request))
        else:
            form = ItemProcessingForm(request.POST)
            return render_to_response('itemProcessingForm.html', {
                'error': error,
                'form': form,
                'task': request.POST['task'],
                'itemType': request.POST['itemType'],
            }, context_instance=RequestContext(request))
    if request.method == 'POST':  # If the form has been submitted...
        form = ProcessingForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            complete = False
            bookid = request.POST['item']
            bookObject = Item.objects.get(barcode=bookid)
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
            bst = ProcessingSession(item=bookObject, user=request.user,
                                    pagesDone=pages, comments=comm,
                                    operationComplete=complete,
                                    startTime=openingDate,
                                    endTime=closingDate, task=tasktype)
            bst.save()
            if tasktype == 'QC' or tasktype == 'QA':
                form = BookForm()
                return render_to_response('process_item_form.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
            else:
                form = BookForm()
                return render_to_response('getbarcode.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ProcessingForm()  # An unbound form
        return render_to_response('processingForm.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def itemProcessingForm(request):
    def errorHandle(error):
        form = ItemProcessingForm(request.POST)
        return render_to_response('itemProcessingForm.html', {
            'error': error,
            'form': form,
            'task': request.POST['task'],
            'itemType': request.POST['itemType'],
        }, context_instance=RequestContext(request))
    if request.method == 'POST':  # If the form has been submitted...
        form = ProcessingForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            complete = False
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
            item_id = request.POST['item']
            bst = ProcessingSession(item=Item.objects.get(id=item_id),
                                    user=request.user, pagesDone=pages,
                                    comments=comm, operationComplete=complete,
                                    startTime=openingDate,
                                    endTime=closingDate, task=tasktype)
            bst.save()
            if tasktype == 'Scan':
                form = BookForm()
                msg = 'record added successfully'
                messages.add_message(request, messages.SUCCESS, msg)
                return render_to_response('getbarcode.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
            else:
                form = BookForm()
                return render_to_response('process_item_form.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ItemProcessingForm()  # An unbound form
        return render_to_response('itemProcessingForm.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def user(request, username):
    if request.GET.get('user'):
        request.session['user'] = request.GET.get('user')
    if request.GET.get('start'):
        request.session['start'] = request.GET.get('start')
    if request.GET.get('end'):
        request.session['end'] = request.GET.get('end')
    if request.GET.get('itemtype'):
        request.session['itemtype'] = request.GET.get('itemtype')
    name = request.session['user']
    start = request.session['start']
    end = request.session['end']
    itemtype = request.session['itemtype']
    myList = []
    totalPages = 0
    totalHours = 0
    a = ProcessingSession.objects.filter(user__username=username)
    dictionary = {}
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'barcode': item.item.barcode,
                          'itemType': item.item.itemType,
                          'duration': str(item.endTime - item.startTime),
                          'objects': item.pagesDone,
                          'user': username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        else:
            rate = int(int(item.pagesDone) / (item.duration() / (60 * 60)))
            dictionary = {'barcode': item.book.barcode,
                          'itemType': item.item.itemType,
                          'duration': None, 'objects': item.pagesDone,
                          'user': username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        myList.append(dictionary)
    paginator = Paginator(myList, 10)
    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)
    return render_to_response('data.html', {
        'list': rows,
        'username': username,
        'totalHours': totalHours,
        'totalPages': totalPages,
    }, context_instance=RequestContext(request))


@login_required
def task(request, tasktype):
    if request.GET.get('user'):
        request.session['user'] = request.GET.get('user')
    if request.GET.get('start'):
        request.session['start'] = request.GET.get('start')
    if request.GET.get('end'):
        request.session['end'] = request.GET.get('end')
    if request.GET.get('itemtype'):
        request.session['itemtype'] = request.GET.get('itemtype')
    name = request.session['user']
    start = request.session['start']
    end = request.session['end']
    itemtype = request.session['itemtype']
    a = ProcessingSession.objects.filter(task__exact=tasktype)
    totalPages = 0
    totalHours = 0
    dictionary = {}
    myList = []
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'barcode': item.item.barcode,
                          'itemType': item.item.itemType,
                          'duration': str(item.endTime - item.startTime),
                          'objects': item.pagesDone,
                          'user': item.user.username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        else:
            rate = int(int(item.pagesDone) / (item.duration() / (60 * 60)))
            dictionary = {'barcode': item.book.barcode,
                          'itemType': item.item.itemType,
                          'duration': None, 'objects': item.pagesDone,
                          'user': item.user.username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        myList.append(dictionary)
    paginator = Paginator(myList, 10)
    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)
    return render_to_response('data.html', {
        'list': rows,
        'totalHours': totalHours,
        'totalPages': totalPages,
    }, context_instance=RequestContext(request))


@login_required
def item(request, itemtype):
    if request.GET.get('user'):
        request.session['user'] = request.GET.get('user')
    if request.GET.get('start'):
        request.session['start'] = request.GET.get('start')
    if request.GET.get('end'):
        request.session['end'] = request.GET.get('end')
    if request.GET.get('itemtype'):
        request.session['itemtype'] = request.GET.get('itemtype')
    name = request.session['user']
    start = request.session['start']
    end = request.session['end']
    itemtype = request.session['itemtype']
    a = ProcessingSession.objects.filter(item__itemType__exact=itemtype)
    totalPages = 0
    totalHours = 0
    dictionary = {}
    myList = []
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'barcode': item.item.barcode,
                          'itemType': item.item.itemType,
                          'duration': str(item.endTime - item.startTime),
                          'objects': item.pagesDone,
                          'user': item.user.username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        else:
            rate = int(int(item.pagesDone) / (item.duration() / (60 * 60)))
            dictionary = {'barcode': item.book.barcode,
                          'itemType': item.item.itemType,
                          'duration': None, 'objects': item.pagesDone,
                          'user': item.user.username,
                          'isFinished': item.operationComplete,
                          'rate': rate, 'task': item.task,
                          'startTime': item.startTime,
                          'comments': item.comments}
            delta = item.endTime - item.startTime
            conversion = delta.days * 86400 + delta.seconds
            totalHours = totalHours + (conversion / 3600.0)
            totalPages = totalPages + item.pagesDone
        myList.append(dictionary)
    paginator = Paginator(myList, 10)
    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)
    return render_to_response('data.html', {
        'list': rows,
        'totalHours': totalHours,
        'totalPages': totalPages,
    }, context_instance=RequestContext(request))


@login_required
def produceData(request):
    if request.GET.get('user'):
        request.session['user'] = request.GET.get('user')
    if request.GET.get('start'):
        request.session['start'] = request.GET.get('start')
    if request.GET.get('end'):
        request.session['end'] = request.GET.get('end')
    if request.GET.get('itemtype'):
        request.session['itemtype'] = request.GET.get('itemtype')
    name = request.session['user']
    start = request.session['start']
    end = request.session['end']
    itemtype = request.session['itemtype']
    myList = []
    totalPages = 0
    totalHours = 0
    if name != 'all':
        a = ProcessingSession.objects.filter(user__username=name)
        a = a.filter(startTime__gte=start)
        c = ProcessingSession.objects.filter(user__username=name)
        c = c.filter(endTime__lte=end)
        c = c.filter(item__itemType__exact=itemtype)
        b = a & c
        dictionary = None
        for item in b:
            rate = int(int(item.pagesDone) / (item.duration() / 3600))
            if item.endTime is not None:
                dictionary = {'barcode': item.item.barcode,
                              'itemType': item.item.itemType,
                              'duration': str(item.endTime - item.startTime),
                              'objects': item.pagesDone, 'user': name,
                              'isFinished': item.operationComplete,
                              'rate': rate, 'task': item.task,
                              'startTime': item.startTime,
                              'comments': item.comments}
                delta = item.endTime - item.startTime
                conversion = delta.days * 86400 + delta.seconds
                totalHours = totalHours + (conversion / 3600.0)
                totalPages = totalPages + item.pagesDone
            else:
                rate = int(int(item.pagesDone) / (item.duration() / (60 * 60)))
                dictionary = {'barcode': item.book.barcode,
                              'itemType': item.item.itemType,
                              'duration': None, 'objects': item.pagesDone,
                              'user': name,
                              'isFinished': item.operationComplete,
                              'rate': rate, 'task': item.task,
                              'startTime': item.startTime,
                              'comments': item.comments}
                delta = item.endTime - item.startTime
                conversion = delta.days * 86400 + delta.seconds
                totalHours = totalHours + (conversion / 3600.0)
                totalPages = totalPages + item.pagesDone
            myList.append(dictionary)
    else:
        b = ProcessingSession.objects.all()
        dictionary = None
        for item in b:
            us = item.user.username
            if item.endTime is not None:
                rate = int(int(item.pagesDone) / (item.duration() / (60 * 60)))
                dictionary = {'barcode': item.item.barcode,
                              'itemType': item.item.itemType,
                              'duration': str(item.endTime - item.startTime),
                              'objects': item.pagesDone, 'user': us,
                              'isFinished': item.operationComplete,
                              'rate': rate, 'task': item.task,
                              'startTime': item.startTime,
                              'comments': item.comments}
                delta = item.endTime - item.startTime
                conversion = delta.days * 86400 + delta.seconds
                totalHours = totalHours + (conversion / 3600.0)
                totalPages = totalPages + item.pagesDone
            else:
                denominator = item.duration() / 3600
                rate = int(int(item.pagesDone) / denominator)
                dictionary = {'barcode': item.book.barcode,
                              'itemType': item.item.itemType,
                              'duration': None, 'objects': item.pagesDone,
                              'user': us,
                              'isFinished': item.operationComplete,
                              'rate': rate, 'task': item.task,
                              'startTime': item.startTime,
                              'comments': item.comments}
                delta = item.endTime - item.startTime
                conversion = delta.days * 86400 + delta.seconds
                totalHours = totalHours + (conversion / 3600.0)
                totalPages = totalPages + item.pagesDone
            myList.append(dictionary)
    paginator = Paginator(myList, 10)
    page = request.GET.get('page')
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1)
    except EmptyPage:
        rows = paginator.page(paginator.num_pages)

    return render_to_response('data.html', {
        'list': rows,
        'username': name,
        'totalHours': totalHours,
        'totalPages': totalPages,
        'start': start,
        'end': end,
    }, context_instance=RequestContext(request))


def logoutUser(request):
    logout(request)
    return render(request, 'logout.html')
