# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import codecs
import os
from django.forms import model_to_dict
from scrapy.pipelines.files import FilesPipeline


class MyFilesPipeline(FilesPipeline):

    # def process_item(self, item, spider):
    #     if spider.name not in ['9gagspy']:
    #         return item
    #     else:
    #         return item

    def item_completed(self, results, item, info):
       try:
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise  IndexError
        item['imagevideo_path'] = 'funfly/images/imageorvideos/'+\
                                 image_paths[0]
       except IndexError:
           return item
       return item


def get_model(item):
    class_model = getattr(item, 'django_model')
    if not class_model:
        raise TypeError("No Django Item type found!")

    return item.instance

def get_or_create(model):
    class_model = type(model)
    created = False

    try:
        obj = class_model.unmoderated_objects.get(title=model.title)
    except class_model.DoesNotExist:
        created = True
        obj = model
    except AttributeError:
        try:
            obj = class_model.unmoderated_objects.get(identifier=model.identifier)
        except class_model.DoesNotExist:
            created = True
            obj = model

    return (obj, created)

def update_model(destination, source, commit=True):
    pk = destination.pk

    source_dict = model_to_dict(source)
    for (key, value) in source_dict.items():
        setattr(destination, key, value)

    setattr(destination, 'pk', pk)

    if commit:
        destination.save()

class ItemUpdatePipeline(object):

    def process_item(self, item, spider):
        try:
            item_model = get_model(item)
        except TypeError:
            return item

        model, created = get_or_create(item_model)

        update_model(model, item_model)

        return item


class JsonEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.json', 'w+', encoding='utf-8')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False,  indent=4) + ',' + '\n'
        self.file.write(line)
        # item.save()
        return item

    def close_spider(self, spider):
        self.file.seek(-2, os.SEEK_END)
        self.file.write(']')
        self.file.close()
