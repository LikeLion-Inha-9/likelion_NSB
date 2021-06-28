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
    return render(req, 'home.html',{'data':user})

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
            service.evalu1 = int(req.POST['evalu1'])
            service.evalu2 = int(req.POST['evalu2'])
            service.evalu3 = int(req.POST['evalu3'])
            #user의 foreign key이기 때문에 무조건 이렇게 가져와야함
            user = User.objects.get(pk=user_pk) #세션에서 값을 가져와 현재 사용자를 알아냄
            service.user_id = user
            service.save()
            return redirect('/service/'+str(service.s_id))
    return render(req,'Service_upload/service_create.html')

def service_read(req,s_id):
    service = get_object_or_404(Service_upload,pk=s_id)
    context = {
        'data' : service,
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
            s_evalu.title = req.POST['title']
            s_evalu.content = req.POST['content']
            s_evalu.grade1 = float(req.POST['grade1'])
            s_evalu.grade2 = float(req.POST['grade2'])
            s_evalu.grade3 = float(req.POST['grade3'])
            # user, service_upload의 foreign key이기때문에 둘다 무조건 이렇게 가져와야함
            user = User.objects.get(pk=user_pk)
            service = Service_upload.objects.get(pk=s_id)
            s_evalu.service_upload_id = service
            s_evalu.user_id = user
            s_evalu.save()
            return redirect('/service/'+str(s_id)+'/evalu/'+str(s_evalu.e_id))
    return render(req,'Service_evaluation/s_evalu_create.html')
    
def s_evalu_read(req,s_id,e_id):
    s_evalu = get_object_or_404(Service_evalu_upload,pk=e_id)
    comments = s_evalu.comment.all()
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
            s_evalu.comment.create(content = req.POST['comment'],user_id=user,
            service_evalu_upload_id=evalu,service_upload_id = service)
            return redirect('/service/'+str(s_id[0])+'/evalu/'+str(s_evalu.e_id))
    return render(req,'Service_evaluations/s_evalu_read.html')
            user = User.objects.get(pk=user_pk)
            service.user_id = user
            service.save()
            return redirect('/service/'+str(service.id))
            #return redirect('/')
    return render(req,'Service_upload/service_create.html')

def service_read(req,id):
    service = get_object_or_404(Service_upload,pk=id)
    context = {
        'data' : service
    }
    return render(req,'Service_upload/service_read.html',context)
