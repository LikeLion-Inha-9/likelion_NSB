from django.shortcuts import render,redirect,get_object_or_404
from .models import *
import re
# views.py

#create하는 경우는 post하는 경우고 read하는 경우는 get하는 경우임 (물론 중간에 form action의 값을 통해서 get과 post 둘 다 가능)
# post의 특성상 data를 받아오는거지 줄수 없는 것임!!! {url ~~ data.id}이런식으로 url에게 값을 줄 수 없음
# get은 data를 줄 수 있음 get 페이지에서 값을 줘서 새로운 것을 생성하기 위해서는 그 연결을 위해서 data를 줘야함

# views.py


def home(req):
    user=User.objects.all()
    services=Service_upload.objects.all()
    ideas=Idea_upload.objects.all()
    user_pk = req.session.get('user')
    context = {
        'services' : services,
        'ideas' : ideas,
        'user_pk' : user_pk,
    }
    return render(req, 'home.html',context)

def check_password(checkpw,originalpw):
    if checkpw==originalpw:
        return True
    else:
        return False

def login(req):
    if req.method=="GET":
        return render(req,'login.html')
    elif req.method=="POST":
        user_id = req.POST.get('user_id')
        user_pw = req.POST.get('user_pw')

        res_data={}
        if not (user_id and user_pw):
            res_data['error']="모든 칸을 다 입력해주세요"

        else:
            #기존(DB)에 있는 Fuser 모델과 같은 값인 걸 가져온다.
            user = User.objects.get(email=user_id) #(필드명=값)

            #비밀번호가 맞는지 확인한다.
            if check_password(user_pw,user.password):
                #응답 데이터 세션에 값 추가. 수신측 쿠키에 저징됨
                req.session['user'] = user.id 
                return redirect('/')
            else:
                res_data['error'] = "비밀번호가 틀렸습니다."
        return render(req,'login.html',res_data) #응답 데이터 res_data 전달

                                                                                # 기본구현
######################################################################################
                                                                                # user

def user_create(req):
    if req.method == 'POST':
        user = User()
        user.email = req.POST['email']
        user.name = req.POST['name']
        user.nickname = req.POST['nickname']
        user.point = int(req.POST['point'])  
        user.level = int(req.POST['level'])
        user.password = req.POST['password']
        user.save()
        return redirect('/user/'+str(user.id))
    return render(req,'User/user_create.html')

def user_read(req,id):
    service = get_object_or_404(User,pk=id)
    context = {
        'data' : service
    }
    return render(req,'User/user_read.html',context)

                                                                                # user
###########################################################################################
                                                                                # service
def service_create(req):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            service = Service_upload()
            service.category = req.POST['category']
            service.title = req.POST['title']
            service.content = req.POST['content']
            service.service = req.POST['service']
            list=req.POST.getlist("evalu[]")
            service.evalu1 = int(list[0])
            service.evalu2 = int(list[1])
            service.evalu3 = int(list[2])
            #user의 foreign key이기 때문에 무조건 이렇게 가져와야함
            user = User.objects.get(pk=user_pk) #세션에서 값을 가져와 현재 사용자를 알아냄
            service.user_id = user
            service.save()
            return redirect('/service/'+str(service.s_id))
    return render(req,'Service_upload/service_create.html')

def service_read(req,id):
    service = get_object_or_404(Service_upload,pk=id)
    user_pk = req.session.get('user')
    tester=Service_evalu_upload.objects.filter(user_id=user_pk, service_upload_id=id)  
    context = {
        'data' : service,
        'tester' : tester,
    }
    return render(req,'Service_upload/service_read.html',context)
                                                                                #service
###########################################################################################
                                                                                # evaluation
def s_evalu_create(req,s_id): 
    #service의 id를 받아와야함 -> service_read에서 id를 받아와야함 그래서 service_read.html에 보면 url 연결해주면서 data.id로 id를 전달받는다
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            s_evalu = Service_evalu_upload()
            s_evalu.content = req.POST['content']
            s_evalu.grade1 = float(req.POST['rating'])
            s_evalu.grade2 = float(req.POST['rating2'])
            s_evalu.grade3 = float(req.POST['rating3'])
            # user, service_upload의 foreign key이기때문에 둘다 무조건 이렇게 가져와야함
            user = User.objects.get(pk=user_pk)
            service = Service_upload.objects.get(pk=s_id)
            s_evalu.service_upload_id = service
            s_evalu.user_id = user
            s_evalu.save()
            return service_read(req,s_id)
    
def s_evalu_read(req,s_id,e_id):
    s_evalu = get_object_or_404(Service_evalu_upload,pk=e_id)
    comments = s_evalu.s_evalu_comment.all()
    context = {
        'data' : s_evalu,
        'comments':comments,
    }
    return render(req,'Service_evaluation/s_evalu_read.html',context)


def s_evalu_comment_create(req,service_upload_id,e_id):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            s_evalu = get_object_or_404(Service_evalu_upload,pk=e_id)
            user = User.objects.get(pk=user_pk)
            evalu = Service_evalu_upload.objects.get(pk=e_id)
            s_id = re.findall("\d",service_upload_id)
            service = Service_upload.objects.get(pk=s_id[0])
            s_evalu.s_evalu_comment.create(content = req.POST['comment'],user_id=user,
            service_evalu_upload_id=evalu,service_upload_id = service)
            return redirect('/service/'+str(s_id[0])+'/evalu/'+str(s_evalu.e_id))
    return render(req,'Service_evaluations/s_evalu_read.html')

def idea_create(req):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            idea = Idea_upload()
            idea.category = req.POST['category']
            idea.title = req.POST['title']
            idea.content = req.POST['content']
            user = User.objects.get(pk=user_pk)
            idea.user_id = user
            idea.save()
            return redirect('/idea/'+str(idea.i_id))
    return render(req,'Idea_upload/idea_create.html')

def idea_read(req, i_id):
    idea = get_object_or_404(Idea_upload, pk=i_id)
    comments = idea.comment.all()
    user_pk = req.session.get('user')
    current_user = User.objects.get(pk=user_pk)
    context = {
        'data' : idea,
        'comments' : comments,
        'current_user' : current_user.id,
    }
    return render(req,'Idea_upload/idea_read.html', context)

def idea_comment_create(req, i_id):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            idea = get_object_or_404(Idea_upload, pk = i_id)
            user = User.objects.get(pk=user_pk)
            idea.comment.create(content = req.POST['comment'],user_id=user,idea_upload_id = idea)
            return redirect('/idea/'+str(i_id))
    return render(req,'Idea_upload/idea_read.html')

def idea_update(req, i_id): 
    idea = get_object_or_404(Idea_upload, pk = i_id)
    if req.method == "POST":
        idea.category = req.POST['category']
        idea.title = req.POST['title']
        idea.content = req.POST['content']
        idea.save()
        return redirect('/idea/'+str(i_id))
    return render(req,'Idea_upload/idea_update.html',{'data' : idea}) 


def idea_delete(req, i_id):
    idea = get_object_or_404(Idea_upload, pk = i_id)
    idea.delete()
    return redirect('/')

def idea_comment_update(req,  idea_upload_id,c_id):
    comment = get_object_or_404(Idea_evalu_comment, pk = c_id)
    if req.method == "POST":
        comment.content = req.POST['content']
        comment.save()
        return redirect('/idea/'+str(idea_upload_id))
    return render(req,'Idea_upload/idea_comment_update.html',{'comment' : comment}) 

def idea_comment_delete(req, idea_upload_id,c_id):
    comment = get_object_or_404(Idea_evalu_comment, pk = c_id)
    comment.delete()
    return redirect('/idea/'+str(idea_upload_id))

def mypage_read(req):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        current_user = User.objects.get(pk=user_pk)
        services = Service_upload.objects.filter(user_id=user_pk)
        services_test = Service_evalu_upload.objects.filter(user_id=user_pk)
           
        context = {
            'current_user' : current_user,
            'services' : services,
            'services_test' : services_test,
        }
        return render(req,'mypage.html', context)
