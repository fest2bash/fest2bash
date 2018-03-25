#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.dont_write_bytecode = True

from pprint import pprint

from utils.format import pfmt, fmt
from base import BaseFest2Bash, join

class Fest2Bash(BaseFest2Bash):
    def __init__(self, manifest, reporoot='repos'):
        super(Fest2Bash, self).__init__(manifest, 'git')
        self.reporoot = reporoot
    @property
    def reponames(self):
        return self.manifest
    def generate_content(self):
        if_predicate = fmt('if hash {0} 2> /dev/null; then\n', self.program)
        else_clause = fmt('else\n    echo "missing {0}"\nfi', self.program)
        clone_github = 'git clone https://github.com'
        body = ['mkdir -p ' + self.reporoot]
        for reponame in self.reponames:
            repopath = os.path.join(self.reporoot, reponame)
            body += [fmt('[ -d "{repopath}" ] || {clone_github}/{reponame} {repopath}')]
            body += [fmt('(cd {repopath} && git pull && git checkout HEAD)')]
        return if_predicate + join(body, prefix='    ', sepby='\n', tail='\n') + else_clause
