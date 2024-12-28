import logging
from pathlib import Path
from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
from .repository_actions import update_or_clone_repo, generate_components, get_last_import_commit, \
    set_last_import_commit, generate_modified_component_list, rename_generated_components_dir
from .update_partcatalog import update_manufacturers, update_distributors, update_partcatalog

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('partdb_git')


@shared_task(bind=True)
def update_all(self):
    progress_recorder = ProgressRecorder(self)
    partsdb_settings = settings.PARTSDB_CONFIG
    destination = Path(partsdb_settings["directory"])
    repos = partsdb_settings["repositories"]
    for repository in repos:
        repo_dict = repos[repository]
        url = repo_dict["url"]
        branch = repo_dict['branch']
        ssh_key = None
        fs_repo_location = destination.joinpath(repository).joinpath('repo')
        repo = update_or_clone_repo(url,
                                    branch,
                                    fs_repo_location,
                                    ssh_key=ssh_key,
                                    credentials=repo_dict['credentials'])
        if repo:
            last_import_commit = get_last_import_commit(repository)
            head_commit = repo.head.commit
            if last_import_commit is None or last_import_commit != head_commit.hexsha:
                progress_recorder.set_progress(1, 4, description='Updating manufacturers data')
                update_manufacturers(fs_repo_location)
                progress_recorder.set_progress(2, 4, description='Updating distributors data')
                update_distributors(fs_repo_location)
                progress_recorder.set_progress(3, 4, description='Generating components data')
                generate_components(fs_repo_location)
                component_files = generate_modified_component_list(fs_repo_location, repo, last_import_commit)
                if len(component_files):
                    progress_recorder.set_progress(4, 4, description='Updating components data')
                    update_partcatalog(component_files, progress_recorder)
                    latest_commit = repo.commit(branch)
                    set_last_import_commit(repository, latest_commit)
                    rename_generated_components_dir(fs_repo_location)
                    logger.info(f"Import done, new commit {latest_commit}")
                else:
                    logger.info(f"Nothing changed skipping.")
