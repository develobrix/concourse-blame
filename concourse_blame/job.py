import os
import re


class Committer:

    def __init__(self, name: str, team_config: dict):
        self.name = name
        self.team = None
        for team, members in team_config.items():
            if name in members:
                self.team = team
                return


class ConcourseJob:

    def __init__(self, id: int, status: str):
        self.id = id
        self.status = status

    def __eq__(self, other):
        return self.id == other.id and self.status == other.status


def get_latest_job(concourse_target: str, concourse_job_name: str) -> ConcourseJob:
    latest_job = os.popen('fly -t {} builds -j {} -c 1'.format(concourse_target, concourse_job_name)).read()
    columns = re.split('\s+', latest_job)
    return ConcourseJob(columns[2], columns[3])


def get_latest_committer(bare_repo_path: str, team_config: dict) -> Committer:
    return_path = os.getcwd()
    os.chdir(bare_repo_path)
    os.system('git fetch origin master:master')
    latest_committer = os.popen("git log -1 --pretty=format:'%an'").read().replace("'", "")
    os.chdir(return_path)
    return Committer(latest_committer, team_config)
