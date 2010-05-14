# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext.webapp import template
from waveapi import events, robot, appengine_robot_runner
from backend import COMMAND_RE, Commander
from hce import max_influence
from models import WaveGame
import waml

def OnBlipSubmitted(event, wavelet):
    game = WaveGame.all().filter('waveid =', wavelet.wave_id).get()
    if not game: return
    blip = event.blip
    com = Commander(game, blip.creator)
    for match in COMMAND_RE.finditer(blip.text):
        result = com.command(match.group('commands'))
        if result is not False:
            # Swap brackets for parens and italicize to mark the command read
            blip.at(match.start()).replace('(')
            blip.at(match.end() - 1).replace(')')
            blipmatch = blip.range(match.start(), match.end())
            blipmatch.annotate('style/fontStyle', 'italic')
        if any(sen['verb'] == 'act' or sen['verb'] == 'contest' for sen
        in com.commanded):
            waml.append_waml(blip, 'wave/roll.yaml', {'roll': game.lastroll})
        if com.errors or com.warnings:
            waml.append_waml(blip.insert_inline_blip(match.end()-2),
                'wave/errors.yaml',
                {'errors': com.errors, 'warnings': com.warnings},
            )
        if com.tickselapsed:
            ticks = ''
            if com.tickselapsed <= 3:
                ticks = ' '.join(['Tick.'] * com.tickselapsed)
            else:
                ticks = '%s Ticks.' % com.tickselapsed
            waml.append_waml(wavelet.reply(),
                'wave/ticks.yaml',
                {'ticks': ticks, 'atready': com.atready, 
                    'maxpoise': max(max_influence(char, 'poise') for char \
                    in com.atready)},
            )
    com.commit()

def OnRobotAdded(event, wavelet):
    if WaveGame.all().filter('waveid =', wavelet.wave_id).count(1) > 0:
        return
    game = WaveGame(waveid=wavelet.wave_id, title=wavelet.title)
    game.put()
    waml.append_waml(wavelet.reply(),
        'wave/welcome.yaml',
        {'game': game},
    )

def title_changed(event, wavelet):
    game = WaveGame.all().filter('waveid =', wavelet.wave_id).get()
    if not game: return
    game.title = wavelet.title
    game.put()

if __name__ == '__main__':
    template.register_template_library('templatetags')
    myRobot = robot.Robot('hce-bee',
        image_url='http://hce-bee.appspot.com/static/logo.jpg',
        version='2',
        profile_url='http://hce-bee.appspot.com/')
    myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
    myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
    myRobot.register_handler(events.WaveletTitleChanged, title_changed)
    appengine_robot_runner.run(myRobot)

# vim: ai et ts=4 sts=4 sw=4
