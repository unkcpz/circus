# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from subprocess import Popen
import os
from pwd import getpwnam
from grp import getgrnam

import time


class Fly(object):
    def __init__(self, wid, cmd, wdir, shell, uid=None, gid=None):
        self.wid = str(wid)
        self.wdir = wdir
        self.shell = shell
        self.cmd = cmd.replace('$WID', self.wid)
        if uid is not None:
            self.uid = getpwnam(uid)[2]
        else:
            self.uid = None

        if gid is not None:
            self.gid = getgrnam(gid)[2]
        else:
            self.gid = None

        def preexec_fn():
            if self.uid:
                os.setgid(self.uid)
            if self.gid:
                os.setuid(self.gid)

        self._worker = Popen(self.cmd.split(), cwd=self.wdir, shell=shell,
                             preexec_fn=preexec_fn)
        self.started = time.time()

    def poll(self):
        return self._worker.poll()

    def terminate(self):
        return self._worker.terminate()

    def age(self):
        return time.time() - self.started

    @property
    def pid(self):
        return self._worker.pid