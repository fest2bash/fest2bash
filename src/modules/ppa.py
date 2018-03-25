#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.dont_write_bytecode = True

from pprint import pprint
from utils.format import fmt, pfmt
from base import BasePackageFest2Bash

class Fest2Bash(BasePackageFest2Bash):
    def __init__(self, manifest):
        super(Fest2Bash, self).__init__(manifest, 'add-apt-repository', '-y')
