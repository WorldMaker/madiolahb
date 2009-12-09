# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext.webapp import template

register = template.create_template_register()

@register.filter
def escapeyaml(value):
    value = unicode(value)
    return value.replace('"', r'\"')

# vim: ai et ts=4 sts=4 sw=4
