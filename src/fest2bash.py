#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import imp
import sys
import operator
sys.dont_write_bytecode = True

from utils.format import pfmt, fmt
from ruamel import yaml

MODNAMES = [
    'ppa',
    'apt',
    'dnf'
    'pip2',
    'pip3',
    'github',
]

class ManifestIsNone(Exception):
    pass

class ManifestIsUnknown(Exception):
    pass

class UnknownModule(Exception):
    def __init__(self, modname):
        msg = fmt('unknown module: {modname}')
        super(UnknownModule, self).__init__(msg)

def _get_ordered(modnames):
    return list(set(MODNAMES).union(modnames)) + list(set(modnames) - set(MODNAMES))

def _load_yaml_json_or_file(obj):
    if os.path.isfile(obj):
        obj = open(obj).read().strip().encode('utf-8')
    try:
        obj = yaml.safe_load(obj)
    except Exception as ex:
        print(ex)
        raise ex
    return obj

def _move_pkg_to_apt_and_dnf(manifest_map):
    pkgs = manifest_map.pop('pkg', None)
    if pkgs:
        for modname in ('apt', 'dnf'):
            manifest_map[modname] += manifest_map.get(modname, []) + pkgs
    return manifest_map

def _load_manifest(manifest):
    if manifest is None:
        raise ManifestIsNone
    elif isinstance(manifest, dict) or isinstance(manifest, list):
        pass
    elif isinstance(manifest, str):
        manifest = _load_yaml_json_or_file(manifest)
    return _move_pkg_to_apt_and_dnf(manifest)

def _load_modules(modpath='modules'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), modpath))
    pyfiles = [f for f in os.listdir(modpath) if f.endswith('.py') and f != 'base.py']
    return {f[0:-3]: imp.load_source(f[0:-3], modpath+'/'+f) for f in pyfiles}

def fest2bash(manifest):
    manifest_map = _load_manifest(manifest)
    modules_map = _load_modules()
    for modname in _get_ordered(manifest_map.keys()):
        if modname in modules_map:
            manifest = modules_map[modname]
            try:
                module = modules_map[modname]
            except KeyError:
                raise UnknownModule(modname)
            fragment = module.Fest2Bash(manifest).generate()
            print(fragment)

    for modname, manifest in manifest_map.items():
        try:
            module = modules_map[modname]
        except KeyError:
            raise UnknownModule(modname)
        fragment = module.Fest2Bash(manifest).generate()
        print(fragment)
        #pfmt('fragment:\n{fragment}')

if __name__ == '__main__':
    bash = fest2bash('basic.yml')
