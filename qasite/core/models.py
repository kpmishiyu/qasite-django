from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    bounty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    def __str__(self):
        return self.title

# --- 下面是我们要添加的新内容 ---
class Profile(models.Model):
    # 与User模型建立一对一的关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 存储金币，设置默认值为50
    coins = models.IntegerField(default=50)

    def __str__(self):
        return f'{self.user.username} Profile'
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField() # 先用文本作为回答内容
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer by {self.author.username} to "{self.question.title}"'