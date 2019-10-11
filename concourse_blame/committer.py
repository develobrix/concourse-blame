import os


class Committer:

    def __init__(self, name: str, team_config: dict):
        self.name = name
        self.team = None
        if team_config:
            for team, members in team_config.items():
                if name in members:
                    self.team = team
                    return

    def get_text(self, text_config: dict) -> str:
        if self.team:
            return text_config['committer']['from_team'] \
                .replace('%name', self.name) \
                .replace('%team', self.team)
        return text_config['committer']['no_team'] \
            .replace('%name', self.name)

    def __repr__(self):
        return 'Committer [name: {}, team: {}]'.format(self.name, self.team)


def get_latest_committer(bare_repo_path: str, team_config: dict) -> Committer:
    return_path = os.getcwd()
    os.chdir(bare_repo_path)
    os.system('git fetch origin master:master')
    latest_committer = os.popen("git log -1 --pretty=format:%an").read()
    os.chdir(return_path)
    return Committer(latest_committer, team_config)
