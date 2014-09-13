# Audio Daemon: this process does the audio processing and stuff like queuing up new files

from threading import Thread

class AudioDaemon(Thread):
    def __init__(self):
        Thread.__init__(self)
        return

    def run(self):
        return
