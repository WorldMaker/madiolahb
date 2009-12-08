from google.appengine.webapp import template
from waveapi import events
from waveapi import model
from waveapi import robot
from models import WaveGame

def OnBlipSubmitted(properties, context):
    root_wavelet = context.GetRootWavelet()
    waveid = root_wavelet.GetWaveId()
    blip = context.GetBlipById(properties['blipId'])


def OnRobotAdded(properties, context):
    root_wavelet = context.GetRootWavelet()
    waveid = root_wavelet.GetWaveId()
    if WaveGame.all(waveid=waveid).count(1) > 0:
        return
    game = WaveGame(waveid=waveid)
    game.put()
    root_wavelet.CreateBlip().GetDocument().SetText(
        template.render('wave/welcome.txt', {'game': game}))

if __name__ == '__main__':
    myRobot = robot.Robot('hce-bee',
        image_url='http://hce-bee.appspot.com/static/logo.jpg',
        version='1',
        profile_url='http://hce-bee.appspot.com/')
    myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.Run()

# vim: ai et ts=4 sts=4 sw=4
