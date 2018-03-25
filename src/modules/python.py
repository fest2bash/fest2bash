#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.dont_write_bytecode = True

from pprint import pprint

from base import BaseFest2Bash

class Fest2Bash(BaseFest2Bash):
    def __init__(self, manifest):
        super(Fest2Bash, self).__init__(manifest)
    def generate(self, *args, **kwargs):
        return self.manifest
