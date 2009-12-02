# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from hce import tick, TIME_READY
from models import Character

def _tick(self):
    if self.game.hold:
        self.game.hold = []
        if self.game not in self.updated:
            self.updated.append(self.game)
    chars = Character.all().ancestor(self.game).filter('active =', True)
    ready = []
    while not ready:
        for char in chars:
            char.time = tick(char.time)
            if char.time == 0 and not char.waiting:
                # The char is no longer waiting for anyone else to 0/ready
                char.time = 1
            if char.time == TIME_READY:
                ready.append(char.name)
                # TODO: Flow exerted influence will
    for char in chars:
        # Remove newly readied characters from a char's waiting list
        # ASSERT: It shouldn't be possible for multiple timesteps to occur?
        if char.time == 0:
            for c in ready:
                if c.name in char.waiting: char.waiting.remove(c.name)
        # Update the commit list
        if char not in self.updated:
            self.updated.append(char)

def timing(self, subject=None, value=None, **kwargs):
    if value is None: return
    if not self._char(subject): return False

    if self.game.active:
        self.errors.append('%s is currently active' % self.game.active)
        return False

    if value.startswith('read'):
        # Ready
        chars = Character.all().ancestor(self.game).filter('active =', True) \
            .filter('time =', TIME_READY) # TODO: Perhaps this query should be
                                          # denormalized?
        maxpoise = max(char.poise for char in chars)
        if self.char.poise == maxpoise:
            self.game.active = self.char.name
            if self.game not in self.updated:
                self.updated.append(self.game)
        else:
            self.errors.append('%s does not have the highest poise'
                % self.char.name)
            return False
    elif value.startswith('hold'):
        # Hold
        if (self.char.time == TIME_READY
        and self.char.name not in self.game.hold):
            self.game.hold.append(self.char)
            if self.game not in self.updated:
                self.updated.append(self.game)
            # TODO: Cache this query?
            atready = Character.all().ancestor(self.game) \
                .filter('time =', TIME_READY).filter('active =', True) \
                .fetch(1000)
            if all(char.name in self.game.hold for char in atready):
                self._tick()
        elif self.char.time != TIME_READY:
            self.warnings.append('%s is not ready to hold' % self.char.name)
    elif value.startswith('interrupt'):
        # Interrupt
        self.game.active = self.char.name
        if self.game not in self.updated:
            self.updated.append(self.game)
    else:
        self.warnings.append('Unrecognized timing verb "%s"' % value)

# vim: ai et ts=4 sts=4 sw=4
