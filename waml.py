# Simple, stupid Wave Annotation Markup
# Copyright 2009 Max Battcher. Licensed for use under the Ms-PL.
from google.appengine.ext.webapp import template
from waveapi.document import Range
import yaml

def append_waml(doc, filename, context={}):
    tmpl = yaml.load(template.render(filename, context))

    pos = len(doc.GetText())

    for tok in tmpl:
        if isinstance(tok, list):
            doc.AppendText(tok[0])
            end = pos + len(tok[0])
            for key, value in tok[1]:
                doc.SetAnnotation(Range(pos, end), key, value)
            pos = end
        # TODO: Element insertion
        elif isinstance(tok, basestring):
            doc.AppendText(tok)
            pos += len(tok)
        space = True

#vim: ai et ts=4 sts=4 sw=4