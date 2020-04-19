from django.db import models
from users.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=70, null=False, blank=False)
    details = models.TextField(max_length=500, null=False, blank=False)
    total_target = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    creator_id = models.ForeignKey("users.User", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100)

class Project_Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=20)
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)

class Project_Pictures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to='images/projects/')
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)

class Project_Ratings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)

class User_Donations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(null=False, blank=False, max_digits=9, decimal_places=2)
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)

class Project_Reports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.TextField(max_length=500, null=False, blank=False)
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment_Reports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report = models.TextField(max_length=500, null=False, blank=False)
    comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)

class Project_Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(max_length=500, null=False, blank=False)
    comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)
    user_id = models.ForeignKey("users.User", on_delete=models.CASCADE)
    project_id = models.ForeignKey("Project", on_delete=models.CASCADE)