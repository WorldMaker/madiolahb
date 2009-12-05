# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from parser import Special

def chown(self, subject=None, object=None, receiver=None, **kwargs):
    owner = self.sender
    if isinstance(subject, Special) and subject.type == 'Addr':
        owner = subject.value
    else:
        self.errors.append('Expected an address or pronoun for the subject')
        return

    object = self._object(object)
    if object is None: return

    if object.owner != owner:
        self.errors.append('%s is not the owner of %s' % (
            owner, object.name))
        return

    if isinstance(receiver, Special) and receiver.type == 'Pronoun':
        receiver = self.sender

    object.owner = receiver
    if object.key() not in self.updated:
        self.updated.append(object.key())

def activate(self, subject=None, **kwargs):
    if not self._char(subject): return False

    self.char.active = True
    self._activechars.append(self.char)
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

def deactivate(self, subject=None, **kwargs):
    if not self._char(subject): return False

    self.char.active = False
    if self.char in self._activechars:
        self._activechars.remove(self.char)
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

# vim: ai et ts=4 sts=4 sw=4
