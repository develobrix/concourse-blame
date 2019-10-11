import json
import sys

from concourse_blame import ConcourseBlame

if len(sys.argv) < 2:
    print('USAGE: python concourse-blame.py /path/to/config.json')
    print('       If you just want to check the voices installed on your system, run:')
    print('       python concourse-blame.py --voices')
    exit(0)

# voice check
if sys.argv[1] == '--voices':
    from concourse_blame.tts import TTS

    TTS.play_system_voice_examples()
    exit(0)

# load configuration and run app
config_path = sys.argv[1]
config = {}
with open(config_path, encoding='utf-8-sig') as config_file:
    config = json.load(config_file)
if not config:
    print('Could not read configuration from file {}'.format(config_path))
    exit(1)

app = ConcourseBlame(config)
app.run()
