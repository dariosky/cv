import os

from fabric.context_managers import cd
from fabric.contrib.files import exists
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.tasks import execute


class Config:
    project_path = '~/webapps/dariocv'
    git_repo = 'git@github.com:dariosky/cv.git'


def set_hosts(hosts):
    # using env.hosts only didn't work for me
    env.hosts = hosts
    env.host_string = ",".join(hosts)


def clone():
    with cd(Config.project_path):
        run(f"git clone {Config.git_repo} .")


def pull_repo():
    with cd(Config.project_path):
        run(f'git pull')


@task
def deploy():
    """ Pull the changes, update requirements on remote host"""
    with cd(Config.project_path):
        if not exists('.git'):
            print("Cloning GIT repo")
            execute(clone)
        execute(pull_repo)


project_folder = os.path.dirname(__file__)
os.chdir(project_folder)

if os.path.exists(os.path.expanduser("~/.ssh/config")):
    env.use_ssh_config = True

if not env.hosts:
    set_hosts('dariosky')  # the host where to deploy
