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


import os.path
import iotlabsshcli.sshlib
import fabric.api


class Ssh(iotlabsshcli.sshlib.SshAPI):
    """Implement SshAPI for fabric."""

    def __init__(self, config_ssh):
        self.config_ssh = config_ssh
        self._config_fabric()

    def _config_fabric(self):
        env = fabric.api.env
        env.user = self.config_ssh['user']
        env.use_ssh_config = True
        env.ssh_config_path = os.path.join(os.path.dirname(__file__),
                                           'ssh_config')
        env.reject_unknown_hosts = False
        env.disable_known_hosts = True
        env.abort_on_prompts = True
        env.skip_bad_hosts = True
        env.pool_size = 10

    @staticmethod
    def _run(*args, **kwargs):
        return fabric.api.run(*args, **kwargs).return_code

    @staticmethod
    def _put(*args, **kwargs):
        return fabric.api.put(*args, **kwargs)

    def run(self, command, hosts=None):
        """Run ssh command using fabric."""
        return fabric.api.execute(self._run, command, hosts=hosts)

    def scp(self, src, dst, hosts=None):
        """Copy file to hosts using scp"""
        return fabric.api.execute(self._put, src, dst, hosts=hosts)
