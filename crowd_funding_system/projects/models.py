from django.db import models
from users.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Avg, Sum
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=70, null=False, blank=False)
    details = models.TextField(max_length=500, null=False, blank=False)
    total_target = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey("users.User", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    
    @property
    def average_rating(self):
        rating = Project_Ratings.objects.filter(project_id = self.id).aggregate(Avg('rating'))
        return rating['rating__avg']
    
    @property
    def images(self):
        return Project_Pictures.objects.filter(project_id = self.id)
        
    def get_donations_of_project(self):
        total_donations = self.user_donations_set.aggregate(Sum('amount'))
        return total_donations["amount__sum"]


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name

class Project_Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=20)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

class Project_Pictures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to='images/projects/')
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

class Project_Ratings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

class User_Donations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Project_Reports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.TextField(max_length=500, null=False, blank=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def report_id(self):
        return self.id

    def project_actions(self):
        url = reverse('project_details', args=(self.project.id,))
        return format_html("<a class='button' href='%s'>View</a> <a class='button' href='%s'>Delete</a>" % (url , (url+"/delete")))
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment_Reports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.TextField(max_length=500, null=False, blank=False)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

class Project_Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)