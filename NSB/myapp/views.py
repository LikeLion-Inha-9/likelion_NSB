from django.shortcuts import render,redirect,get_object_or_404
from .models import *
# views.py

def home(req):
    user=User.objects.all()
    ideas=Idea_upload.objects.all()
    return render(req, 'home.html',{'data':ideas})

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
            return redirect('/idea/'+str(idea.id))
    return render(req,'Idea_upload/idea_create.html')

def idea_read(req, id):
    idea = get_object_or_404(Idea_upload, pk=id)
    comments = idea.comment.all()
    user_pk = req.session.get('user')
    current_user = User.objects.get(pk=user_pk)
    context = {
        'data' : idea,
        'comments' : comments,
        'current_user' : current_user
    }
    return render(req,'Idea_upload/idea_read.html', context)

def idea_comment_create(req, id):
    user_pk = req.session.get('user')
    if not user_pk:
        return redirect('/login')
    elif user_pk:
        if req.method == 'POST':
            idea = get_object_or_404(Idea_upload, pk = id)
            user = User.objects.get(pk=user_pk)
            idea.comment.create(content = req.POST['comment'], writer=user)
        
            return redirect('/idea/'+str(id))
    return render(req,'Idea_upload/idea_read.html')

def idea_update(req, id): 
    idea = get_object_or_404(Idea_upload, pk = id)
    if req.method == "POST":
        idea.category = req.POST['category']
        idea.title = req.POST['title']
        idea.content = req.POST['content']

        idea.save()
        return redirect('/idea/'+str(id))
    return render(req,'Idea_upload/idea_update.html',{'data' : idea}) 


def idea_delete(req, id):
    idea = get_object_or_404(Idea_upload, pk = id)
    idea.delete()
    return redirect('/')

def idea_comment_update(req, id):
    comment = get_object_or_404(Idea_evalu_comment, pk = id)
    if req.method == "POST":
        comment.content = req.POST['content']
        
        comment.save()
        return redirect('/idea/'+str(comment.idea_upload_id.id))
    return render(req,'Idea_upload/idea_comment_update.html',{'comment' : comment}) 

def idea_comment_delete(req, id):
    comment = get_object_or_404(Idea_evalu_comment, pk = id)
    idea = comment.idea_upload_id.id
    comment.delete()
    return redirect('/idea/'+str(idea))