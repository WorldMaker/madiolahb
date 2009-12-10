# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from django.template import Node, resolve_variable
from google.appengine.ext.webapp import template

register = template.create_template_register()

@register.filter
def escapeyaml(value):
    value = unicode(value)
    return value.replace('"', r'\"')

@register.filter
def maxpoise(value):
    from hce import max_influence
    return max_influence(value, 'poise')

class RollEffectNode(Node):
    def __init__(self, roll):
        self.roll = roll
    def render(self, context):
        from hce import ROLL_EFFECT
        import math
        try:
            roll = int(resolve_variable(self.roll, context))
        except TypeError:
            context['rollcolor'] = context['effectcolor'] = 'black'
            context['timingcolor'] = 'black'
            return ""
        effect, timing = ROLL_EFFECT[roll]
        rollcolor = effectcolor = timingcolor = 'yellow'
        effectlt, timinglt = '', ''
        if effect < 0:
            effectlt = '<'
            rollcolor = effectcolor = 'red'
        elif effect > 0:
            effectlt = '<'
            rollcolor = effectcolor = 'green'
        if timing < 0:
            if timing > -6: timinglt = '<'
            timingcolor = 'red'
        elif timing > 0:
            if timing < 6: timinglt = '<'
            timingcolor = 'green'
        effect, timing = math.abs(effect), math.abs(timing)
        context.update({
            'rollcolor': rollcolor,
            'effect': effect,
            'effectlt': effectlt,
            'effectcolor': effectcolor,
            'timing': timing,
            'timinglt': timinglt,
            'timingcolor': timingcolor,
        })
        return ""

@register.tag
def rolleffect(parser, token):
    try:
        tag_name, roll = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "Rolleffect tag requires an arg"
    return RollEffectNode(roll)

# vim: ai et ts=4 sts=4 sw=4
