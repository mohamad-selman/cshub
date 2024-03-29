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
from .db import DB_connect
from django.core.mail import send_mail

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
            if request.POST['next']:
                return redirect(request.POST['next'])
            return redirect(dashboard)
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
    db, cursor = DB_connect()

    input = ''
    if request.method == 'POST':
        input = request.POST['input']

    if input != '' and input[0] == '0':
        input = input[1:]

    cursor.execute(f'''
        SELECT count(*) AS count
        FROM COURSE
        WHERE CAST(course_id as CHAR) LIKE '%{input}%';
    ''')
    count = cursor.fetchone()

    cursor.execute(f'''
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
        WHERE CAST(C.course_id as CHAR) LIKE '%{input}%'
        ORDER BY RC.count DESC;
    ''')
    
    courses = cursor.fetchall()

    context = {
        'count': count['count'],
        'courses': courses,
    }

    cursor.close()
    db.close()

    return render(request, 'results.html', context)

def course(request, cid=None):
    db, cursor = DB_connect()

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
    course = cursor.fetchone()

    context = {
        'course_id': cid,
        'course_name': course['course_name'],
        'count': course['count'],
        'watching': 'F',
    }

    if request.user.is_authenticated:
        cursor.execute(f'''
            SELECT *
            FROM USER_WATCH_COURSE
            WHERE user_id={request.user.id} AND course_id={cid};
        ''')
        watching = cursor.fetchone()

        if watching is not None:
            context['watching'] = 'T'

    for type in ['V','A','B','N','S','O']:
        cursor.execute(f'''
            SELECT R.resource_id, R.url, R.title, V.upvotes, V.downvotes, R.descr
            FROM S_RESOURCE R
            LEFT OUTER JOIN VOTES V
                ON R.resource_id = V.resource_id
            WHERE R.course_id={cid} AND R.type='{type}';
        ''')
        resources = cursor.fetchall()
        context[type] = resources

    cursor.close()
    db.close()

    return render(request, 'course.html', context)

@login_required(login_url='login')
def watch(request, cid=None):
    db, cursor = DB_connect()

    cursor.execute(f'''
        SELECT *
        FROM USER_WATCH_COURSE
        WHERE user_id={request.user.id} AND course_id={cid};
    ''')
    watching = cursor.fetchone()

    if watching is None:
        cursor.execute(f'''
            INSERT INTO USER_WATCH_COURSE
            VALUES({request.user.id}, {cid});
        ''')
    else:
        cursor.execute(f'''
            DELETE FROM USER_WATCH_COURSE
            WHERE user_id={request.user.id} AND course_id={cid};
        ''')

    cursor.close()
    db.close()

    return redirect(course, cid=cid)

@login_required(login_url='login')
def add(request, cid=None):
    db, cursor = DB_connect()

    cursor.execute(f'''
        SELECT course_name
        FROM COURSE
        WHERE course_id={cid};
    ''')
    course = cursor.fetchone()

    context = {
        'course_id': cid,
        'course_name': course['course_name']
    }

    cursor.close()
    db.close()

    return render(request, 'add.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def submit(request, cid=None):
    db, cursor = DB_connect()

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

    cursor.execute(f'''
        SELECT U.email, U.username
        FROM USER_WATCH_COURSE W
        JOIN auth_user U
            ON W.user_id = U.id
        WHERE W.course_id = {cid} and W.user_id != {request.user.id};
    ''')
    notify = cursor.fetchall()

    for u in notify:
        uname = u['username']
        send_mail(
            f'New resource get added to {cid}',
            f'Hi {uname}, a new resource get added to course {cid}.',
            'cshub.ku@yahoo.com',
            [u['email']],
            fail_silently = False, # will raise an smtplib.SMTPException if an error occured
        )

    context = {
        'course_id': cid
    }

    cursor.close()
    db.close()

    return render(request, 'submitted.html', context)

@login_required(login_url='login')
def vote(request, cid, rid):
    db, cursor = DB_connect()

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

    elif exsited_vote['vote_type'] == requested_vote:
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

    cursor.close()
    db.close()

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
    db, cursor = DB_connect()

    descr = request.POST['descr']

    cursor.execute(f'''
        INSERT INTO USER_REPORT_RESOURCE(user_id, resource_id, descr)
        VALUE({request.user.id}, '{rid}', '{descr}');
    ''')

    context = {
        'course_id': cid
    }

    cursor.close()
    db.close()

    return render(request, 'submitted.html', context)

def admin_report(request):
    db, cursor = DB_connect()

    cursor.execute(f'''
        SELECT count(*) as count
        FROM USER_REPORT_RESOURCE;
    ''')
    total = cursor.fetchone()

    cursor.execute(f'''
        SELECT RE.resource_id, RE.report_id, RE.user_id, RE.report_date, RE.descr as comment, R.title, R.descr
        FROM USER_REPORT_RESOURCE RE
        JOIN S_RESOURCE R
            ON RE.resource_id = R.resource_id;
    ''')
    reports = cursor.fetchall()

    context = {
        'count': total['count'],
        'reports': reports,
    }

    cursor.close()
    db.close()

    return render(request, 'all_reports.html', context)

@login_required(login_url='login')
def dashboard(request):
    db, cursor = DB_connect()

    cursor.execute(f'''
        SELECT count(*) as count
        FROM S_RESOURCE
        WHERE user_id = {request.user.id};
    ''')
    total = cursor.fetchone()

    cursor.execute(f'''
        SELECT *
        FROM S_RESOURCE
        WHERE user_id = {request.user.id};
    ''')
    resources = cursor.fetchall()

    context = {
        'count': total['count'],
        'resources': resources,
    }

    cursor.close()
    db.close()

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def delete(request, rid):
    db, cursor = DB_connect()

    cursor.execute(f'''
        SELECT user_id
        FROM S_RESOURCE
        WHERE resource_id={rid};
    ''')
    added_by = cursor.fetchone()

    if added_by['user_id'] == request.user.id or request.user.is_superuser:
        cursor.execute(f'''
            DELETE FROM S_RESOURCE
            WHERE resource_id={rid};
        ''')
        print("The resource was removed successfully")

    cursor.close()
    db.close()

    if request.user.is_superuser:
            return redirect(admin_report)
    return redirect(dashboard)

def error(request):
    return render(request, 'error.html')
