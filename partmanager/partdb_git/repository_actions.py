import git
import logging
import subprocess
from pathlib import Path
from git import RemoteProgress
from git.exc import NoSuchPathError
from .models import GitImportStatus

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('partdb_git')


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)


def update_or_clone_repo(repo_url, local_path, ssh_key=None):
    logger.info(f"Updating repository {repo_url}, in directory {local_path}")
    try:
        # Attempt to open the repository
        repo = git.Repo(local_path)
        # If the repository exists, pull the latest changes
        repo.remote().fetch()
        switch_to_local_branch(repo)
        repo.git.rebase('local')
        logger.info("Repository updated successfully.")
    except NoSuchPathError:
        # If the repository doesn't exist locally, clone it
        if ssh_key:
            git.Repo.clone_from(repo_url, local_path, progress=Progress(), env={"GIT_SSH_COMMAND": f"ssh -i {ssh_key}"})
        else:
            repo = git.Repo.clone_from(repo_url, local_path, progress=Progress())
        logger.info("Repository cloned successfully.")
    except Exception as e:
        logger.error("An error occurred:", repr(e))
        return None
    return repo


def generate_components(local_path):
    logger.info(f"Generating components")
    subprocess.run(['python', 'generate.py'], cwd=local_path + '/scripts')


def get_last_import_commit(repository_name):
    try:
        last_import = GitImportStatus.objects.get(part_db_name=repository_name)
        return last_import.part_db_last_import_commit
    except GitImportStatus.DoesNotExist as e:
        return None


def set_last_import_commit(repository_name, commit):
    last_import = GitImportStatus.objects.get_or_create(part_db_name=repository_name,
                                                        defaults={'part_db_last_import_commit': commit})


def generate_modified_component_list(directory, repo, commit):
    logger.info(f"Preparing modified files list")
    if commit:
        try:
            modified_files = repo.git.diff(commit, name_only=True).splitlines()
        except git.exc.GitCommandError:
            logger.warning(f"Error while checking for modified files in repository. Updating all files.")
            modified_files = list(Path(directory + "/parts/").rglob('*.json'))
    else:
        logger.info(f"No commit provided. Loading all files from repository")
        modified_files = list(Path(directory + "/parts/").rglob('*.json'))
    return modified_files


def commit_to_local_branch(partsdb_repo):
    try:
        switch_to_local_branch(partsdb_repo)
        partsdb_repo.git.add(update=True)
        commit = partsdb_repo.index.commit("Committing all modified files")
        return commit.hexsha
    except git.exc.GitCommandError as e:
        logger.error(f"Error: {e}")


def switch_to_local_branch(partsdb_repo):
    if 'local' in partsdb_repo.heads:
        branch = partsdb_repo.heads['local']
        branch.checkout()
    else:
        partsdb_repo.git.checkout('-b', 'local')
