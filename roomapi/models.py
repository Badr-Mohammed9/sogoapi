from django.db import models
from django.contrib.auth.models import User
# TOPIC_CHOICES = [
#         ('Cybersecurity', 'Cybersecurity'),
#         ('CloudComputing', 'Cloud Computing'),
#         ('SoftwareDevelopment', 'Software Development'),
#         ('DataManagement', 'Data Management'),
#         ('NetworkAdministration', 'Network Administration'),
#         ('ITCareerAdvice', 'IT Career Advice'),
#         ('EmergingTechnologies', 'Emerging Technologies'),
#     ]
# Create your models here.
class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups',null=True)
    title = models.CharField(default='title', max_length=50)
    participants = models.ManyToManyField(User, related_name='participating_groups',null=True)
    topic = models.CharField(max_length=50,default='Cybersecurity')
    
    def __str__(self):
        return self.title
    
        
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(null=True)
    image = models.ImageField(null=True,blank=True,upload_to='postsImages/')
    
    def __str__(self):
        return self.text
    
    
