import logging
from celery import shared_task
from django.conf import settings
from celery_progress.backend import ProgressRecorder
from .repository_actions import update_or_clone_repo, generate_components, get_last_import_commit, \
    set_last_import_commit, generate_modified_component_list, commit_to_local_branch
from .update_partcatalog import update_manufacturers, update_distributors, update_partcatalog

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('partdb_git')


@shared_task(bind=True)
def update_all(self):
    progress_recorder = ProgressRecorder(self)
    partsdb_settings = settings.PARTSDB_CONFIG
    destination = partsdb_settings["directory"]
    repos = partsdb_settings["repositories"]
    for repository in repos:
        repo_dict = repos[repository]
        url = repo_dict["url"]
        branch = repo_dict['branch']
        ssh_key = None
        repo = update_or_clone_repo(url,
                                    branch,
                                    destination + repository,
                                    ssh_key=ssh_key,
                                    credintials=repo_dict['credentials'])
        if repo:
            progress_recorder.set_progress(1, 4, description='Updating manufacturers data')
            update_manufacturers(destination + repository)
            progress_recorder.set_progress(2, 4, description='Updating distributors data')
            update_distributors(destination + repository)
            progress_recorder.set_progress(3, 4, description='Generating components data')
            generate_components(destination + repository)
            last_import_commit = get_last_import_commit(repository)
            component_files = generate_modified_component_list(destination + repository, repo, last_import_commit)
            if len(component_files):
                progress_recorder.set_progress(4, 4, description='Updating components data')
                update_partcatalog(component_files, progress_recorder)
                new_commit = commit_to_local_branch(repo)
                set_last_import_commit(repository, new_commit)
                logger.info(f"Import done, new commit {new_commit}")
            else:
                logger.info(f"Nothing changed skipping.")
