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
from iotlabsshcli.sshlib.fabric_ssh import Ssh


def _sites_from_nodes(nodes):
    """Get list of sites from a list of nodes.
    >>> _sites_from_nodes([])
    []
    >>> _sites_from_nodes(['node-a8-1.grenoble.iot-lab.info',
    ...                    'node-a8-2.grenoble.iot-lab.info',
    ...                    'node-a8-2.saclay.iot-lab.info',
    ...                    'node-a8-2.lille.iot-lab.info'])
    ['grenoble.iot-lab.info', 'lille.iot-lab.info', 'saclay.iot-lab.info']
    """
    sites = {host.split('.', 1)[1] for host in nodes}
    return sorted(list(sites))


_UPDATE_M3_CMD = 'flash_a8_m3 {0}'


def update_m3(config_ssh, nodes, firmware):
    """Update the firmware of M3 of open A8 nodes."""
    results = []

    # Configure ssh and remote firmware names.
    sites = _sites_from_nodes(nodes)
    remote_fw = os.path.join('~/A8', os.path.basename(firmware))
    ssh = Ssh(config_ssh)

    # Copy firmware on sites.
    result = ssh.scp(firmware, remote_fw, hosts=sites)
    results.append({'scp': result})

    # Run firmware update.
    result = ssh.run(_UPDATE_M3_CMD.format(remote_fw), hosts=nodes)
    results.append({'update-m3': result})

    return results
