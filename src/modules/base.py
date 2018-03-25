#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.dont_write_bytecode = True

from pprint import pprint
from utils.format import fmt, pfmt

def join(items, head='', prefix='', sepby='\n', suffix='', tail=''):
    return head + sepby.join([prefix + item + suffix for item in items]) + tail

class GenerateGuardWithoutProgram(Exception):
    pass

class BaseFest2Bash(object):
    def __init__(self, manifest, program=None, sudo=True, guard=True):
        self.manifest = manifest
        self.program = program
        self.sudo = sudo
        self.guard = guard
    def generate_guard(self):
        if not hasattr(self, 'program'):
            raise GenerateGuardWithoutProgram
        program = self.program
        return fmt('! hash {program} 2> /dev/null && echo "missing {program}" || ')
    def generate_header(self, message=None):
        if message is None:
            message = fmt('echo "{0}:"', self.program)
        return message
    def generate_content(self):
        raise NotImplementedError('abstract class not implemented in base')
    def generate_footer(self, message='echo'):
        return message if message is not None else ''
    def generate(self):
        header = self.generate_header()
        content =  self.generate_content()
        footer = self.generate_footer()
        return fmt('{header}\n{content}\n{footer}\n')

class BasePackageFest2Bash(BaseFest2Bash):
    def __init__(self, manifest, program, default_args='', sudo=True, guard=True):
        super(BasePackageFest2Bash, self).__init__(manifest, program, sudo, guard)
        self.default_args = default_args
    @property
    def args(self):
        print('manifest =>', self.manifest)
        return [self.default_args] + sorted(list(set(self.manifest)))
    def generate_arguments(self, sepby=' \\\n    '):
        return join(self.args, head=' ', sepby=sepby) if self.args else ''
    def generate_content(self):
        guard = self.generate_guard() if self.guard else ''
        sudo = 'sudo ' if self.sudo else ''
        args = self.generate_arguments()
        return guard + sudo + self.program + args
