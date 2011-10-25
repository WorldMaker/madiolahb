# Simple GAE Model JSON Serialization
# Copyright 2009 Max Battcher. Licensed for use under the Ms-PL.
from django.utils import simplejson as json
from google.appengine.ext import db

class GaeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return dict([(name, getattr(obj, name)) for name 
                in obj.properties().keys()])
        return super(self, GaeEncoder).default(obj)

# vim: ai et ts=4 sts=4 sw=4
