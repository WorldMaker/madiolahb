# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.

def nextpos(hexmap, x, y, n, dir):
    if hexmap:
        if dir == 'n':
            if n % 2 != 0: return None, None
            else:          return x, y + n
        elif dir == 'ne':  return x + n % 2, y + n
        elif dir == 'e':   return x + n, y
        elif dir == 'se':  return x + n % 2, y - n
        elif dir == 's':
            if n % 2 != 0: return None, None
            else:          return x, y - n
        elif dir == 'sw':  return x - n % 2, y - n
        elif dir == 'w':   return x - n, y
        elif dir == 'nw':  return x - n % 2, y + n
        else:              raise ValueError, "%s is not a direction" % dir
    else:
        if dir == 'n':     return x, y + n
        elif dir == 'ne':  return x + n, y + n
        elif dir == 'e':   return x + n, y
        elif dir == 'se':  return x + n, y - n
        elif dir == 's':   return x, y - n
        elif dir == 'sw':  return x - n, y - n
        elif dir == 'w':   return x - n, y
        elif dir == 'nw':  return x - n, y + n
        else:              raise ValueError, "%s is not a direction" % dir

def at(self, subject=None, x=0, y=0, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    self.char.x = x
    self.char.y = y
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

def move(self, subject=None, object=None, count=0, dir=None, **kwargs):
    if not self._char(subject): return False
    if not self._active(): return False

    object = self._object(object)
    if object is None: return

    if self.game.hexmap and dir in ('n', 's') and count % 2 != 0:
        self.errors.append('%s is not a multiple of two for N/S on a hex map' %
            count)
        return

    self.char.x, self.char.y = nextpos(self.game.hexmap,
        self.char.x,
        self.char.y,
        count,
        dir,
    )
    if self.char.key() not in self.updated:
        self.updated.append(self.char.key())

# vim: ai et ts=4 sts=4 sw=4
