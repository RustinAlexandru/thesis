from __future__ import absolute_import

import sys
from datetime import timedelta

from celery import task
from celery.task import periodic_task

from youtube_parsing import youtube_search

sys.path.append('/Users/alexandrurustin/Desktop/thesis/thesis/ninegag')
from ninegag.spiders.spider import run_9gag_spider, run_jokes_spider



@task
def spider_9gag():
    run_9gag_spider()


@task
def spider_jokes():
    run_jokes_spider()


@task
# run_every=crontab(hour=22, minute=50)
@periodic_task(run_every=timedelta(seconds=30))
def youtube_task():
    youtube_search('funny')
