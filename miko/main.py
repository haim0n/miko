#!/usr/bin/env python

import argparse
import eventlet
from eventlet.green import urllib2
import getpass
from github import Github
import logging
import sys

from project import Project
from summary import Summary


ORG_NAME = 'openstack'
REQ_FILES = ['requirements.txt',
             'test-requirements.txt',
             'other-requirements.txt']
REPO_RAW_URL_PREFIX = "https://raw.githubusercontent.com/" + ORG_NAME


def create_parser():
    """Returns argument parser."""

    parser = argparse.ArgumentParser(
        description='Identify which OpenStack projects use specific library.')
    parser.add_argument(
        '--library', dest='library', help='Library name')
    parser.add_argument(
        '--user', dest='user', help='Github username')
    parser.add_argument(
        '--debug', dest='debug', action='store_true', help='Turn on debug')

    return parser


def set_logging(debug_mode):
    """Sets logging level.

    :param debug_mode: whether debug mode should be enabled or not
    """

    if not debug_mode:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)


def check_lib_list(url, lib, project):
    """Checks if library is mentioned in requirements file

       and sets 'found_library' attribute accordingly.

    :param url: the url of the requirements file
    :param lib: the name of the library
    :param project: the Project object
    """
    try:
        lib_list = urllib2.urlopen(url).read()
        if lib_list.find(lib) != -1:
            logging.debug("There is a match in {}".format(url))
            project.found_library = True
    except Exception:
        logging.debug("No such url: {}".format(url))


def find_library(project_tuple):
    """Calls the method for checking the lib in requirements

       file, for each specified requirement file in the project.

    :param project_tuple: tuple(Project, lib)
    """
    project, lib = project_tuple
    logging.info("Scanning project: {}".format(project.name))
    for url in project.requirement_urls:
        check_lib_list(url, lib, project)

    return project


def main():
    """Miko main loop."""

    parser = create_parser()
    args = parser.parse_args()

    set_logging(args.debug)

    if not args.library:
        parser.error("Must specify library name")

    if not args.user:
        gith = Github()
    else:
        password = getpass.getpass("Enter password: ")
        gith = Github(args.user, password, per_page=1000)

    openstack_org = gith.get_organization(ORG_NAME)
    logging.info("Pulling information on all OpenStack projects")
    repos = openstack_org.get_repos()

    projects = []
    projects_counter = 0
    pool = eventlet.GreenPool(64)
    # Create list of project objects
    for repo in repos:
        projects_counter += 1
        sys.stdout.write("Pulled the data of {} projects\r"
                         .format(projects_counter))
        sys.stdout.flush()
        project_urls = [
            '{}/{}/master/{}'.format(REPO_RAW_URL_PREFIX, repo.name, req_file)
            for req_file in REQ_FILES]
        project = Project(repo.name, project_urls)
        projects.append(project)

    proj_tuples = [(proj, args.library) for proj in projects]
    for project in pool.imap(find_library, proj_tuples):
        print("got project: {}".format(project.name))

    miko_run_summary = Summary(projects_counter, projects)
    miko_run_summary.print_summary()


if __name__ == '__main__':
    sys.exit(main())
