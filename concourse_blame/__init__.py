import getpass
import time

from playsound import playsound

from .committer import *
from .state import *
from .tts import *


class ConcourseBlame:

    def __init__(self, config: dict):
        self.config = config

    def run(self):
        # initialize bare repository if not exists
        if not os.path.isdir(self.config['git']['clone_path']):
            os.system('git clone --bare {} {}'.format(
                self.config['git']['repository_url'],
                self.config['git']['clone_path']))

        # fly login
        if 'concourse' in self.config:
            password = getpass.getpass('Enter concourse password: ')
            error = os.system('fly login -t {} -u {} -p {}'.format(
                self.config['concourse']['target'],
                self.config['concourse']['user'],
                password))
            if error:
                exit(1)

        # init tts
        tts = TTS(self.config['tts']['voice_id'], self.config['tts']['words_per_minute'])
        if 'greeting' in self.config['tts']:
            tts.say(self.config['tts']['greeting'])

        # get latest state for initialization
        latest_state = get_latest_state(self.config)
        print('Initialized in state: {}'.format(latest_state))

        while True:
            time.sleep(self.config['update_rate_seconds'])

            # get latest state
            current_state = get_latest_state(self.config)
            if latest_state == current_state:
                continue

            # state has changed

            latest_state = current_state
            print('State update: {}'.format(latest_state))

            if not latest_state.get_configured_sound_file(self.config['sounds']):
                print('... but no notification has been configured for this state update.')
                continue

            # there is a sound configured to be played for the new state

            latest_committer = get_latest_committer(self.config['git']['clone_path'], self.config['teams'])
            print('... from {}'.format(latest_committer))

            # start sound
            if 'start' in self.config['sounds']:
                playsound(self.config['sounds']['start'])

            # configured state sound
            playsound(latest_state.get_configured_sound_file(self.config['sounds']))

            # tts
            tts.say(latest_state.get_tts_text(latest_committer, self.config['texts']))

            # end sound
            if 'end' in self.config['sounds']:
                playsound(self.config['sounds']['end'])
