#!/usr/bin/env python3

""" Unit tests for the manifest parser """

import mock
from manifest_parser import parse_current_manifest

@mock.patch('manifest_parser.open', new_callable=mock.mock_open,
            read_data="""<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <remote fetch="https://github.com" name="github" review="https://github.com"/>
  <remote fetch="other_url" name="other_remote" review="other_review"/>
  <default revision="repo" remote="github" sync-j="4" sync-s="true" />

  <project name="Javier-varez/buildsystem.git" path="buildsystem" groups="postform,cortex-m-scheduler" revision="main" >
    <linkfile src="template.mk" dest="Makefile" />
  </project>

  <project name="Javier-varez/Postform.git" path="postform" groups="postform" remote="other_remote" />
</manifest>
""")
def test_parse_current_manifest(mock_open):
    """ Test for parse_current_manifest """
    projects = parse_current_manifest('mypath')
    mock_open.assert_called_with('mypath/.repo/manifest.xml', 'r')

    assert projects == [
        {
            "name": "Javier-varez/buildsystem.git",
            "path": "buildsystem",
            "revision": "main",
            "remote": {
                'name': 'github',
                'url': "https://github.com"
            }
        },
        {
            "name": "Javier-varez/Postform.git",
            "path": "postform",
            "revision": "repo",
            "remote": {
                'name': 'other_remote',
                'url': "other_url"
            }
        }
    ]
