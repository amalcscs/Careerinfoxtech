from ast import Or
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from app.models import *
from aptitude.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.defaults import page_not_found
from django.contrib import messages
import random
import json
from datetime import datetime
import datetime

def Register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        contact = request.POST['contact']
        qualification = request.POST['qualifcation']
        college = request.POST['college']
        passoutyr = request.POST['passoutyr']
        username = email
        password = random.randint(10000, 99999)
        reference = request.POST['reference']
        dept = request.POST['dept']
        if candidates.objects.filter(email=email).exists():
            msg_warning = "Mail id exists"
            return render(request, 'user_registration.html', {'msg_warning': msg_warning})
        else:
            register = candidates(fullname=fname, email=email, contact_no=contact,
                                  qualifications=qualification, passout_year=passoutyr, college=college,
                                  username=username, password=password, reference=reference, deptmnt_id=dept, regdate=datetime.datetime.now())
            register.save()
            messages.success(
                request, 'username and password for exam is sent to your registered mail id.........')
            member = candidates.objects.get(id=register.id)
            subject = 'Greetings from iNFOX TECHNOLOGIES'
            message = 'Congratulations,\n' \
                'You have successfully registered with iNFOX TECHNOLOGIES.\n' \
                'following is your login credentials for taking aptitude test\n'\
                'username :'+str(member.username)+'\n' 'password :'+str(member.password) + \
                '\n' 'ALL THE BEST WISHES FOR YOUR TEST ' + \
                '\n' 'Login to test :https://careerinfoxtechnologies.com/'
            recepient = str(email)
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient], fail_silently=False)
            msg_success = "Registration completed Check Your Mail"
            return render(request, 'user_registration.html', {'msg_success': msg_success})

    else:
        des = designation.objects.get(designation='HR')
        vars = login.objects.filter(designation_id=des.id)
        vars1 = department.objects.all()
        return render(request, 'user_registration.html', {'var': vars, 'vars1': vars1})


def Login(request):
    des = designation.objects.get(designation='HR')
    tims = exam_timing.objects.get(id=1)
    current_datetime = datetime.datetime.now()
    
    if request.method == 'POST':

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard')

        elif login.objects.filter(email=request.POST['username'], password=request.POST['password'], designation_id=des.id).exists():
            member = login.objects.get(
                email=request.POST['username'], password=request.POST['password'])
            request.session['usernamehr'] = member.designation_id
            request.session['usernamehr1'] = member.fullname
            request.session['usernamehr2'] = member.id

            return render(request, 'hrsec.html', {'member': member})
        else:

            try:

                tm = exam_timing.objects.get(
                    from_date_time__lte=current_datetime, to_date_time__gte=current_datetime, id=1)
                if tm:

                    if candidates.objects.filter(email=request.POST['username'], password=request.POST['password']).exists():
                        mem = candidates.objects.get(
                            password=request.POST['password'], email=request.POST['username'])
                        request.session['username'] = mem.username
                        request.session['username1'] = mem.id
                        request.session['username2'] = mem.exam_status
                        request.session['username3'] = mem.email
                        request.session['username4'] = mem.deptmnt_id
                        username = request.session['username']
                        username1 = request.session['username1']
                        username2 = request.session['username2']
                        username3 = request.session['username3']
                        username4 = request.session['username4']
                        sn = 0
                        c = catagory.objects.all()
                        for i in c:
                            sn = sn+i.time_taken
                        if username2 == '0':
                            return render(request, 'aptitude_instructions.html', {'username': username, 'sn': sn, 'mem': mem})
                        else:
                            return redirect('/')

                    else:
                        context = {'msg_error': 'Invalid data'}
                        return render(request, 'user_login.html', context)

            except exam_timing.DoesNotExist:

                context = {
                    'msg_error': "Access Not avalable now. Attend Exam on right time"}
                return render(request, 'user_login.html', context)

    return render(request, 'user_login.html')


def aptitude_catagory(request):
    if 'username1' in request.session:
        if request.session.has_key('username'):
            username = request.session['username']
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username2'):
            username2 = request.session['username2']
        else:
            return redirect('/')

        m = catagory.objects.all()

        mem = candidates.objects.get(username=username)
        return render(request, 'aptitude_catagory.html', {'username': username, 'm': m, 'mem': mem})
    else:
        return redirect('/')


def his_id(request):
    if 'username1' in request.session:
        if request.session.has_key('username'):
            username = request.session['username']
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username3'):
            username3 = request.session['username3']
        if request.session.has_key('username4'):
            username4 = request.session['username4']
        else:
            return redirect('/')
        delete_id = request.GET.get('id')
        z = candidates.objects.get(id=delete_id)
        z.exam_status = 1
        z.save()
        msg = "success"
        return HttpResponse(json.dumps({'msg': msg}))
    else:
        return redirect('/')


def start(request, id):
    if 'username1' in request.session:
        if request.session.has_key('username'):
            username = request.session['username']
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username3'):
            username3 = request.session['username3']
        if request.session.has_key('username4'):
            username4 = request.session['username4']
        else:
            return redirect('/')

        mem = candidates.objects.get(username=username)
        var = catagory.objects.get(id=id)

        try:

            tm = time_out.objects.get(user_id=username1, category_id=id)
            return redirect('aptitude_catagory')
        except time_out.DoesNotExist:

            cnt = var.no_of_question
            j = question.objects.filter(ctgry_id=id).count()


            if var.name == "Technical_ability":

                if int(cnt) <= j:
                    vars = question.objects.filter(
                        ctgry_id=var.id, dept_id=username4).order_by('?')[0:int(cnt)]
                    return render(request, 'aptitude_start.html', {'vars': vars, 'username': username, 'var': var, 'mem': mem})
                else:
                    return redirect('aptitude_catagory')
            else:
                if int(cnt) <= j:
                    vars = question.objects.filter(
                        ctgry_id=var.id).order_by('?')[0:int(cnt)]
                    return render(request, 'aptitude_start.html', {'vars': vars, 'username': username, 'var': var, 'mem': mem})
                else:
                    return redirect('aptitude_catagory')
    else:
        return redirect('/')


def submit(request, id):
  
    if 'username1' in request.session:
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username'):
            username = request.session['username']

        else:
            return redirect('/')
        if request.method == 'POST':

            try:

                vars = catagory.objects.get(id=id)
                ques1 = question.objects.filter(ctgry_id=vars.id).values()
                score = 0
                try:
                    dct = json.loads(request.POST['myval'])
                    flag = True
                except:
                    dct = {}
                    flag = False
                for item in ques1:
                    if flag and item['questions'] in dct['dct'].keys():
                        option = dct['dct'][item['questions']].replace(' ', '')

                    elif request.POST.get(item['questions']):
                        option = request.POST.get(
                            item['questions']).replace(' ', '')
                    else:
                        option = ''

                    if item['correct_option'].replace(' ', '') == option:
                        score = score+10
                        print(score)

                    else:
                        pass
                user = candidates.objects.get(id=username1)
                user.mark = score+user.mark
                user.save()
                print(user.mark)

                s = catagory.objects.all()
                c = catagory.objects.filter(time_taken=vars.time_taken)

                time = vars.id
                user = username1
                mm = time_out(category_id=time, user_id=user)
                mm.save()
                lst_cat = list(time_out.objects.filter(
                    user_id=username1).values_list('category_id', flat=True))

                m = catagory.objects.exclude(id__in=lst_cat).values()
                msg_success = "This section completed"
                return render(request, 'aptitude_start.html', {'msg_success': msg_success, 'username': username, 'm': m})
            except:
                return redirect('aptitude_catagory')
        else:
            return redirect('aptitude_catagory')


def saved(request, id):

    if 'username1' in request.session:
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username3'):
            username3 = request.session['username3']
        else:
            return redirect('/')
        if request.method == 'POST':
            try:
                vars = catagory.objects.get(id=id)
                time = vars.id
                user = username1
                x = time_out(category_id=time, user_id=user, exam_status=1)
                x.save()
                ques1 = question.objects.filter(ctgry_id=vars.id).values()
                score = 0
                try:
                    dct = json.loads(request.POST['myval'])
                    flag = True
                except:
                    dct = {}
                    flag = False
                for item in ques1:
                    if flag and item['questions'] in dct['dct'].keys():
                        option = dct['dct'][item['questions']].replace(' ', '')

                    elif request.POST.get(item['questions']):
                        option = request.POST.get(
                            item['questions']).replace(' ', '')
                    else:
                        option = ''

                    if item['correct_option'].replace(' ', '') == option:
                        score = score+10
                        print(score)

                    else:
                        pass
                user = candidates.objects.get(id=username1)
                user.mark = score+user.mark

                user.save()
                print(user.mark)
                msg_warning = "This section completed"
                return render(request, 'aptitude_catagory.html', {'msg_warning': msg_warning})
            except:
                return redirect('aptitude_catagory')

        else:
            return redirect('aptitude_catagory')


def total(request):
    if 'username1' in request.session:
        if request.session.has_key('username'):
            username = request.session['username']
        if request.session.has_key('username1'):
            username1 = request.session['username1']
        if request.session.has_key('username3'):
            username3 = request.session['username3']
        else:
            return redirect('/')
        user = candidates.objects.get(id=username1)
        user.exam_status = 1
        user.save()
        subject = 'Thankyou For taking Online test'
        message = 'Congratulations,\n' \
            'You have successfully completed online aptitude test.\n' \
                  'If you got selected you will contacted by Hr shortly.\n' \
            'All the best !!!'
        send_mail(subject, message, EMAIL_HOST_USER,
                  [username3], fail_silently=False)
        msg_succ = "You are sucessfully completed test! All the best.If you got selected you will be contacted by Hr shortly."
        return render(request, 'aptitude_catagory.html', {'msg_succ': msg_succ})
    else:
        return redirect('/')

# ******************ADMIN AND HR ******************

def reqflush(request):
  request.session.flush()
  return redirect("/")

def logout(request):
    auth.logout(request)
    return redirect("/")

# def admin_dashboard(request):
#       mem = User.objects.all()

#       que = catagory.objects.all()
#       dep = department.objects.values().exclude(name="Default")
#       des1 = department.objects.get(name='Python')
#       des2 = department.objects.get(name='Machine learning')
#       count_python = question.objects.filter(dept_id = des1.id).count()
#       count_ML = question.objects.filter(dept_id = des2.id).count()
#       print(dep)
#       print('hai')
#       return render(request, 'admin_dashboard.html', {'mem': mem, 'que':que,'dep':dep ,'count_python':count_python, 'count_ML':count_ML})


def admin_dashboard(request):
    mem = User.objects.all()

    que = catagory.objects.all()
    return render(request, 'admin_dashboard.html', {'mem': mem, 'que': que, })


def Dashboard(request):
    mem = User.objects.all()
    return render(request, 'Dashboard.html', {'mem': mem})


def add_question(request):
    mem = User.objects.all()
    vars = catagory.objects.all()
    var = department.objects.all().exclude(name='Default')
    z = question()
    if request.method == 'POST':
        z.questions = request.POST['question']
        z.option1 = request.POST['opt1']
        z.option2 = request.POST['opt2']
        z.option3 = request.POST['opt3']
        z.option4 = request.POST['opt4']
        z.correct_option = request.POST['answer']
        a = request.POST['form_select']
        ab = catagory.objects.get(name=a)
        c = request.POST['Categorysel']
        print(a)
        print(c)
        abc = department.objects.get(name=c)
        z.ctgry_id = ab.id
        z.dept_id = abc.id
        z.save()
        return redirect('Dashboard')
    return render(request, 'add_question.html', {'mem': mem, 'z': z, 'vars': vars, 'var': var})


def admin_add_limit(request):
    mem = User.objects.all()
    z = adminlimit()
    if request.method == 'POST':
        z.no_of_question = request.POST['noqstn']
        z.time_taken = request.POST['appt']
        z.save()
        return redirect('Dashboard')
    return render(request, 'admin_add_limit.html', {'mem': mem})


def view_questions(request, id1, id2):
    var = department.objects.get(id=id2)
    var1 = catagory.objects.get(id=id1)
    mem = User.objects.all()
    i = question.objects.filter(ctgry_id=var1.id, dept_id=var.id)
    return render(request, 'view_questions.html', {'mem': mem, 'i': i})


def view_questionss(request, id1):
    var1 = catagory.objects.get(id=id1)
    mem = User.objects.all()
    i = question.objects.filter(ctgry_id=var1.id)
    return render(request, 'view_questions.html', {'mem': mem, 'i': i})


def view_question_update(request, id):
    mem = User.objects.all()
    if request.method == 'POST':
        vars = question.objects.get(id=id)
        vars.questions = request.POST['question']
        vars.option1 = request.POST['opt1']
        vars.option2 = request.POST['opt2']
        vars.option3 = request.POST['opt3']
        vars.option4 = request.POST['opt4']
        vars.correct_option = request.POST['answer']
        vars.save()
        return redirect("Dashboard")
    return render(request, 'view_questions.html', {'mem': mem})


def view_question_delete(request, id):
    mem = User.objects.all()
    var = question.objects.filter(id=id)
    var.delete()
    return redirect("Dashboard")


def admin_allMembers(request):
    mem = User.objects.all()
    des = designation.objects.get(designation='HR')
    desgn = login.objects.filter(designation_id=des.id)
    var = candidates.objects.all()
    return render(request, 'admin_allMembers.html', {'mem': mem, 'var': var, 'desgn': desgn})


def admin_allMembers_reference(request):
    mem = User.objects.all()
    desgn = candidates.objects.all()
    j = request.POST['refer']
    if request.method == 'POST':
        ref = request.POST['refer']
        if request.POST.get('att'):
            vi = request.POST.get('att')
            vi = str(vi)
            l = len(vi)
            vii = vi[0:l-1]
            present = vii.split(",")
            key = []
            for i in present:
                key.append(i)
            for i in key:
                new = candidates.objects.get(id=i)
                new.reference = ref
                new.save()
            return redirect('admin_allMembers')
    return render(request, 'admin_allMembers.html', {'mem': mem, 'desgn': desgn})


def NO_ref(request):
    mem = User.objects.all()
    des = designation.objects.get(designation='HR')
    desgn = login.objects.filter(designation_id=des.id)
    var = candidates.objects.filter(
        Q(reference='no reference') | Q(reference='Select HR'))
    return render(request, 'NO_ref.html', {'mem': mem, 'var': var, 'desgn': desgn})


def BY_ref(request):
    mem = User.objects.all()
    des = designation.objects.get(designation='HR')
    desgn = login.objects.filter(designation_id=des.id)
    var = candidates.objects.all().exclude(reference='no reference')
    return render(request, 'BY_ref.html', {'mem': mem, 'var': var, 'desgn': desgn})


def HR(request):
    mem = User.objects.all()
    return render(request, 'HR.html', {'mem': mem})


def HR_view(request):
    mem = User.objects.all()
    des = designation.objects.get(designation='HR')
    m = login.objects.filter(designation_id=des)
    return render(request, 'HR_view.html', {'mem': mem, 'm': m})


def HR_view_update(request, id):
    mem = User.objects.all()
    if request.method == 'POST':
        vars = login.objects.get(id=id)
        vars.fullname = request.POST['hrname']
        vars.email = request.POST['hrmail']
        vars.contact_no = request.POST['hrcontact']
        vars.save()
        return redirect("HR_view")
    return render(request, 'HR_view.html', {'mem': mem})


def HR_add(request):
    mem = User.objects.all()
    des = designation.objects.get(designation='HR')
    m = login.objects.filter(designation_id=des)
    reg = login()
    if request.method == 'POST':
        reg.fullname = request.POST['name']
        reg.email = request.POST['email']
        reg.contact_no = request.POST['number']
        reg.designation_id = des.id
        reg.image = request.FILES['img']
        reg.password = random.randint(10000, 99999)
        reg.save()
        lg = login.objects.get(id=reg.id)
        subject = 'Greetings from iNFOX TECHNOLOGIES'
        message = 'Congratulations,\n' \
            'You have successfully registered with iNFOX TECHNOLOGIES.\n' \
            'following is your login credentials\n'\
            'username :'+str(lg.email)+'\n' 'password :'+str(lg.password) + \
            '\n' 'Login :https://careerinfoxtechnologies.com/'
        recepient = str(reg.email)
        send_mail(subject, message, EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        return redirect('HR_view')
    return render(request, 'HR_add.html', {'mem': mem, 'm': m})


def HR_view_delete(request, id):
    mem = User.objects.all()
    var = login.objects.filter(id=id)
    var.delete()
    return redirect('HR_view')


def hr_dashboard(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        return render(request, 'hr_dashboard.html', {'mem': mem})
    else:
        return redirect('/')


def hr_allMembers(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        return render(request, 'hr_allMembers.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def admin_question_view(request):
    des1 = catagory.objects.get(name='Technical_ability')

    cat = catagory.objects.filter(name=des1.name)
    cat1 = catagory.objects.all().exclude(name='Technical_ability')
    mem = User.objects.all()
    return render(request, 'admin_question_view.html', {'mem': mem, 'cat': cat, 'cat1': cat1})


def admin_question_view_dep(request, id):
    var = catagory.objects.get(id=id)
    print(var.id)
    mem = User.objects.all()
    dep = department.objects.all().exclude(name='Default')
    return render(request, 'admin_question_view_dep.html', {'mem': mem, 'dep': dep, 'var': var, })


def admin_question_category(request):
    mem = User.objects.all()
    return render(request, 'admin_question_category.html', {'mem': mem})


def admin_view_category(request):
    mem = User.objects.all()
    z = catagory.objects.all()
    return render(request, 'admin_view_category.html', {'mem': mem, 'z': z})


def admin_view_update(request, id):
    mem = User.objects.all()
    if request.method == 'POST':
        vars = catagory.objects.get(id=id)
        vars.name = request.POST['namecat']
        vars.no_of_question = request.POST['noqstn']
        vars.time_taken = request.POST['cattime']
        vars.save()
        return redirect("admin_view_category")
    return render(request, 'admin_view_category.html', {'mem': mem})


def admin_view_delete(request, id):
    mem = User.objects.all()
    var = catagory.objects.filter(id=id)
    var.delete()
    return redirect('admin_view_category')


def admin_add_question(request):
    mem = User.objects.all()
    z = catagory()
    if request.method == 'POST':
        z.name = request.POST['namecat']
        z.no_of_question = request.POST['noqstn']
        z.time_taken = request.POST['cattime']
        z.save()

        return redirect('admin_question_category')
    return render(request, 'admin_add_question.html', {'mem': mem})


def admin_allMembers_category(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    return render(request, 'admin_allMembers_category.html', {'mem': mem, 'var': var})


def admin_category_newlist(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(
        reference=var.fullname, contact_status=0).order_by('-id')
    return render(request, 'admin_category_newlist.html', {'m': m, 'mem': mem})


def admin_contactsave(request):
    tid = request.GET.get('tid')
    con = candidates.objects.get(id=tid)
    mem = User.objects.all()
    if request.method == "POST":
        con.contact_status = 1
        con.save()

    msg_success = "contacted"
    return render(request, 'admin_category_newlist.html', {'mem': mem, 'msg_success': msg_success})


def admin_category_contactedlist(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(
        reference=var.fullname, contact_status=1).order_by('-id')
    return render(request, 'admin_category_contactedlist.html', {'mem': mem, 'm': m})

# def admin_contactsave1(request):
#       tid=request.GET.get('tid')
#       con=candidates.objects.get(id=tid)
#       mem = User.objects.all()
#       if request.method=="POST":
#             con.replay_status=1
#             con.contact_status=2
#             con.save()

#       msg_success = "intrested"
#       return render(request, 'admin_category_contactedlist.html',{'mem':mem,'msg_success':msg_success})

# def admin_contactsave2(request):
#       tid=request.GET.get('tid')
#       con=candidates.objects.get(id=tid)
#       mem = User.objects.all()
#       if request.method=="POST":
#             con.replay_status=2
#             con.contact_status=2
#             con.save()

#       msg_warning = "not-intrested"
#       return render(request, 'admin_category_contactedlist.html',{'mem':mem,'msg_warning':msg_warning})


def admin_contactsave1(request):
    tid = request.GET.get('tid')
    con = candidates.objects.get(id=tid)
    mem = User.objects.all()

    con.replay_status = 1
    con.contact_status = 2
    con.save()

    msg_success = "intrested"
    return render(request, 'admin_category_contactedlist.html', {'mem': mem, 'msg_success': msg_success})


def admin_contactsave2(request):
    tid = request.GET.get('tid')
    con = candidates.objects.get(id=tid)
    mem = User.objects.all()

    con.replay_status = 2
    con.contact_status = 2
    con.save()

    msg_warning = "not-intrested"
    return render(request, 'admin_category_contactedlist.html', {'mem': mem, 'msg_warning': msg_warning})


def admin_category_history(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(reference=var.fullname,).exclude(
        replay_status=0).order_by('-id')
    return render(request, 'admin_category_history.html', {'mem': mem, 'm': m})


def admin_category_intrestedlist(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(
        reference=var.fullname, replay_status=1).order_by('-id')
    return render(request, 'admin_category_intrestedlist.html', {'mem': mem, 'm': m})


def admin_category_rejectedlist(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(
        reference=var.fullname, replay_status=2).order_by('-id')
    return render(request, 'admin_category_rejectedlist.html', {'mem': mem, 'm': m})


def admin_department(request):
    mem = User.objects.all()
    return render(request, 'admin_department.html', {'mem': mem})


def admin_add_department(request):
    mem = User.objects.all()
    var = department.objects.all()
    if request.method == 'POST':
        z = department()
        z.name = request.POST['form_select']
        z.description = request.POST['desc']
        z.save()
        return redirect('/admin_department/')
    return render(request, 'admin_add_department.html', {'mem': mem, 'var': var})


def admin_department_view(request):
    var = department.objects.all()
    mem = User.objects.all()

    return render(request, 'admin_department_view.html', {'mem': mem, 'var': var, })


def admin_view_department_delete(request, id):
    var = department.objects.filter(id=id)
    var.delete()
    return redirect('/admin_department_view/')


def admin_view_department_update(request, id):
    mem = User.objects.all()
    z = department.objects.all()
    if request.method == 'POST':
        vars = department.objects.get(id=id)
        vars.name = request.POST['name']
        vars.description = request.POST['desc']
        vars.save()
        return redirect("/admin_department_view/")

    return render(request, 'admin_department_view.html', {'mem': mem, 'z': z})


def admin_category_waiting(request, id):
    var = login.objects.get(id=id)
    mem = User.objects.all()
    m = candidates.objects.filter(
        reference=var.fullname, replay_status=3).order_by('-id')
    return render(request, 'admin_category_waiting.html', {'mem': mem, 'm': m})


# **********************HR Module****************************************************************

def hr_allMembers_category(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        return render(request, 'hr_allMembers_category.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def hr_category_newlist(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1) .filter(
            contact_status=0).order_by('-id')

        return render(request, 'hr_category_newlist.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def contactsave(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        tid = request.GET.get('tid')
        con = candidates.objects.get(id=tid)
        msg_success = "Contacted"
        if request.method == "POST":
            con.contact_status = 1
            con.save()
            # return redirect('/hr_allMembers_category')
        return render(request, 'hr_category_newlist.html', {'m': m, 'mem': mem, 'msg_success':  msg_success})
    else:
        return redirect('/')


def hr_category_contactedlist(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(
            reference=usernamehr1, contact_status=1).order_by('-id')

        return render(request, 'hr_category_contactedlist.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def replaysaveintrest(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        tid = request.GET.get('tid')
        con = candidates.objects.get(id=tid)

        con.replay_status = 1
        con.contact_status = 2
        con.save()
        msg_success = "Intrested"

        # return redirect('/hr_allMembers_category')
        return render(request, 'hr_category_contactedlist.html', {'m': m, 'mem': mem, 'msg_success': msg_success})
    else:
        return redirect('/')


def replaysavenotintrest(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        tid = request.GET.get('tid')
        con = candidates.objects.get(id=tid)

        con.replay_status = 2
        con.contact_status = 2
        con.save()
        msg_successs = "not Intrested"
        # return redirect('/hr_allMembers_category')
        return render(request, 'hr_category_contactedlist.html', {'m': m, 'mem': mem, 'msg_successs': msg_successs})
    else:
        return redirect('/')


def hr_category_intrestedlist(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        # m=candidates.objects.filter(reference=usernamehr1)
        m = candidates.objects.filter(
            reference=usernamehr1, replay_status=1).order_by('-id')
        return render(request, 'hr_category_intrestedlist.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def hr_category_rejectedlist(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        # m=candidates.objects.filter(reference=usernamehr1)
        m = candidates.objects.filter(
            reference=usernamehr1, replay_status=2).order_by('-id')
        return render(request, 'hr_category_rejectedlist.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def hr_category_history(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            return redirect('/')
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1).exclude(
            replay_status=0).order_by('-id')

        return render(request, 'hr_category_history.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def hr_passwordchange(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        if request.session.has_key('usernamehr1'):
            usernamehr2 = request.session['usernamehr2']
        else:
            usernamehr1 = "dummy"
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        if request.method == 'POST':
            abc = login.objects.get(id=usernamehr2)
            oldps = request.POST['currentPassword']
            newps = request.POST['newPassword']
            cmps = request.POST.get('confirmPassword')
            if oldps != newps:
                if newps == cmps:
                    abc.password = request.POST.get('confirmPassword')
                    abc.save()
                    return render(request, 'hr_dashboard.html', {'mem': mem})

            elif oldps == newps:
                messages.add_message(request, messages.INFO,
                                     'Current and New password same')
            else:
                messages.info(request, 'Incorrect password same')

            return render(request, 'hr_passwordchange.html', {'mem': mem})

        return render(request, 'hr_passwordchange.html', {'mem': mem})

    else:
        return redirect('/')


def hr_category_waiting(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            usernamehr1 = "dummy"
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1, replay_status=3)

        return render(request, 'hr_category_waiting.html', {'m': m, 'mem': mem})
    else:
        return redirect('/')


def replaysavewaiting(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        else:
            usernamehr1 = "dummy"
        mem = login.objects.filter(
            designation_id=usernamehr) .filter(fullname=usernamehr1)
        m = candidates.objects.filter(reference=usernamehr1)
        tid = request.GET.get('tid')
        con = candidates.objects.get(id=tid)

        con.replay_status = 3
        con.contact_status = 2
        con.save()
        msg_success = "Waiting"

        # return redirect('/hr_allMembers_category')
        return render(request, 'hr_category_contactedlist.html', {'m': m, 'mem': mem, 'msg_success': msg_success})
    else:
        return redirect('/')


def hr_imagechange(request):
    if 'usernamehr2' in request.session:
        if request.session.has_key('usernamehr'):
            usernamehr = request.session['usernamehr']
        if request.session.has_key('usernamehr1'):
            usernamehr1 = request.session['usernamehr1']
        if request.session.has_key('usernamehr1'):
            usernamehr2 = request.session['usernamehr2']
        else:
            usernamehr1 = "dummy"
        mem = login.objects.filter(
            designation_id=usernamehr).filter(fullname=usernamehr1)
        return render(request, 'hr_imagechange.html', {'mem': mem})
    else:
        return redirect('/')


def imagechange(request, id):
    if request.method == 'POST':

        abc = login.objects.get(id=id)
        abc.image = request.FILES['filename']

        abc.save()
        return redirect('hr_imagechange')
    return render(request, 'hr_imagechange.html')
