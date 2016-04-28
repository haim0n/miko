#!/usr/bin/env python

import argparse
import eventlet
from eventlet.green import urllib2
import getpass
from github import Github
import logging
import sys


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


def fetch_lib_list(url):
    """Returns the content of the url.

    :param url: the url which contains the libraries list
    """
    try:
        return urllib2.urlopen(url).read()
    except Exception:
        logging.debug("No such page: {}".format(url))
        return None


def check_project(project):
    """Return the libraries list and the name of the project.

    :param project: Github repo object
    """

    logging.info("Searching in {}".format(project.keys()[0]))
    pool = eventlet.GreenPool()
    for lib_list in pool.imap(fetch_lib_list, project.values()[0]):
        return lib_list, project.keys()[0]


def get_projects_using_library(repos, lib):
    """Returns list of projects which using the specific library.

    :param repos: list of Github repo objects
    :param lib: the name of the chosen library
    """
    pool = eventlet.GreenPool()
    projects_using_lib = []

    for lib_list, project in pool.imap(check_project, repos):
        if lib_list:
            if lib_list.find(lib) != -1:
                projects_using_lib.append(project)

    return projects_using_lib


def summary(repos_counter, lib, proj_using_lib):
    """Output summary."""

    logging.info("=========== Summary ===========")
    logging.info("Scanned {} of repos".format(repos_counter))
    for project in proj_using_lib:
            logging.info("{} is using {}".format(project, lib))


def main():
    """Miko main loop."""

    repos = []

    parser = create_parser()
    args = parser.parse_args()

    if not args.debug:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)

    if not args.library:
        parser.error("Must specify library name")

    if not args.user:
        gith = Github()
    else:
        password = getpass.getpass("Enter password: ")
        gith = Github(args.user, password)
    openstack_org = gith.get_organization(ORG_NAME)

    for repo in openstack_org.get_repos():
        repos.append({repo.name:
                      [REPO_RAW_URL_PREFIX +
                       "/{}/master/{}".format(
                           repo.name, req_file) for req_file in REQ_FILES]})

    logging.info("Start scanning. This might take a while!")
    proj_using_lib = get_projects_using_library(repos, args.library)

    summary(len(repos), args.library, proj_using_lib)

if __name__ == '__main__':

    sys.exit(main())
