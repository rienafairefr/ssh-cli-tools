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

from __future__ import print_function
import os.path
from iotlabsshcli.sshlib import OpenA8Ssh


def _nodes_grouped(nodes):
    """Group nodes per site from a list of nodes.
    >>> _sites_from_nodes([])
    []
    >>> _sites_from_nodes(['node-a8-1.grenoble.iot-lab.info',
    ...                    'node-a8-2.grenoble.iot-lab.info',
    ...                    'node-a8-2.saclay.iot-lab.info',
    ...                    'node-a8-2.lille.iot-lab.info'])
    {'grenoble': ['node-a8-1', 'node-a8-2'],
    ...           'lille': ['node-a8-2'],
    ...           'saclay': ['node-a8-2']}
    """
    result = {}
    for host in nodes:
        node = host.split('.')[0]
        site = host.split('.')[1]
        if site not in result:
            result.update({site: [node]})
        else:
            result[site].append(node)
    return result


_MKDIR_DST_CMD = 'mkdir -p {}'
_UPDATE_M3_CMD = 'source /etc/profile && /usr/bin/flash_a8_m3 {}'
_RESET_M3_CMD = 'source /etc/profile && /usr/bin/reset_a8_m3'


def update_m3(config_ssh, nodes, firmware):
    """Update the firmware of M3 of open A8 nodes."""
    results = []

    # Configure ssh and remote firmware names.
    groups = _nodes_grouped(nodes)
    ssh = OpenA8Ssh(config_ssh, groups=groups)
    remote_fw = os.path.join('~/A8/.iotlabsshcli', os.path.basename(firmware))

    # Create firmware destination directory
    ssh.run(_MKDIR_DST_CMD.format(os.path.dirname(remote_fw)))

    # Copy firmware on sites.
    ssh.scp(firmware, remote_fw)

    # Run firmware update.
    ssh.run(_UPDATE_M3_CMD.format(remote_fw))

    return results


def reset_m3(config_ssh, nodes):
    """Reset the M3 of open A8 nodes."""
    results = []

    # Configure ssh.
    groups = _nodes_grouped(nodes)
    ssh = OpenA8Ssh(config_ssh)

    # Run M3 reset command.
    ssh.run(_RESET_M3_CMD, groups=groups)

    return results
