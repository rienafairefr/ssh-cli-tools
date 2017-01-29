# -*- coding:utf-8 -*-
"""iotlabsshcli package implementing a ssh lib using fabric."""

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


from pssh import ParallelSSHClient, utils
from pprint import pprint


class OpenA8Ssh():
    """Implement SshAPI for Parallel SSH."""

    def __init__(self, config_ssh, groups={}, verbose=False):
        self.config_ssh = config_ssh
        self.groups = groups
        self.verbose = verbose

        if self.verbose:
            utils.enable_logger(utils.logger)

    def run(self, command):
        """Run ssh command using Parallel SSH."""
        for site in self.groups:
            client = ParallelSSHClient(self.groups[site],
                                       user='root',
                                       proxy_host='{}'
                                                  '.iot-lab.info'.format(site),
                                       proxy_user=self.config_ssh['user'])
            output = client.run_command(command)
            client.join(output)
            if self.verbose:
                self._print_output(output, self.groups[site])
        return

    def scp(self, src, dst):
        """Copy file to hosts using Parallel SSH copy_file"""
        sites = ['{}.iot-lab.info'.format(site) for site in self.groups]
        client = ParallelSSHClient(sites, user=self.config_ssh['user'])
        return client.copy_file(src, dst)

    def _print_output(self, output, hosts):
        for host in hosts:
            pprint(output[host])
            for line in output[host]['stdout']:
                pass
