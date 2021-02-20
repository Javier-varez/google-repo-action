#!/usr/bin/env python3

""" Parses a git-repo manifest """

import xml.etree.ElementTree as ET


def parse_project_node(project, defaults, remotes):
    """ Parses a project node """
    if 'revision' in project.attrib:
        revision = project.attrib['revision']
    else:
        revision = defaults['revision']

    if 'remote' in project.attrib:
        remote = project.attrib['remote']
        if remote not in remotes:
            raise Exception(f"Can't find definition for {remote}")
        remote = remotes[remote]
    else:
        remote = defaults['remote']

    return {
        'name': project.attrib['name'],
        'path': project.attrib['path'],
        'revision': revision,
        'remote': remote,
    }


def parse_manifest(manifest_path, project_root):
    """ Parses a given manifest file. """
    projects = []
    remotes = {}
    defaults = {}
    with open(manifest_path, 'r') as manifest_file:
        document = ET.parse(manifest_file)
        manifest_root = document.getroot()
        for node in manifest_root:
            if node.tag == 'include':
                include_file = project_root + '/.repo/manifests/' + \
                               node.attrib['name']
                projects.extend(parse_manifest(include_file, project_root))
            elif node.tag == 'project':
                projects.append(parse_project_node(node, defaults, remotes))
            elif node.tag == 'remote':
                remotes[node.attrib['name']] = {
                    'name': node.attrib['name'],
                    'url': node.attrib['fetch']
                }
            elif node.tag == 'default':
                if 'revision' in node.attrib:
                    defaults['revision'] = node.attrib['revision']
                if 'remote' in node.attrib:
                    remote = node.attrib['remote']
                    if remote not in remotes:
                        raise Exception(f"Can't find definition for {remote}")
                    defaults['remote'] = remotes[remote]
    return projects


def parse_current_manifest(project_root):
    """ Parses the current manifest file for the selected project root """
    manifest_path = project_root + '/.repo/manifest.xml'
    return parse_manifest(manifest_path, project_root)
