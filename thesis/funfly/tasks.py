from __future__ import absolute_import

import sys
from datetime import timedelta

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from youtube_parsing import youtube_search

sys.path.append('/Users/alexandrurustin/Desktop/thesis/thesis/ninegag')
from ninegag.spiders.spider import run_9gag_spider, run_jokes_spider, run_jokescc_spider



@task
@periodic_task(run_every=crontab(minute=0, hour=0))
def spider_9gag():
    run_9gag_spider()

@task
@periodic_task(run_every=crontab(minute=0, hour=0))
def spider_jokes():
    run_jokes_spider()

@task
@periodic_task(run_every=crontab(minute=0, hour=0))
def spider_jokescc():
    run_jokescc_spider()


@task
@periodic_task(run_every=crontab(minute=0, hour=0))
def youtube_task():
    youtube_search('funny')

