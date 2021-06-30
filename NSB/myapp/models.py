from enum import unique
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField


# Create your models here.

class User(models.Model):
    # pk : django 자동으로 제공하는 id 값으로 할거임
    email = models.EmailField(max_length=128)
    name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=20)
    point = models.IntegerField(default=0)
    level = models.CharField(max_length=10,default=0)
    password = models.CharField(max_length=30,null=True)

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Service_upload (TimeStampModel):
    # pk : 자동으로 증가하는 id는 django 자체적으로 존재 고로 생략
    Evaluation_Standard=(    #평가 기준 논의해야함 일단 1. 상업성 2. 공익성 3. 독창성 이렇게 정의해놓음
        (1,'commercial'),
        (2,'public interest'),
        (3,'creativity')
    )

    def number():
        no = Service_upload.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    s_id = models.IntegerField(primary_key=True,unique= True,default=number)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
    service = models.TextField() # 이거 조금 고민대상!! (service를 프로그램 자체에 저장해두고 불러올지 불러오면 여기에 링크 저장해야할듯)
    evalu1 = models.IntegerField(choices=Evaluation_Standard)
    evalu2 = models.IntegerField(choices=Evaluation_Standard)
    evalu3 = models.IntegerField(choices=Evaluation_Standard)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자") # 식별관계임! user가 있어야지만 해당 service가 존재할 수 있다
    #user_id = models.IntegerField(primary_key=True,unique=True) # 식별관계임! user가 있어야지만 해당 service가 존재할 수 있다
    
    # date값을 TimeStampModel을 상속하므로 해결

class Idea_upload(TimeStampModel):
    category = models.CharField(max_length=20, blank=False, null=False)
    title = models.CharField(max_length=20, blank=False, null=False)
    content = models.TextField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자")

class Idea_evalu_comment(TimeStampModel):
    content = models.TextField()
    idea_upload_id = models.ForeignKey(Idea_upload, on_delete=models.CASCADE, related_name="comment", verbose_name="원글")
    writer = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="작성자", null=True) #댓글의 작성자.
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자") # 비식별관계
    
    # date값을 TimeStampModel을 상속하므로 해결

class Service_evalu_upload(TimeStampModel):
    # pk : 자동으로 증가하는 id는 django 자체적으로 존재 고로 생략
    def number():
        no = Service_evalu_upload.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    e_id = models.IntegerField(primary_key=True,unique= True,default=number)
    title = CharField(max_length=50)
    content = TextField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자")
    grade1 = models.FloatField(default=0.0)
    grade2 = models.FloatField(default=0.0)
    grade3 = models.FloatField(default=0.0)
    service_upload_id = models.ForeignKey(Service_upload,on_delete=models.CASCADE)

class Service_evalu_comment(TimeStampModel):
    # pk : 자동으로 증가하는 id는 django 자체적으로 존재 고로 생략
    def number():
        no = Service_evalu_comment.objects.count()
        if no == None:
            return 1
        else:
            return no + 1
    c_id = models.IntegerField(primary_key=True,unique= True,default=number)
    content = TextField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자")
    service_evalu_upload_id = models.ForeignKey(Service_evalu_upload,on_delete=models.CASCADE,verbose_name="Service_upload",related_name="comment")
    service_upload_id = models.ForeignKey(Service_upload,on_delete=models.CASCADE,verbose_name="Service")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="작성자",primary_key=True) # 식별관계임! user가 있어야지만 해당 service가 존재할 수 있다
    #user_id = models.IntegerField(primary_key=True,unique=True) # 식별관계임! user가 있어야지만 해당 service가 존재할 수 있다
    
    # date값을 TimeStampModel을 상속하므로 해결
