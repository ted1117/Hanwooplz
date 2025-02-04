from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
# from tinymce.models import HTMLField

# Create your models here.

class UserProfile(AbstractUser):
    '''
    User model-builtin column with AbstractUser class
    - ID: username
    - PW: password
    - Email: email
    '''
    first_name = None
    last_name = None
    
    # Custom column
    full_name = models.CharField(max_length=6)
    job = models.CharField(max_length=50)
    tech_stack = ArrayField(models.CharField(max_length=20))
    career = models.IntegerField(default=0)
    career_detail = models.TextField() # could be modified
    introduction = models.TextField()
    github_link = models.URLField(blank=True,default='')
    linkedin_link = models.URLField(blank=True,default='')
    user_img = models.ImageField(upload_to="user_img", default=None, null=True)

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='Untitled')
    # content = HTMLField()
    content = models.TextField()

class PostPnP(Post):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tech_stack = ArrayField(models.CharField(max_length=20))
    ext_link = models.URLField()

    class Meta:
        abstract = True

class PostPortfolio(PostPnP):
    portfolio_id = models.AutoField(primary_key=True)
    members = models.IntegerField(default=1)

class PostProject(PostPnP):
    project_id = models.AutoField(primary_key=True)
    status = models.IntegerField(default=1)
    '''
    - 모집중단: 0
    - 모집중: 1
    - 모집완료: 2
    '''
    members = models.ManyToManyField(UserProfile, through='ProjectMembers')
    target_members = models.IntegerField(default=1)

class ProjectMembers(models.Model):
    project = models.ForeignKey(PostProject, on_delete=models.CASCADE)
    members = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class PostQnA(Post):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class PostQuestion(Post):
    question_id = models.AutoField(primary_key=True)
    keyword = ArrayField(models.CharField(max_length=20))
    like = models.ManyToManyField(UserProfile, through="QuestionLike")

class PostAnswer(Post):
    answer_id = models.AutoField(primary_key=True, default=1)
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ManyToManyField(UserProfile, through="AnswerLike")

class QuestionLike(models.Model):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class AnswerLike(models.Model):
    answer = models.ForeignKey(PostAnswer, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="comments_written")
    content = models.TextField()
    like = models.ManyToManyField(UserProfile, through="CommentLike")
    created_at = models.DateTimeField(auto_now_add=True)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class ChatRoom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyer')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessages(models.Model):  
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='receiver')
    message = models.CharField(max_length=500)
    read_or_not = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat_uuid = models.UUIDField(editable=False, unique=True, null=True)

class Notifications(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,related_name='prj_sender')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accept_or_not = models.BooleanField(null=True)
    read_or_not = models.BooleanField(default=False)