# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import os
import sys
import glob
import re
import itertools
import scipy.io.wavfile as wavfile

sys.path.append("/opt/mycroft/skills/speaker-rec-skill-test")

from gui.interface import ModelInterface
from gui.utils import read_wav

sys.path.append("/opt/mycroft/skills/speaker-rec-skill-test/filters")

from silence import remove_silence


__author__ = 'TREE'

LOGGER = getLogger(__name__)


class SpeakerRecSkillTest(MycroftSkill):
    def __init__(self):
        super(SpeakerRecSkillTest, self).__init__(name="SpeakerRecSkillTest")

        self.known_speakers = []

    def initialize(self):
        speaker_rec_greeting_intent = IntentBuilder("SpeakerRecGreetingIntent"). \
            require("SpeakerRecGreetingKeyword").build()
        self.register_intent(speaker_rec_greeting_intent, self.handle_speaker_rec_greeting_intent)

    def handle_speaker_rec_greeting_intent(self, message):
        directory = "/tmp/mycroft_wake_words"
        self.newest = max(glob.iglob(os.path.join(directory, '*.wav')), key=os.path.getctime)
        CWD_PATH = os.path.dirname(__file__)
        input_model = os.path.join(CWD_PATH, "model.out")
        m = ModelInterface.load(input_model)
        input_files = self.newest
        fs, signal = read_wav(input_files)
        label = m.predict(fs, signal)
        self.speak("Yes, I do recognize your voice, %s" % (label))
        print(self.newest)
        


    def stop(self):
        pass


def create_skill():
    return SpeakerRecSkillTest()
