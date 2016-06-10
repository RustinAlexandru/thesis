from __future__ import absolute_import

from datetime import timedelta

from celery import task
from celery.task import periodic_task

from ninegag.spiders.spider import run_spider
from youtube_parsing import youtube_search


# from spider import run_spider
# from ninegag.spiders.spider import run_spider

@task
def spider():
    run_spider()


@task
# run_every=crontab(hour=22, minute=50)
@periodic_task(run_every=timedelta(seconds=30))
def youtube_task():
    youtube_search('funny')

