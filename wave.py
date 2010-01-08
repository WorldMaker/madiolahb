# HCE Bee
# Copyright 2009 Max Battcher. Licensed for use under the Ms-RL. See LICENSE.
from google.appengine.ext.webapp import template
from waveapi import events, robot
from waveapi.document import Range
from backend import COMMAND_RE, Commander
from hce import max_influence
from models import WaveGame
import waml

def OnBlipSubmitted(properties, context):
    root_wavelet = context.GetRootWavelet()
    waveid = root_wavelet.GetWaveId()
    game = WaveGame.all().filter('waveid =', waveid).get()
    if not game: return
    blip = context.GetBlipById(properties['blipId'])
    com = Commander(game, blip.GetCreator())
    doc = blip.GetDocument()
    for match in COMMAND_RE.finditer(doc.GetText()):
        result = com.command(match.group('commands'))
        if result is not False:
            # Swap brackets for parens and italicize to mark the command read
            doc.SetTextInRange(Range(match.start(), match.start() + 1), '(')
            doc.SetTextInRange(Range(match.end() - 1, match.end()), ')')
            doc.SetAnnotation(Range(match.start(), match.end()), 
                'style/fontStyle', 'italic')
        if any(sen['verb'] == 'act' or sen['verb'] == 'contest' for sen
        in com.commanded):
            waml.append_waml(doc, 'wave/roll.yaml', {'roll': game.lastroll})
        if com.errors or com.warnings:
            waml.append_waml(doc.InsertInlineBlip(match.end()-2).GetDocument(),
                'wave/errors.yaml',
                {'errors': com.errors, 'warnings': com.warnings},
            )
        if com.tickselapsed:
            ticks = ''
            if com.tickselapsed <= 3:
                ticks = ' '.join(['Tick.'] * com.tickselapsed)
            else:
                ticks = '%s Ticks.' % com.tickselapsed
            waml.append_waml(root_wavelet.CreateBlip().GetDocument(),
                'wave/ticks.yaml',
                {'ticks': ticks, 'atready': com.atready, 
                    'maxpoise': max(max_influence(char, 'poise') for char \
                    in com.atready)},
            )
    com.commit()

def OnRobotAdded(properties, context):
    root_wavelet = context.GetRootWavelet()
    waveid = root_wavelet.GetWaveId()
    if WaveGame.all().filter('waveid =', waveid).count(1) > 0:
        return
    game = WaveGame(waveid=waveid, title=root_wavelet.GetTitle())
    game.put()
    waml.append_waml(root_wavelet.CreateBlip().GetDocument(),
        'wave/welcome.yaml',
        {'game': game},
    )

def title_changed(properties, context):
    root_wavelet = context.GetRootWavelet()
    game = WaveGame.all().filter('waveid =', waveid).get()
    if not game: return
    game.title = root_wavelet.GetTitle()
    game.put()

if __name__ == '__main__':
    template.register_template_library('templatetags')
    myRobot = robot.Robot('hce-bee',
        image_url='http://hce-bee.appspot.com/static/logo.jpg',
        version='2',
        profile_url='http://hce-bee.appspot.com/')
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.RegisterHandler(events.WAVELET_TITLE_CHANGED, title_changed)
    myRobot.Run()

# vim: ai et ts=4 sts=4 sw=4
