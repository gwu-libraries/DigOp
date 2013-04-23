from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset, \
    password_change_done as auth_password_change_done
from django.contrib.messages import constants as messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import Library, RequestContext
from django.utils import simplejson as json
from operator import itemgetter

from ui.models import BookForm
from ui.models import CloseProjectForm
from ui.models import ItemProcessingForm
from ui.models import Item
from ui.models import LoginForm
from ui.models import ProcessingForm
from ui.models import ProcessingSession
from ui.models import ProfileForm
from ui.models import ProjectForm
from ui.models import Project
from ui.models import UserProfile

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
        return HttpResponseRedirect('/index_page/')
    if request.method == 'POST':  # If the form has been submitted...
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            use = authenticate(username=username, password=password)
            request.session['user_id'] = use
            if use is not None:
                auth_login(request, use)
                return HttpResponseRedirect('/index_page/')
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
def user_json(request, username):
    dictionary = user(request, username, json_view=True)
    return HttpResponse(json.dumps(dictionary, default=_date_handler),
                        content_type='application/json')


def _date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj


@login_required
def edit_profile(request, pk):
    return profile_views.edit_profile(request, form_class=ProfileForm)


@login_required
def password_change_done(request,
                         template='accounts/my_password_change_done.html'):
    return auth_password_change_done(request, template_name=template)


@login_required
def profile_menu(request):
    return render(request, 'profile_menu.html')

@login_required
def project(request):
    return render(request, 'project_menu.html')


@login_required
def item_menu(request):
    return render(request, 'item_menu.html')


@login_required
def project_form(request):
    return render(request,'add_project.html')


@login_required
def close_project(request):
    def errorHandle(error):
        form = CloseProjectForm()
        return render_to_response('close_project_form.html', {
            'error': error,
            'form': form,
        }, context_instance=RequestContext(request))
    if request.method == 'POST':  # If the form has been submitted...
        project = Project.objects.get(pk=request.POST['name'])
        form = CloseProjectForm(request.POST, instance=project)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return render(request, 'project_menu.html')
        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = CloseProjectForm()  # An unbound form
        return render_to_response('close_project_form.html',  {
            'form': form,
        }, context_instance=RequestContext(request))


def reset_done(request):
    return render(request, 'reset_done.html')


@login_required
def view_profile(request):
        return render(request, 'view_profile.html', {
            'profile': UserProfile.objects.get(user=request.user),
        })


def reset_password(request, template_name='reset_password.html'):
        return password_reset(request, template_name)


@login_required
def index_page(request):
    if request.user.is_superuser:
        return render_to_response('admin_page.html', {
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('user_page.html', {
        }, context_instance=RequestContext(request))


@login_required
def admin_session_data(request):
    projects = Project.objects.all()
    open_projects = []
    for p in projects:
        if p.projectComplete == False:
            open_projects.append(p)
    form = BookForm()
    return render_to_response('get_barcode.html', {
        'projects': open_projects,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def display_item_processing_form(request):
    projects = Project.objects.all()
    open_projects = []
    for p in projects:
        if p.projectComplete == False:
            open_projects.append(p)
    form = BookForm()
    return render(request, 'process_item_form.html', {
        'projects': open_projects,
        'form': form,
    })


@login_required
def show_users(request):
    return render_to_response('admin_login.html', {
        'users': User.objects.all(),
    }, context_instance=RequestContext(request))


@login_required
def show_graph(request,chartType):
    userObjects = User.objects.all()
    users = []
    low = 0
    high = 0
    values = []
    valuesList = []
    entryList = []
    hoursList = []
    projectsList = []
    if chartType == 'pie' or chartType == 'bar':
        for u in userObjects:
            users.append(u.username)
            userrows = ProcessingSession.objects.filter(user=u)
            pages = 0
            hours = 0
            for row in userrows:
                pages = pages + row.pagesDone
                hours = hours + row.duration()
            if pages < low:
                low = pages
            if pages > high:
                high = pages
            valuesList.append(u.username + '(' + str(pages) + ')')
            entryList.append(pages)
            hoursList.append(hours)
        values.append(entryList)
        if chartType == 'pie':
            return render_to_response('pie_chart.html', {
                'users': users,
                'low': low,
                'high': high,
                'hours': hoursList,
                'values': zip(users, entryList),
                'testValues': values,
                'entries': entryList,
                'chartType': chartType,
            }, context_instance=RequestContext(request))
        else:
            return render_to_response('bar_chart.html', {
                'users': users,
                'low': low,
                'high': high,
                'hours': hoursList,
                'values': zip(users, entryList),
                'testValues': values,
                'entries': entryList,
                'chartType': chartType,
            }, context_instance=RequestContext(request))

    elif chartType=='combo':
        projects = Project.objects.all()
        for p in projects:
            items = Item.objects.filter(project=p)
            num_items = 0
            for i in items:
                num_items = num_items + 1
            entryList.append(num_items)
            projectsList.append(p.name)
        return render(request, 'combo_chart.html', {
            'values': zip(projectsList, entryList),
            'chartType': chartType,
        })
    else:
        projects = Project.objects.all()
        projList = []
        for p in projects:
            projList.append(p)
        return render(request, 'time_graph_form.html', {
            'projects': projList,
        })


@login_required
def display_time_line_graph(request):
    if request.method == 'POST':  # If the form has been submitted...
        project_id = request.POST['project']
        p = Project.objects.get(pk=project_id)
        items = Item.objects.filter(project=p)
        values = []
        for i in items:
            item_data = ProcessingSession.objects.filter(item=i)
            for val in item_data:
                row = {}
                row['Date'] = val.startTime
                row['objects'] = val.pagesDone
                row['task'] = val.task
                values.append(row)
        sorted_values = sorted(values, key=itemgetter('Date'))
        return render(request, 'time_chart.html' , {
            'values': sorted_values,
        })


@login_required
def show_projects(request):
    projects = Project.objects.all()
    rows = []
    for p in projects:
        items = Item.objects.filter(project=p)
        num_items = 0
        for i in items:
            num_items = num_items + 1
        data = {}
        data['project'] = p.name
        data['description'] = p.description
        data['start'] = p.startDate 
        data['end'] = p.endDate
        data['closed'] = p.projectComplete
        data['items'] = num_items
        rows.append(data)
    return render(request, 'show_projects.html' , {
        'rows': rows,
    })


@login_required
def barcode_page(request):
    return render_to_response('barcode_report_form.html', {
    }, context_instance=RequestContext(request))


@login_required
def barcode_report(request):
    if request.method == 'POST':  # If the form has been submitted...
        bar = request.POST['barcode']
        dictionary = {}
        values = []
        try:
            book = Item.objects.filter(barcode=bar)
        except Item.DoesNotExist:
            err_msg = 'Barcode does not exist '
            messages.add_message(request, messages.ERROR, err_msg)
            return render_to_response('barcode_result.html', {
                'list': values,
            }, context_instance=RequestContext(request))
        result = ProcessingSession.objects.filter(item=book)
        for rec in result:
            dictionary['project'] = rec.item.project
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
        return render_to_response('barcode_result.html', {
            'list': values,
        }, context_instance=RequestContext(request))


@login_required
def barcode_json(request, identifier):
    dictionary = barcode(request, identifier, json_view=True)
    return HttpResponse(json.dumps(dictionary, default=_date_handler),
                        content_type='application/json')


@login_required
def barcode(request, identifier, json_view=False):
    dictionary = {}
    values = []
    book = None
    try:
        book = Item.objects.filter(barcode=identifier)
    except Item.DoesNotExist:
        return render_to_response('barcode_result.html', {
            'list': values,
            'barcode': identifier,
        }, context_instance=RequestContext(request))
    result = ProcessingSession.objects.filter(item=book)
    for rec in result:
        dictionary['project'] = rec.item.project
        dictionary['itemType'] = rec.item.itemType
        dictionary['barcode'] = rec.item.barcode
        dictionary['duration'] = str(rec.endTime - rec.startTime)
        dictionary['objects'] = rec.pagesDone
        dictionary['user'] = rec.user.username
        dictionary['isFinished'] = rec.operationComplete
        rate_of_work = int(int(rec.pagesDone) / (rec.duration() / 3600))
        dictionary['rate'] = rate_of_work
        dictionary['task'] = rec.task
        dictionary['startTime'] = rec.startTime
        values.append(dictionary)
    if json_view:
        dataset = {'Sessions': values}
        return dataset
    else:
        return render_to_response('data.html', {
            'list': values,
        }, context_instance=RequestContext(request))


@login_required
def project_data_json(request, identifier):
    dictionary = project_data(request, identifier, json_view=True)
    return HttpResponse(json.dumps(dictionary, default=_date_handler),
                        content_type='application/json')


@login_required
def project_data(request, identifier, json_view=False):
    dictionary = {}
    values = []
    p = None
    try:
        p = Project.objects.get(name=identifier)
    except Project.DoesNotExist:
        return render_to_response('barcode_result.html', {
            'list': values,
            'project': identifier,
        }, context_instance=RequestContext(request))
    item = Item.objects.filter(project=p)
    for i in item:
        result = ProcessingSession.objects.filter(item=i)
        for rec in result:
            dictionary['project'] = rec.item.project
            dictionary['itemType'] = rec.item.itemType
            dictionary['barcode'] = rec.item.barcode
            dictionary['duration'] = str(rec.endTime - rec.startTime)
            dictionary['objects'] = rec.pagesDone
            dictionary['user'] = rec.user.username
            dictionary['isFinished'] = rec.operationComplete
            rate_of_work = int(int(rec.pagesDone) / (rec.duration() / 3600))
            dictionary['rate'] = rate_of_work
            dictionary['task'] = rec.task
            dictionary['startTime'] = rec.startTime
            values.append(dictionary)
    if json_view:
        dataset = {'Sessions': values}
        return dataset
    else:
        return render_to_response('data.html', {
            'list': values,
        }, context_instance=RequestContext(request))


@login_required
def report_menu(request):
    return render_to_response('report_menu.html', {
    }, context_instance=RequestContext(request))


@login_required
def process_item_form(request):
    def errorHandle(error):
        form = BookForm()
        return render_to_response('process_item_form.html', {
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
                    proj = Project.objects.get(pk=request.POST['project'])
                    book = Item.objects.create(project=proj,barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    task_type = request.POST['taskType']
                    return render_to_response('processing_form.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': task_type,
                                                        }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
                else:
                    task_type = request.POST['taskType']
                    return render_to_response('processing_form.html', {
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
                    book = Item.objects.create(project=request.POST['project'],barcode=bar, totalPages=pages,
                                               itemType=item_type)
                    book.save()
                    task_type = request.POST['taskType']
                    user = request.user
                    return render_to_response('item_processing_form.html', {
                        'form': ItemProcessingForm(initial={'item': book,
                                                            'user': user,
                                                            'task': task_type,
                                                            }),
                        'itemType': request.POST['itemType'],
                        'task': request.POST['taskType'],
                    }, context_instance=RequestContext(request))
                else:
                    task_type = request.POST['taskType']
                    user = request.user
                    return render_to_response('item_processing_form.html', {
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
        return render_to_response('process_item_form.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def process_book_form(request):
    def errorHandle(error):
        form = BookForm(request.POST)
        return render_to_response('get_barcode.html', {
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
                    p = Project.objects.get(id=request.POST['project'])
                    book = Item.objects.create(barcode=bar, totalPages=pages,
                                               itemType=item_type, project=p)
                    book.save()
                    return render_to_response('processing_form.html', {
                        'form': ProcessingForm(initial={'item': book,
                                                        'user': request.user,
                                                        'task': 'Scan',
                                                        }),
                        'itemType': request.POST['itemType'],
                        'task': 'Scan',
                        'item': book,
                    }, context_instance=RequestContext(request))
                else:
                    return render_to_response('processing_form.html', {
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
                    return render_to_response('item_processing_form.html', {
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
                    return render_to_response('item_processing_form.html', {
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
        return render_to_response('get_barcode.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def process_processing_form(request):
    def errorHandle(error):
        if request.POST['itemType'] in ['Book', 'Map']:
            form = ProcessingForm(request.POST)
            return render_to_response('processing_form.html', {
                'error': error,
                'form': form,
                'task': request.POST['task'],
                'itemType': request.POST['itemType'],
            }, context_instance=RequestContext(request))
        else:
            form = ItemProcessingForm(request.POST)
            return render_to_response('item_processing_form.html', {
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
                return render_to_response('get_barcode.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ProcessingForm()  # An unbound form
        return render_to_response('processing_form.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def add_project(request):
    def errorHandle(error):
        form = ProjectForm(request.POST)
        return render_to_response('add_project.html', {
            'error': error,
            'form': form,
        },context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project(name=request.POST['name'], description=request.POST['description'], startDate=request.POST['startDate'], endDate=None, projectComplete=False)
            project.save()
            return render(request,'project_menu.html')
        else:
            error = 'form is invalid'
            return errorHandle(error)
    else:
        form = ProjectForm()
        return render_to_response('add_project.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def item_processing_form(request):
    def errorHandle(error):
        form = ItemProcessingForm(request.POST)
        return render_to_response('item_processing_form.html', {
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
                return render_to_response('get_barcode.html', {
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
        return render_to_response('item_processing_form.html', {
            'form': form,
        }, context_instance=RequestContext(request))


@login_required
def user(request, username, json_view=False):
    myList = []
    totalPages = 0
    totalHours = 0
    a = ProcessingSession.objects.filter(user__username=username)
    dictionary = {}
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'project': item.item.project,
                          'barcode': item.item.barcode,
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
            dictionary = {'project': item.item.project,
                          'barcode': item.book.barcode,
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
    if json_view:
        return {'Sessions': myList,
                'username': username,
                'totalHours': totalHours,
                'totalPages': totalPages,
                }
    else:
        return render_to_response('data.html', {
            'list': myList,
            'username': username,
            'totalHours': totalHours,
            'totalPages': totalPages,
        }, context_instance=RequestContext(request))


@login_required
def task_json(request, tasktype):
    dict = task(request, tasktype, json_view=True)
    return HttpResponse(json.dumps(dict, default=_date_handler,
                        indent=2), content_type='application/json')


@login_required
def task(request, tasktype, json_view=False):
    a = ProcessingSession.objects.filter(task__exact=tasktype)
    totalPages = 0
    totalHours = 0
    dictionary = {}
    myList = []
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'project': item.item.project,
                          'barcode': item.item.barcode,
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
            dictionary = {'project': item.item.project,
                          'barcode': item.book.barcode,
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
    if json_view:
        return {
            'Sessions': myList,
            'totalHours': totalHours,
            'totalPages': totalPages,
        }
    else:
        return render_to_response('data.html', {
            'list': myList,
            'totalHours': totalHours,
            'totalPages': totalPages,
        }, context_instance=RequestContext(request))


@login_required
def item_json(request, itemtype):
    dictionary = item(request, itemtype, json_view=True)
    return HttpResponse(json.dumps(dictionary, default=_date_handler,
                        indent=2), content_type='application/json')


@login_required
def item(request, itemtype, json_view=False):
    a = ProcessingSession.objects.filter(item__itemType__exact=itemtype)
    totalPages = 0
    totalHours = 0
    dictionary = {}
    myList = []
    for item in a:
        rate = int(int(item.pagesDone) / (item.duration() / 3600))
        if item.endTime is not None:
            dictionary = {'project': item.item.project,
                          'barcode': item.item.barcode,
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
            dictionary = {'project': item.item.project,
                          'barcode': item.book.barcode,
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
    if json_view:
        return {
            'Sessions': myList,
            'totalHours': totalHours,
            'totalPages': totalPages,
        }
    else:
        return render_to_response('data.html', {
            'list': myList,
            'totalHours': totalHours,
            'totalPages': totalPages,
        }, context_instance=RequestContext(request))


@login_required
def produce_data(request):
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
                dictionary = {'project': item.item.project,
                              'barcode': item.item.barcode,
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
                dictionary = {'project': item.item.project,
                              'barcode': item.book.barcode,
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
                dictionary = {'project': item.item.project,
                              'barcode': item.item.barcode,
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
                dictionary = {'project': item.item.project,
                              'barcode': item.book.barcode,
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
    #paginator = Paginator(myList, 10)
    #page = request.GET.get('page')
    #try:
        #rows = paginator.page(page)
    #except PageNotAnInteger:
        #rows = paginator.page(1)
    #except EmptyPage:
        #rows = paginator.page(paginator.num_pages)

    return render_to_response('data.html', {
        'list': myList,
        'username': name,
        'totalHours': totalHours,
        'totalPages': totalPages,
        'start': start,
        'end': end,
    }, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return render(request, 'logout.html')
