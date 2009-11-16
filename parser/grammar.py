# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.

import re
import sys
sys.path.append('arpeggio.zip')

from arpeggio import *
from arpeggio import RegExMatch as rem

## Atomic bits and pieces ##

imverb = [('is', 'called'), 'continues', 'ends']
dir = ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']
element = ['life', 'earth', 'water', 'energy', 'air', 'water']
influence = ['mastery', 'persistence', 'design', 'poise', 'sleight', 'charm',
    'mind', 'body', 'spirit']
pronouns = ['i', 'he', 'she', 'it']
pospronouns = ['my', 'his', 'her', 'its']
refpronouns = ['me', 'myself', 'him', 'himself', 'her', 'herself', 'it',
    'itself']

flowverb = rem(re.compile('flows?|exerts?'))
herorem = rem(re.compile('hero(ically)?'))
contestverb = rem(re.compile('challenges?|contests?'))
actverb = rem(re.compile('act(s|ion)?'))
setverb = rem(re.compile('(re)?set'))
reknownverb = rem(re.compile('nominates?|props,?'))
voteverb = rem(re.compile('assents?|aye|dissents?|nay'))
chownverb = rem(re.compile('yields?'))
timingverb = rem(re.compile('ready|readies|holds?|interrupts?'))
reservedverbs = ['is', 'am', 'at', 'to', 'for', 'advanced', 'have', 'has',
    'lose', 'move', flowverb, herorem, contestverb, actverb, setverb,
    reknownverb, voteverb, chownverb, timingverb, 'inactive']

def num():          return rem(re.compile(r'\d+'))
def pronoun():      return pronouns
def pospronoun():   return pospronouns
def refpronoun():   return refpronouns
def imsentence():   return ['this', 'thus'], imverb, rem(re.compile(r'[^\.]+'))

# TODO: Grab a better email/im RegEx
def addr():         return rem(re.compile(r'[\w0-9\-_\.\+]+\@[\w0-9\-_\.]+'))
def name():         return OneOrMore((Not(reservedverbs),
                        rem(re.compile(r'[^\.\s\,]+'))))
def id():           return [pronoun, addr, name]
def refid():        return [refpronoun, addr, name]
def asphrase():     return [('as', 'for'), 'for', 'as'], [addr, name], ','
def andcomma():     return Optional([(',', 'and'), ',', 'and'])

## Verb Phrases ##

def playing():      return ['am', 'is'], 'playing', name

def profnum():      return 'profession', num
def profcard():     return pospronoun, ['first', 'second', 'third'], \
                        'profession'
def profpt():       return num, Optional(['points', 'tokens']), 'in', \
                        [profnum, profcard]
def advanced():     return Optional(['have', 'has']), 'advanced', \
                        Optional('to'), OneOrMore((profpt, andcomma))

def stat():         return num, [(['ego', 'will'], Optional('drained')),
                        (element, Optional('strength'))]
def has():          return ['have', 'has'], OneOrMore((stat, andcomma))

def flow():         return flowverb, num, 'to', influence

def heroic():       return Optional(herorem)
def underprof():    return Optional(('under', [profnum, profcard]))
def contest():      return heroic, contestverb, refid, ['with', 'in'], \
                        influence, underprof
def act():          return heroic, actverb, ['with', 'in'], influence, \
                        underprof

def set():          return setverb, Optional(refid), \
                        Optional(('to', Optional('time'), num))

def lose():         return 'lose', num, Optional('ego')

def amat():         return Optional(['am', 'is']), 'at', num, Optional(','), \
                        num

def move():         return 'move', Optional(refid), dir, num, \
                        Optional(rem(re.compile('spots?|spaces?')))

def renown():       return reknownverb, id, 'for', num, influence, \
                        Optional('renown')

def vote():         return voteverb

def chown():        return chownverb, 'to', addr

def timing():       return timingverb

def deactivate():   return Optional(['am', 'is']), 'inactive'

## Final Composition ##

def phrase():       return [playing, advanced, has, flow, contest, act, set,
                        lose, amat, move, renown, vote, chown, timing,
                        deactivate]

def asentence():    return Optional(asphrase), Optional(id), phrase
def sentence():     return [imsentence, asentence], '.'
def command():      return OneOrMore(sentence)

## Semantic Actions ##

class Special(object):
    def __init__(self, type='Special', value=''):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return "%s: %s" % (self.type, self.value)
        return self.type

class SpecialSem(SemanticAction):
    def __init__(self, type, value=False):
        self.type = type
        self.value = value

    def first_pass(self, parser, node, nodes):
        if not isinstance(node, NonTerminal) or nodes:
            return Special(self.type, value=node.value if self.value else '')

pronoun.sem = SpecialSem('Pronoun')
pospronoun.sem = SpecialSem('Pronoun')
refpronoun.sem = SpecialSem('Pronoun')
addr.sem = SpecialSem('Addr', value=True)
heroic.sem = SpecialSem('Heroic')

class ToInt(SemanticAction):
    def first_pass(self, parser, node, nodes):
        return int(node.value)

num.sem = ToInt()

class NameConcat(SemanticAction):
    def first_pass(self, parser, node, nodes):
        return ' '.join(n.value for n in nodes)

name.sem = NameConcat()

class PopNT(SemanticAction):
    def first_pass(self, parser, node, nodes):
        return nodes[0]

id.sem = PopNT()
refid.sem = PopNT()
phrase.sem = PopNT()

class AsPhrase(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'as': nodes[-2]}
        return node

asphrase.sem = AsPhrase()

class SetVerb(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'verb': 'set', 'time': None, 'object': None}
        nodes.pop(0) # pop the verb
        if len(nodes) > 0:
            if isinstance(nodes[-1], int):
                node.nodes['time'] = nodes[-1]
            if not (isinstance(nodes[0], Terminal) and nodes[0].value == 'to'):
                node.nodes['object'] = nodes[0]
        return node

set.sem = SetVerb()

class VerbOnly(SemanticAction):
    def first_pass(self, parser, node, nodes):
        n = NonTerminal(node.type, node.position, [])
        n.nodes = {'verb': node.value}
        return n

vote.sem = VerbOnly()
timing.sem = VerbOnly()

class Playing(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'verb': 'playing', 'name': nodes[-1]}
        return node

playing.sem = Playing()

class ProfNum(SemanticAction):
    def first_pass(self, parser, node, nodes):
        return nodes[-1]

profnum.sem = ProfNum()

class ProfCard(SemanticAction):
    def first_pass(self, parser, node, nodes):
        if nodes[-2].value == 'first':
            return 1
        elif nodes[-2].value == 'second':
            return 2
        elif nodes[-2].value == 'third':
            return 3
        return 0

profcard.sem = ProfCard()

class ProfPt(SemanticAction):
    def first_pass(self, parser, node, nodes):
        # Return (prof num, points)
        return nodes[-1], nodes[0]

profpt.sem = ProfPt()

class Advanced(SemanticAction):
    def first_pass(self, parser, node, nodes):
        sd = {'verb': 'advanced', 'profs': []}
        for n in nodes:
            if isinstance(n, tuple):
                sd['profs'].append(n)
        node.nodes = sd
        return node

advanced.sem = Advanced()

class Stat(SemanticAction):
    def first_pass(self, parser, node, nodes):
        # Return (stat, points)
        stat = nodes[-1 if len(nodes) < 3 else -2].value
        if nodes[-1].value == 'drained':
            stat += '_spot'
        return stat, nodes[0]

stat.sem = Stat()

class Has(SemanticAction):
    def first_pass(self, parser, node, nodes):
        stats = [n for n in nodes if isinstance(n, tuple)]
        node.nodes = dict(stats)
        node.nodes['verb'] = 'has'
        return node

has.sem = Has()

class ASentence(SemanticAction):
    def first_pass(self, parser, node, nodes):
        sd = {'nodes': [], 'subject': None}
        for n in nodes:
            if isinstance(n, NonTerminal):
                if isinstance(n.nodes, dict):
                    sd.update(n.nodes)
                else:
                    sd['nodes'].append(n.nodes)
            else:
                # Whatever is left as a Terminal is our subject
                sd['subject'] = n
        node.nodes = sd
        return node

asentence.sem = ASentence()

class IMSentence(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'imsentence': True,
            'verb': nodes[1].value, 
            'name': nodes[-1].value,
        }
        return node

imsentence.sem = IMSentence()

class CleanSentences(SemanticAction):
    def first_pass(self, parser, node, nodes):
        sentences = []
        for n in nodes:
            sd = {'imsentence': False}
            if isinstance(n.nodes[0].nodes, dict):
                sd.update(n.nodes[0].nodes)
            else:
                sd['nodes'] = n.nodes[0].nodes
            sentences.append(sd)
        return sentences

command.sem = CleanSentences()

# Convenience Function
def parse(input):
    parser = ParserPython(command)
    parser.parse(input.lower())
    return parser.getASG()

# For testing...
if __name__ == "__main__":
    import doctest
    print "Running through the corpus..."
    doctest.testfile('corpus.rst', globs={'parse': parse})

# vim: ai et ts=4 sts=4 sw=4
