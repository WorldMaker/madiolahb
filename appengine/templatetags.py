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
        try:
            roll = int(resolve_variable(self.roll, context))
        except TypeError:
            context['rollcolor'] = context['effectcolor'] = 'black'
            context['timingcolor'] = 'black'
            return ""
        effect, timing = ROLL_EFFECT[roll]
        rollcolor = effectcolor = timingcolor = '#b4b400'
        effectlt, timinglt = '', ''
        if effect < 0:
            effectlt = '<'
            rollcolor = effectcolor = '#b40000'
        elif effect > 0:
            effectlt = '<'
            rollcolor = effectcolor = '#00b400'
        if timing < 0:
            if timing > -6: timinglt = '<'
            timingcolor = '#b40000'
        elif timing > 0:
            if timing < 6: timinglt = '<'
            timingcolor = '#00b400'
        effect, timing = abs(effect), abs(timing)
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
