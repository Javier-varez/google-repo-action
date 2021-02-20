#!/usr/bin/env python3

""" Downloads dependent changes """

import os
import argparse
import subprocess

from  manifest_parser import parse_current_manifest

def run_command(command, directory):
    """ Runs a command, logging it to stdout """
    print(f"Running '{command}' in '{directory}'")
    return subprocess.check_output(command.split(' '), cwd=directory)

def checkout_root_project(project_root, root_project, branch):
    """ Checksout the root project to the selected branch """
    directory = project_root + '/' + root_project['path']
    run_command(f"git fetch {root_project['remote']['name']} {branch}", directory)
    run_command(f"git reset --hard FETCH_HEAD", directory)

def parse_dependencies(project_root, root_project):
    """ Parses the dependencies found in the root_project """
    dependencies = []
    directory = project_root + '/' + root_project['path']
    commit_msg = run_command("git rev-list --max-count=1 HEAD --format=full",\
                             directory).decode('utf-8')
    for line in commit_msg.split('\n'):
        if line.strip().startswith('Depends-On:'):
            dependency = line.strip().split(" ")[1]
            dependencies.append(dependency)
    return dependencies

def download_dependencies(projects, dependencies, branch, project_root=os.getcwd()):
    """ Downloads a list of dependencies """
    for dependency in dependencies:
        project = find_project_for_name(projects, dependency)
        if project is None:
            print(f'Skipping unknown dependency {dependency}')
            continue
        directory = project_root + '/' + project['path']
        run_command(f"git fetch {project['remote']['name']} {branch}", directory)

def find_project_for_name(projects, name):
    """ Finds a project with a given name """
    for project in projects:
        if name == project['name']:
            return project
    return None

def main():
    """ Executes the program """
    parser = argparse.ArgumentParser(description='Downloads changes in the associated repositories')
    parser.add_argument('branch', help='branch to sync across projects')
    parser.add_argument('root_project', \
                        help='name of the root project that contains the dependency list')
    args = parser.parse_args()

    project_root = os.getcwd()
    projects = parse_current_manifest(project_root)

    root_project = find_project_for_name(projects, args.root_project)
    if root_project is None:
        raise Exception(f'Root project {args.root_project} not found in manifest!')
    checkout_root_project(project_root, root_project, args.branch)
    dependencies = parse_dependencies(project_root, root_project)
    download_dependencies(projects, dependencies, args.branch, project_root)

if __name__ == '__main__':
    main()
