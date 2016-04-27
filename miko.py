#!/usr/bin/env python

import argparse
import getpass
from github import Github
import logging
import sys
import urllib2


ORG_NAME = 'openstack'
REQ_FILES = ['requirements.txt', 'test-requirements.txt', 'other-requirements.txt']
REPO_RAW_URL = "https://raw.githubusercontent.com/" + ORG_NAME


def create_parser():
    """Returns argument parser."""

    parser = argparse.ArgumentParser(
        description='Identify which OpenStack projects use specific library.')
    parser.add_argument(
        '--library', dest='library', help='library name')
    parser.add_argument(
        '--user', dest='user', help='Github username')


    return parser

def check_library_used(repo, lib):
    """Checks if the library is used by the project.
    
    :param repo: Github repo object
    :param library: the library name.
    """

    found = False
    for req_file in REQ_FILES:
        try:
            req_list = urllib2.urlopen(REPO_RAW_URL +
                                   "/{}/master/{}".format(repo.name, req_file)).read()
        except:
            req_list = ""

        if req_list.find(lib) != -1:
            found = True
                                
    if found:
        logging.info("{} is using {} :)".format(repo.name, lib))
    else:
        logging.info("{} is not using {} :(".format(repo.name, lib))

    return found
            


def summary(repos_counter, lib, repos_use_library):
    """ Print summary."""

    logging.info("=========== Summary ===========")
    logging.info("Scanned {} of repos".format(repos_counter))
    if not repos_use_library:
        logging.info("Couldn't find any repos that use this library")
    else:
        logging.info("Repos using '{}':".format(lib))
        for repo in repos_use_library:
            logging.info("Project: {}".format(repo))


def main():
    """Miko main loop."""

    repos_counter = 0
    repos_use_library = []

    parser = create_parser()
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    if not args.library:
        parser.error("Must specify library name")
        
    if not args.user:
        gith = Github()
    else:
        password = getpass.getpass("Enter password: ")
        gith = Github(args.user, password)
    openstack_org = gith.get_organization(ORG_NAME)

    logging.info("Start scanning. This might take a while!")
    for repo in openstack_org.get_repos():
        repos_counter += 1
        if check_library_used(repo, args.library):
            repos_use_library.append(repo.name)

    summary(repos_counter, args.library, repos_use_library)


if __name__ == '__main__':

    sys.exit(main())
