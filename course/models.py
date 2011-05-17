from django.db import models
from django.contrib.auth.models import User

from msc_qas.course.defaults import COURSE_CATEGORY


class Course(models.Model):
    name = models.CharField("Name", max_length=200)
    duration = models.PositiveIntegerField("Duration", default=1)
    description = models.TextField("Description")
    admin = models.ForeignKey(User, 
                    related_name="course_administered",
                    verbose_name="Administrator")
    leader = models.ForeignKey(User, 
                    related_name="course_led",
                    verbose_name="Leader")
    developers = models.ManyToManyField(User,
                    related_name="course_developed",
                    verbose_name="Developers",
                    null=True, blank=True)
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_target = models.DateField(verbose_name="Target Finish Date")
    category = models.PositiveIntegerField("Category",
                    choices=COURSE_CATEGORY,
                    default=1)
    activated = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.name


class Milestone(models.Model):
    name = models.CharField("Name", max_length=200)
    course = models.ForeignKey(Course)
    approver = models.ForeignKey(User)
    date_target = models.DateField("Target Finish Date")
    completed = models.BooleanField(default=False)
    data_completed = models.DateTimeField("Date Completed", blank=True, null=True)
    approved = models.BooleanField(default=False)
    data_approved = models.DateTimeField("Date Approved", blank=True, null=True)
    
    def all_tasks_completed(self):
        return not self.task_set.filter(completed=False).exists()
        
    def has_tasks(self):
        return self.task_set.exists()


class Task(models.Model):
    name = models.CharField("Name", max_length=200)
    milestone = models.ForeignKey(Milestone)
    developer = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    data_completed = models.DateTimeField("Date Completed", blank=True, null=True)
    #position = models.IntegerField()


class TaskNotes(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task)
    developer = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
