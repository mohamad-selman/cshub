from distutils.log import info
from re import S
import resource
from django.shortcuts import render, redirect
from django.http import HttpResponse
from regex import D
from requests import request
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import connection
cursor = connection.cursor()

def dictfetchone(cursor):
    desc = cursor.description
    row = cursor.fetchone()
    return dict(zip([col[0] for col in desc], row))

def dictfetchall(cursor): 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall()
    ]

def index(request):
    return render(request, 'index.html')

def login_u(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, './login.html')

def logout_u(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        fname = request.POST['name']
        username = request.POST['username']
        user_email = request.POST['email']
        passw = request.POST['password']

        try:
            User.objects.create_user(password=passw, username=username, first_name=fname, email=user_email)
            return redirect('login')
        except:
            return render(request, './error.html')
    return render(request, './signup.html')

def results(request):
    cursor.execute('''
        SELECT count(*) AS count
        FROM COURSE
    ''')
    count = dictfetchone(cursor)

    cursor.execute('''
        SELECT C.course_id, C.course_name, D.dept_name, RC.count
        FROM COURSE C
        JOIN DEPARTMENT D
            ON C.dept_id=D.dept_id
        LEFT OUTER JOIN (
                SELECT course_id, count(resource_id) AS count
                FROM S_RESOURCE
                GROUP BY course_id
            ) RC
            ON C.course_id=RC.course_id
        ORDER BY RC.count DESC;
    ''')
    
    courses = dictfetchall(cursor)

    context = {
        'count': count['count'],
        'courses': courses
    }

    return render(request, 'results.html', context)

def course(request, cid=None):
    cursor.execute(f'''
        SELECT C.course_name, RC.count
        FROM COURSE C
        LEFT OUTER JOIN (
                SELECT course_id, count(resource_id) AS count
                FROM S_RESOURCE
                GROUP BY course_id
            ) RC
            ON C.course_id=RC.course_id
        WHERE C.course_id={cid};
    ''')
    course = dictfetchone(cursor)

    context = {
        'course_id': cid,
        'course_name': course['course_name'],
        'count': course['count']
    }

    for type in ['V','A','B','N','S','O']:
        cursor.execute(f'''
            SELECT R.resource_id, R.url, R.title, V.upvotes, V.downvotes, R.descr
            FROM S_RESOURCE R
            LEFT OUTER JOIN VOTES V
                ON R.resource_id = V.resource_id
            WHERE R.course_id={cid} AND R.type='{type}';
        ''')
        resources = dictfetchall(cursor)
        context[type] = resources

    return render(request, 'course.html', context)

@login_required(login_url='login')
def add(request, cid=None):
    cursor.execute(f'''
        SELECT course_name
        FROM COURSE
        WHERE course_id={cid};
    ''')
    course = dictfetchone(cursor)

    context = {
        'course_id': cid,
        'course_name': course['course_name']
    }

    return render(request, 'add.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def submit(request, cid=None):
    type = request.POST['type']
    title = request.POST['title']
    url = request.POST['url']
    descr = request.POST['descr']

    url = url.replace("http://","")
    url = url.replace("https://","")

    cursor.execute(f'''
        INSERT INTO S_RESOURCE(course_id, type, title, url, descr, user_id)
        VALUE({cid}, '{type}', '{title}', '{url}', '{descr}', {request.user.id});
    ''')

    context = {
        'course_id': cid
    }

    return render(request, 'submitted.html', context)

@login_required(login_url='login')
def vote(request, cid, rid):
    requested_vote = request.POST['vote']

    cursor.execute(f'''
        SELECT vote_type
        FROM USER_VOTE_RESOURCE
        WHERE resource_id={rid} AND user_id={request.user.id};
    ''')
    exsited_vote = cursor.fetchone()

    if exsited_vote == None:
        cursor.execute(f'''
            INSERT INTO USER_VOTE_RESOURCE(user_id, resource_id, vote_type)
            VALUE({request.user.id}, {rid}, '{requested_vote}');
        ''')
        print("Your vote was recorded successfully")

    elif exsited_vote[0][0] == requested_vote:
        cursor.execute(f'''
            DELETE FROM USER_VOTE_RESOURCE
            WHERE resource_id={rid} AND user_id={request.user.id};
        ''')
        print("Your vote was removed successfully")

    else:
        cursor.execute(f'''
            UPDATE USER_VOTE_RESOURCE
            SET vote_type='{requested_vote}'
            WHERE resource_id={rid} AND user_id={request.user.id};
        ''')
        print("Your vote was changed successfully")

    return redirect(course, cid=cid)

@login_required(login_url='login')
def report(request, cid=None, rid=None):
    context = {
        'course_id': cid,
        'resource_id': rid,
    }

    return render(request, 'report.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def submit_report(request, cid=None, rid=None):
    descr = request.POST['descr']

    cursor.execute(f'''
        INSERT INTO USER_REPORT_RESOURCE(user_id, resource_id, descr)
        VALUE({request.user.id}, '{rid}', '{descr}');
    ''')

    context = {
        'course_id': cid
    }

    return render(request, 'submitted.html', context)

def admin_report(request):
    cursor.execute(f'''
        SELECT count(*) as count
        FROM USER_REPORT_RESOURCE;
    ''')
    total = dictfetchone(cursor)

    cursor.execute(f'''
        SELECT *
        FROM USER_REPORT_RESOURCE;
    ''')
    reports = dictfetchall(cursor)

    context = {
        'count': total['count'],
        'reports': reports,
    }

    return render(request, 'all_reports.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')

def error(request):
    return render(request, 'error.html')
