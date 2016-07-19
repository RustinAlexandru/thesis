# -*- coding: utf-8 -*-

# Scrapy settings for auto project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ninegag'

SPIDER_MODULES = ['ninegag.spiders']
NEWSPIDER_MODULE = 'ninegag.spiders'


import sys
sys.path.append('/Users/alexandrurustin/Desktop/thesis/thesis/thesis')

import os
os.environ["DJANGO_SETTINGS_MODULE"] = 'thesis.settings'

import django
django.setup()

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'auto (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'auto.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'auto.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'scrapy.telnet.TelnetConsole': None,
   # 'scrapy.extensions.closespider.CloseSpider': 0,
}

# CLOSESPIDER_ITEMCOUNT=0

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'auto.pipelines.SomePipeline': 300,
#}
ITEM_PIPELINES = {
    'ninegag.pipelines.ItemUpdatePipeline': 3,
    'ninegag.pipelines.MyFilesPipeline': 2,
}


FEED_EXPORTERS_BASE = {
    'xml': 'scrapy.contrib.exporter.XmlItemExporter',
}

FILES_STORE = '/Users/alexandrurustin/Desktop/thesis/thesis/thesis/funfly/static/funfly/imagesandvideos/imageorvideos'

FILES_URLS_FIELD = 'source_url'
FILES_RESULT_FIELD = 'imagevideo'

IMAGES_URLS_FIELD = 'source_url'
IMAGES_RESULT_FIELD = 'imagevideo'

IMAGES_STORE = '/Users/alexandrurustin/Desktop/thesis/thesis/thesis/funfly/static/funfly/imagesandvideos/imageorvideos'

IMAGES_THUMBS = {
    'big': (100, 100),
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
