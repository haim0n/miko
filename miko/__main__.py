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


def get_project_lib_list(project):
    """returns all libraries in use by project

    :param project: the Project object
    """
    try:
        for url in project.requirement_urls:
            project.lib_list.append(urllib2.urlopen(url).read())
    except urllib2.URLError as e:
        logging.debug("error on request: {}, {}".format(e, url))

    return project


def is_lib_in_requirements(lib, req_list):
    for req in req_list:
        if lib in req:
            return True

    return False


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

    projects_using_lib = []
    for project in pool.imap(get_project_lib_list, projects):
        print("got project: {}".format(project.name))
        if is_lib_in_requirements(args.library, project.lib_list):
            projects_using_lib.append(project)

    miko_run_summary = Summary(projects, projects_using_lib)
    miko_run_summary.print_summary()


if __name__ == '__main__':
    sys.exit(main())
