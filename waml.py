# Simple, stupid Wave Annotation Markup
# Copyright 2009 Max Battcher. Licensed for use under the Ms-PL.
from google.appengine.ext.webapp import template
from waveapi.document import FormElement, Gadget, Image, Range
import yaml

def append_waml(doc, filename, context={}):
    """
    Applies to the doc, which is expected to be a Wave API Document, the
    transforms specified in an appropriate data structure loaded from a
    YAML document that is rendered by a Django Template of the given
    filename and with the given context.
    """
    tmpl = yaml.load(template.render(filename, context))

    pos = len(doc.GetText()) + 1 # Why are ranges 1-based?
    annots = []

    for tok in tmpl:
        if isinstance(tok, list):
            doc.AppendText(tok[0])
            end = pos + len(tok[0])
            if isinstance(tok[1], dict):
                for key, value in tok[1].items():
                    annots.append((Range(pos, end), key, value))
            pos = end
        elif isinstance(tok, dict):
            type = tok.pop('type').lower()
            if type == 'image':
                doc.AppendElement(Image(**tok))
            elif type == 'gadget':
                doc.AppendElement(Gadget(**tok))
            elif type == 'formelement':
                etype = tok.pop('element_type')
                name = tok.pop('name')
                doc.AppendElement(FormElement(etype, name, **tok))
            pos += 1 # These elements take up a position?
        else:
            tok = str(tok)
            doc.AppendText(tok)
            pos += len(tok)
        space = True
    # We collect, then apply all of the annotations at the end here
    # because AppendText apparently automagically adjusts the end of
    # ranges that coincide with the end of the current document, thus
    # producing "leaky" annotations
    for annot in annots:
        doc.SetAnnotation(*annot)

# vim: ai et ts=4 sts=4 sw=4
