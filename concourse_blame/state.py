import os
import random
import re
from abc import ABC, abstractmethod

from .committer import Committer


class State(ABC):

    @abstractmethod
    def get_configured_sound_file(self, sound_config: dict):
        pass

    @abstractmethod
    def get_tts_text(self, committer: Committer, text_config: dict) -> str:
        pass


class ConcourseJob(State):

    @staticmethod
    def get_latest(concourse_target: str, concourse_job_name: str):
        latest_job = os.popen('fly -t {} builds -j {} -c 1'.format(concourse_target, concourse_job_name)).read()
        columns = re.split('\s+', latest_job)
        return ConcourseJob(columns[2], columns[3], concourse_job_name)

    def __init__(self, id: int, status: str, job_name: str):
        self.id = id
        self.status = status
        self.job_name = job_name

    def get_configured_sound_file(self, sound_config: dict):
        if self.status in sound_config['status']:
            return sound_config['status'][self.status]
        return None

    def get_tts_text(self, committer: Committer, text_config: dict) -> str:
        texts = text_config['status'][self.status]
        if len(texts) > 0:
            text = random.choice(texts)
            return text.replace('%committer', committer.get_text(text_config))

    def __eq__(self, other):
        return isinstance(other, ConcourseJob) \
               and self.id == other.id \
               and self.status == other.status \
               and self.job_name == other.job_name

    def __repr__(self):
        return 'ConcourseJob [job: {}, id: {}, status: {}]'.format(self.job_name, self.id, self.status)


class GitCommit(State):

    @staticmethod
    def get_latest(bare_repo_path: str):
        return_path = os.getcwd()
        os.chdir(bare_repo_path)
        os.system('git fetch origin master:master')
        latest_commit_id = os.popen("git log -1 --pretty=format:%H").read()
        os.chdir(return_path)
        return GitCommit(latest_commit_id)

    def __init__(self, id: int):
        self.id = id

    def get_configured_sound_file(self, sound_config: dict):
        if 'commit' in sound_config:
            return sound_config['commit']
        return None

    def get_tts_text(self, committer: Committer, text_config: dict) -> str:
        texts = text_config['commit']
        if len(texts) > 0:
            text = random.choice(texts)
            return text.replace('%committer', committer.get_text(text_config))

    def __eq__(self, other):
        return isinstance(other, GitCommit) and self.id == other.id

    def __repr__(self):
        return 'GitCommit [id: {}]'.format(self.id)


def get_latest_state(config: dict) -> State:
    if 'concourse' in config:
        return ConcourseJob.get_latest(config['concourse']['target'], config['concourse']['job'])
    return GitCommit.get_latest(config['git']['clone_path'])
