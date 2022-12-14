import datetime
from msilib.schema import AdminExecuteSequence
from time import timezone
from django.db import models
from django.contrib import admin

class Thread(models.Model):
    thread_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
    latest_date = models.DateTimeField('date published')

    def __str__(self):
        return self.thread_text

    def print_pub_date(self):
        return (self.pub_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')#wrong


    def update_date(self):
        self.latest_date = datetime.timezone.now()

    def print_latest_date(self):
        return (self.latest_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')#wrong

    def print_count_response(self):
        return self.response_set.count()

    def print_title(self):
        if(len(self.thread_text) > 16):
            return self.thread_text[0:16]+'...'
        else:
            return self.thread_text

    @ admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = datetime.timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=255)
    name_text = models.CharField(max_length=255)
    tweet_date = models.DateTimeField('date published')

    def __str__(self):
        return self.response_text

    def print_tweet_date(self):
        return (self.tweet_date+datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')#wrong
