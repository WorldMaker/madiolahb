# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.

import re
import sys
sys.path.append('arpeggio.zip')

from arpeggio import *
from arpeggio import RegExMatch

regex = lambda pattern: RegExMatch(re.compile(pattern))

## Atomic bits and pieces ##

imverb = [('is', 'called'), 'continues', 'ends']
dir = ['ne', 'nw', 'se', 'sw', 'n', 's', 'e', 'w']
element = ['life', 'earth', 'water', 'energy', 'air', 'water']
influence = ['mastery', 'persistence', 'design', 'poise', 'sleight', 'charm',
    'mind', 'body', 'spirit']
pronouns = ['i', 'he', 'she', 'it']
pospronouns = ['my', 'his', 'her', 'its']
refpronouns = ['me', 'myself', 'him', 'himself', 'her', 'herself', 'it',
    'itself']

loseverb = regex(r'(loses?|drains?)\s+')
moveverb = regex(r'moves?\s+')
flowverb = regex(r'(flows?|exerts?)\s+')
herorem = regex(r'hero(ic(ally)?)?\s+')
contestverb = regex(r'(challenges?|contests?)\s+')
actverb = regex(r'act(s|ion)?\s+')
setverb = regex('(re)?sets?')
reknownverb = regex(r'(nominates?|props,?)\s+')
voteverb = regex('assents?|aye|dissents?|nay|acclimates?')
chownverb = regex(r'yields?\s+')
timingverb = regex('ready|readies|holds?|interrupts?')
activerem = regex('(in)?active')
reservedverbs = ['is ', 'am ', 'at ', 'to ', 'for ', 'advanced ', 'have ',
    'has ', loseverb, moveverb, flowverb, herorem, contestverb, actverb,
    setverb, reknownverb, voteverb, chownverb, timingverb, activerem, 'in ',
    'with ']

def num():          return regex(r'\d+')
def pronoun():      return pronouns
def pospronoun():   return pospronouns
def refpronoun():   return refpronouns
def imsentence():   return ['this', 'thus'], imverb, regex(r'[^\.]+')

# TODO: Grab a better email/im RegEx
def addr():         return regex(r'[\w0-9\-_\.\+]+\@[\w0-9\-_\.]+')
def notreserved():  return Not(reservedverbs)
def name():         return OneOrMore( (notreserved, regex(r'[^\.\s\,]+')) )
def id():           return [pronoun, addr, name]
def refid():        return [refpronoun, addr, name]
def asphrase():     return [('as', 'for'), 'for', 'as'], [addr, name], ','
def andcomma():     return Optional([(',', 'and'), ',', 'and'])

## Verb Phrases ##

def playing():      return 'playing', name

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

def flowto():       return num, 'to', influence
def flow():         return flowverb, OneOrMore((flowto, andcomma))

def heroic():       return Optional(herorem)
def underprof():    return Optional(('under', [profnum, profcard]))
def contest():      return contestverb, Optional('against'), refid, \
                        heroic, ['with', 'in'], influence, underprof
def act():          return actverb, heroic, ['with', 'in'], influence, \
                        underprof

def set():          return setverb, Optional(refid), \
                        Optional(('to', Optional('time'), num))

def lose():         return loseverb, num, Optional('ego')

def amat():         return 'at', num, Optional(','), num

def move():         return moveverb, Optional(refid), 'to', num, \
                        Optional(regex(r'spots?|s?paces?')), dir

def renown():       return reknownverb, id, 'for', num, influence, \
                        Optional('renown')

def vote():         return voteverb

def chown():        return chownverb, Optional(refid), 'to', [refpronoun, 
                        ('<', addr, '>')]

def timing():       return timingverb

def deactivate():   return activerem

## Final Composition ##

def isphrase():     return Optional(['am', 'is']), [deactivate, amat, playing]
def phrase():       return [advanced, has, flow, contest, act, move,
                        set, lose, renown, vote, chown, timing,
                        isphrase]

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
    def __init__(self, pos=0):
        self.pos = pos

    def first_pass(self, parser, node, nodes):
        return nodes[self.pos]

id.sem = PopNT()
refid.sem = PopNT()
phrase.sem = PopNT()
underprof.sem = PopNT(1)
isphrase.sem = PopNT(-1)

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
            if isinstance(nodes[0], (basestring, Special)):
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

class Stat(SemanticAction):
    def first_pass(self, parser, node, nodes):
        # Return (stat, points)
        stat = nodes[-1 if len(nodes) < 3 else -2].value
        if nodes[-1].value == 'drained':
            stat += '_spot'
        return stat, nodes[0]

stat.sem = Stat()

class FlowTo(SemanticAction):
    def first_pass(self, parser, node, nodes):
        # Return (influence, count)
        return nodes[2].value, nodes[0]

flowto.sem = FlowTo()

class TupleVerb(SemanticAction):
    def __init__(self, name):
        self.name = name

    def first_pass(self, parser, node, nodes):
        stats = [n for n in nodes if isinstance(n, tuple)]
        node.nodes = dict(stats)
        node.nodes['verb'] = self.name
        return node

has.sem = TupleVerb('has')
flow.sem = TupleVerb('flow')
advanced.sem = TupleVerb('advanced')

class Action(SemanticAction):
    def __init__(self, verb):
        self.verb = verb

    def first_pass(self, parser, node, nodes):
        sd = {'verb': self.verb, 'object': None, 'heroic': False,
            'profession': 0}
        for n in nodes:
            if isinstance(n, Special):
                if n.type == 'Heroic':
                    sd['heroic'] = True
                else: # Pronoun, Addr
                    sd['object'] = n
            elif isinstance(n, basestring): # Name
                sd['object'] = n
            elif isinstance(n, int):
                sd['profession'] = n
            elif isinstance(n, Terminal) and n.value in influence:
                sd['influence'] = n.value
        node.nodes = sd
        return node

act.sem = Action('act')
contest.sem = Action('contest')

class Lose(SemanticAction):
    def first_pass(self, parser, node, nodes):
        sd = {'verb': 'lose'}
        if isinstance(nodes[-1], int):
            sd['count'] = nodes[-1]
        else:
            sd['count'] = nodes[-2]
        node.nodes = sd
        return node

lose.sem = Lose()

class AmAt(SemanticAction):
    def first_pass(self, parser, node, nodes):
        sd = {'verb': 'at', 'y': nodes[-1],
            'x': nodes[-3] if isinstance(nodes[-2], Terminal) else nodes[-2],
        }
        node.nodes = sd
        return node

amat.sem = AmAt()

class Move(SemanticAction):
    def first_pass(self, parser, node, nodes):
        poscount, posdir = -2, -1
        if isinstance(nodes[-2], Terminal):
            poscount = -3
        sd = {'verb': 'move',
            'object': None,
            'count': nodes[poscount],
            'dir': nodes[posdir].value,
        }
        if isinstance(nodes[1], (basestring, Special)):
            sd['object'] = nodes[1]
        node.nodes = sd
        return node

move.sem = Move()

class Deactivate(SemanticAction):
    def first_pass(self, parser, node, nodes):
        n = NonTerminal(node.type, node.position, [])
        n.nodes = {
            'verb': 'deactivate' if node.value.startswith('in') else 'activate',
        }
        return n

deactivate.sem = Deactivate()

class Chown(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'verb': 'chown',
            'object': nodes[1] if isinstance(nodes[1], (basestring, Special)) \
                else None,
            'receiver': nodes[-2] if isinstance(nodes[-2], Special) \
                else nodes[-1],
        }
        return node

chown.sem = Chown()

class Renown(SemanticAction):
    def first_pass(self, parser, node, nodes):
        node.nodes = {'verb': 'renown',
            'object': nodes[1],
            'count': nodes[3],
            'influence': nodes[4].value,
        }
        return node

renown.sem = Renown()

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
    try:
        parser.parse(input.lower())
    except NoMatch, e:
        import logging
        logging.error("Expected %s at position %s.", e.value,
            e.parser.pos_to_linecol(e.position))
        raise e
    return parser.getASG()

# For testing...
if __name__ == "__main__":
    import doctest
    print "Running through the corpus..."
    doctest.testfile('corpus.rst', globs={'parse': parse})

# vim: ai et ts=4 sts=4 sw=4
