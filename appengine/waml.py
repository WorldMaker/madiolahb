# Simple, stupid Wave Annotation Markup
# Copyright 2010 Max Battcher. Licensed for use under the Ms-PL.
from google.appengine.ext.webapp import template
from waveapi import element
import yaml

def append_waml(blip, filename, context={}):
    """
    Applies to the doc, which is expected to be a Wave API Document, the
    transforms specified in an appropriate data structure loaded from a
    YAML document that is rendered by a Django Template of the given
    filename and with the given context.
    """
    tmpl = yaml.load(template.render(filename, context))
    annots = []
    start, end = 0, 0

    for tok in tmpl:
        if isinstance(tok, list):
            if isinstance(tok[1], dict):
                start = len(blip)
                blip.append(unicode(tok[0]))
                end = len(blip)
                annots.append((start, end, tok[1].items()))
            else:
                blip.append(unicode(tok[0]))
        elif isinstance(tok, dict):
            type = tok.pop('type').lower()
            if type == 'image':
                blip.append(element.Image(**tok))
            elif type == 'gadget':
                blip.append(element.Gadget(tok.pop('url'), tok))
            else:
                pass # TODO: Support other element types
        else:
            tok = unicode(tok)
            blip.append(tok)

    # We add annotations after the fact because Wave's API continues
    # annotations on append. Otherwise, we'd use bundled_annotations
    for start, end, annotations in annots:
        # This should work according to the documentation, but the
        # API doesn't actually support it yet:
        #
        # blip.range(start, end).annotate(annotations)

        segment = blip.range(start, end)
        for ann in annotations:
           segment.annotate(ann[0], ann[1])

def plaintext(filename, context={}):
    """
    Takes a Django-templated YAML file at filename and returns a
    plaintext expansion with the given context.
    """
    tmpl = yaml.load(template.render(filename, context))

    def txt(tok):
        if isinstance(tok, list):
            if len(tok) > 1 and isinstance(tok[1], dict):
                if "link/manual" in tok[1]: # Specially extract hyperlinks
                    return u"%s <%s>" % (unicode(tok[0]), tok[1]["link/manual"])
            return unicode(tok[0])
        elif isinstance(tok, dict):
            return ''
        else:
            return unicode(tok)

    return u''.join(txt(tok) for tok in tmpl)

# vim: ai et ts=4 sts=4 sw=4
