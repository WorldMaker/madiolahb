# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from hce import in_prof_range, in_spot_range
from models import Character, SPOTS

# These are command functions for the backend.Commander class

def playing(self, subject=None, name='', **kwargs):
    # Check for an existing character with this name
    exists = Character.all().ancestor(self.game).filter('name =', name) \
        .count(1)
    if exists:
        self.errors.append('Character name exists: %s' % name)
        return False
    owner = self.sender
    if subject is not None:
        if isinstance(subject, basestring):
            self.warnings.append('The subject of "is playing" should be a player.')
        elif subject.type == 'Addr':
            owner = subject.value
    self.char = self.game.new_char(owner, name)
    self.updated.append(self.char)

def advanced(self, subject=None, prof1=None, prof2=None, prof3=None,
    **kwargs):
    if not self._char(subject): return False

    for prof, value in ((self.char.job1, prof1), (self.char.job2, prof2),
        (self.char.job3, prof3)):
        if value is not None:
            if in_prof_range(value):
                prof = value
                if self.char not in self.updated:
                    self.updated.append(self.char)
            else:
                self.warnings.append('%s is out of range for a profession'
                    % value)

def has(self, subject=None, **kwargs):
    if not self._char(subject): return False

    for spot in SPOTS:
        if spot in kwargs:
            if in_spot_range[spot](kwargs[spot]):
                charspot = getattr(self.char, spot)
                charspot = kwargs[spot]
                if self.char not in self.updated:
                    self.updated.append(self.char)
            else:
                self.warnings.append('%s is out of range for %s' % (
                    kwargs[spot], spot))

# vim: ai et ts=4 sts=4 sw=4
