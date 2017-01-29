# -*- coding:utf-8 -*-
"""iotlabsshcli parser for Open A8 cli."""

# This file is a part of IoT-LAB ssh-cli-tools
# Copyright (C) 2015 INRIA (Contact: admin@iot-lab.info)
# Contributor(s) : see AUTHORS file
#
# This software is governed by the CeCILL license under French law
# and abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info.
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.


import sys
import argparse
from iotlabcli import auth
from iotlabcli import helpers
from iotlabcli import rest
from iotlabcli.parser import common
import iotlabsshcli.open_a8


def parse_options():
    """Parse command line option."""
    parent_parser = common.base_parser()
    # We create top level parser
    parser = argparse.ArgumentParser(
        parents=[parent_parser],
    )

    common.add_expid_arg(parser)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True  # needed for python 3.

    # update-m3 parser
    update_parser = subparsers.add_parser('update-m3',
                                          help='update the M3 firmware of A8 '
                                               'node')
    update_parser.add_argument('firmware', help='firmware elf path.')
    # nodes list or exclude list
    common.add_nodes_selection_list(update_parser)

    # reset-m3 parser
    reset_parser = subparsers.add_parser('reset-m3',
                                         help='reset the M3 of A8 node')
    # nodes list or exclude list
    common.add_nodes_selection_list(reset_parser)

    return parser


def open_a8_parse_and_run(opts):
    """Parse namespace 'opts' object and execute M3 fw update action."""
    user, passwd = auth.get_user_credentials(opts.username, opts.password)
    api = rest.Api(user, passwd)
    exp_id = helpers.get_current_experiment(api, opts.experiment_id)

    config_ssh = {
        'user': user,
    }

    # TODO: replace list_nodes function in order to work without -l option.
    nodes = common.list_nodes(api, exp_id, opts.nodes_list,
                              opts.exclude_nodes_list)

    # TODO: filter only a8 nodes
    nodes = ["node-{0}".format(node) for node in nodes]

    command = opts.command
    if command == 'reset-m3':
        return iotlabsshcli.open_a8.reset_m3(config_ssh, nodes)
    elif command == 'update-m3':
        return iotlabsshcli.open_a8.update_m3(config_ssh, nodes, opts.firmware)
    else:  # pragma: no cover
        raise ValueError('Unknown command {0}'.format(command))


def main(args=None):
    """Open A8 SSH cli parser."""
    args = args or sys.argv[1:]  # required for easy testing.
    parser = parse_options()
    common.main_cli(open_a8_parse_and_run, parser, args)
