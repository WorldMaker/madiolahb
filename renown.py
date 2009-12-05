# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.

def renown(self, subject=None, object=None, influence=None, count=0, **kwargs):
    # Subject is ignored -- always sender
    object = self._object(object)
    if object is None: return

    self.game.renownvote = True
    self.game.renownnom = object.key()
    self.game.renowninf = influence
    self.game.renowncount = count
    if self.sender in self.players:
        self.game.renownaye = [self.sender]
    else:
        self.game.renownaye = []
    self.game.renownnay = []
    self.gameupdated = True

def vote(self, subject=None, value='', **kwargs):
    # Subject is ignored -- always sender
    if self.sender not in self.game.players:
        self.errors.append('%s is not playing and has no vote.' % self.sender)
        return
    if value.startswith('assent') or value == 'aye':
        if self.sender in self.game.renownnay:
            self.game.renownnay.remove(self.sender)
        self.game.renownaye.append(self.sender)
    elif value.startswith('dissent') or value == 'nay':
        if self.sender in self.game.renownaye:
            self.game.renownaye.remove(self.sender)
        self.game.renownnay.append(self.sender)
    # Simple majority checks
    ayes, nays = False, False
    if value.startswith('acclimate'):
        ayes = (len(self.game.renownaye) > 0
            and len(self.game.renownaye) > len(self.game.renownnay))
        nays = not ayes
    else:
        ayes = len(self.game.renownaye) > len(self.game.players) / 2 + 1
        nays = len(self.game.renownnay) > len(self.game.players) / 2 + 1
    if ayes:
        toks = getattr(self.game.renownnom, self.game.renowninf, 0)
        setattr(self.game.renownnom, self.game.renowninf,
            toks + self.game.renowncount)
        if self.game.renownnom.key() not in self.updated:
            self.updated.append(self.game.renownnom.key())
    if ayes or nays:
        self.game.renownvote = False
        self.game.renownnom = None
        self.game.renowninf = None
        self.game.renowncount = 0
        self.game.renownaye = []
        self.game.renownnay = []
    self.gameupdated

# vim: ai et ts=4 sts=4 sw=4
