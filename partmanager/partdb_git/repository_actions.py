import os
import shutil
import git
import logging
import subprocess
import filecmp
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


def update_or_clone_repo(repo_url, branch, local_path, ssh_key=None, credentials=None):
    logger.info(f"Updating repository {repo_url}, in directory {local_path}")
    try:
        # Attempt to open the repository
        repo = git.Repo(local_path)
        # If the repository exists, pull the latest changes
        repo.git.checkout(branch)
        repo.remote().pull()
        logger.info(f"Repository updated successfully. Latest commit is: {repo.head.commit.hexsha}")
    except NoSuchPathError:
        # If the repository doesn't exist locally, clone it
        if ssh_key:
            repo = git.Repo.clone_from(repo_url, local_path, progress=Progress(), env={"GIT_SSH_COMMAND": f"ssh -i {ssh_key}"})
        else:
            if credentials:
                repo = git.Repo.clone_from(f"https://{credentials['user']}:{credentials['password']}@{repo_url}",
                                           local_path,
                                           progress=Progress())
            else:
                repo = git.Repo.clone_from(repo_url, local_path, progress=Progress())
        logger.info("Repository cloned successfully.")
    except Exception as e:
        logger.error("An error occurred:", repr(e))
        return None
    return repo


def generate_components(local_path):
    logger.info(f"Generating components")
    subprocess.run(['python', 'generate.py', '--prefix', '../../generated/parts_new'], cwd=local_path.joinpath('scripts'))

def rename_generated_components_dir(local_path: Path):
    logger.info(f"Removing old generated components directory and renaming new one to old")
    old_path = local_path.joinpath('../generated/parts_old').resolve()
    if old_path.exists():
        shutil.rmtree(old_path)
    os.rename(local_path.joinpath('../generated/parts_new').resolve(),
              local_path.joinpath('../generated/parts_old').resolve())


def get_last_import_commit(repository_name):
    try:
        last_import = GitImportStatus.objects.get(part_db_name=repository_name)
        return last_import.part_db_last_import_commit
    except GitImportStatus.DoesNotExist as e:
        return None


def set_last_import_commit(repository_name, commit):
    last_import = GitImportStatus.objects.update_or_create(part_db_name=repository_name,
                                                           defaults={'part_db_last_import_commit': commit})


def generate_modified_component_list(directory, repo, commit):
    logger.info(f"Preparing modified files list, commit diff: {commit}")
    if commit:
        try:
            head_commit = repo.head.commit
            if commit != head_commit.hexsha:
                tmp_modified_files = repo.commit(commit).diff(head_commit.hexsha)
                modified_files = [f'{directory}/{i.a_path}' for i in tmp_modified_files if i.change_type in ['A', 'M'] and i.a_path.endswith('.json')]
                modified_files += generate_modified_generated_components_list(directory)
            else:
                modified_files = []
        except git.exc.GitCommandError as e:
            logger.warning(f"Error while checking for modified files in repository. Updating all files. Error: {e}")
            modified_files = list(directory.joinpath("components").rglob('*.json'))
            modified_files += generate_modified_generated_components_list(directory)
    else:
        logger.info(f"No commit provided. Loading all files from repository")
        modified_files = list(directory.joinpath("components").rglob('*.json'))
        modified_files += generate_modified_generated_components_list(directory)
    return modified_files


def generate_modified_generated_components_list(local_path: Path):
    old_path = local_path.joinpath('../generated/parts_old')
    new_path = local_path.joinpath('../generated/parts_new')
    if old_path.exists():
        result = compare_dirs(old_path, new_path)
        return result
    else:
        return list(new_path.rglob('*.json'))

def compare_dirs(old_path, new_path):
    dir_cmp = filecmp.dircmp(old_path.resolve(), new_path.resolve(), shallow=False)
    result = [new_path.joinpath(x).resolve() for x in dir_cmp.right_only]
    result += [new_path.joinpath(x).resolve() for x in dir_cmp.diff_files]

    for x in dir_cmp.common_dirs:
        result += compare_dirs(old_path.joinpath(x).resolve(), new_path.joinpath(x))
    return  result