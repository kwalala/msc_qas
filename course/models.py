from django.db import models
from django.contrib.auth.models import User

COURSE_CATEGORY = (
    (1, "Start a New Course"),
    (2, "Run an Existing Course"),
    (3, "Extend an Existing Course"),
)


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
    date_target = models.DateTimeField("Target Finish Date")
    category = models.PositiveIntegerField("Category",
                    choices=COURSE_CATEGORY,
                    default=1)

    def __unicode__(self):
        return "%s" % self.name


class Milestone(models.Model):
    name = models.CharField("Name", max_length=200)
    course = models.ForeignKey(Course)
    approver = models.ForeignKey(User)
    date_target = models.DateTimeField("Target Finish Date")
    completed = models.BooleanField(default=False)
    data_completed = models.DateTimeField("Date Completed")
    approved = models.BooleanField(default=False)
    data_approved = models.DateTimeField("Date Approved")


class Task(models.Model):
    name = models.CharField("Name", max_length=200)
    milestone = models.ForeignKey(Milestone)
    developer = models.ForeignKey(User)
    completed = models.BooleanField(default=False)
    data_completed = models.DateTimeField("Date Completed")
    position = models.IntegerField()


class TaskNotes(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task)
    developer = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
