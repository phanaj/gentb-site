#!/usr/bin/env python
"""Process all available"""

import os
import sys
import fnmatch
import atexit

from datetime import datetime
from subprocess import Popen

DIR = os.path.abspath(os.path.dirname(__file__))
ANNO = os.path.join(DIR, 'flatAnnotatorVAR_2.0.pl')
DATA = os.path.abspath(os.path.join(DIR, '..', 'data', 'media', 'pipeline', 'files'))
FASTA = os.path.join(DATA, 'h37rv.fasta')
CODING = os.path.join(DATA, 'h37rv_genome_summary.txt')
NONCODING = os.path.join(DATA, 'h37rv_noncoding_summary.txt')

def module(*_):
    """This is a cover for the module below"""
    raise IOError("Failed to load lmod's python environment file.")

def prepare_lmod():
    """Is there's an lmod, set it up"""
    if 'MODULESHOME' in os.environ:
        for ifile in ('python.py', 'env_modules_python.py'):
            ifile = os.path.join(os.environ['MODULESHOME'], 'init', ifile)
            if os.path.isfile(ifile):
                with open(ifile, 'r') as fhl:
                    exec(fhl.read()) # pylint: disable=exec-used
                break
        module('load', 'gcc')
        module('load', 'perl')

def lock_dir(path):
    """Prevent this command from running more than once"""
    lock_file = os.path.join(path, '.import.lock')
    if os.path.isfile(lock_file):
        sys.stderr.write("Importer is locked: {}\n".format(lock_file))
        sys.exit(5)

    def unlock():
        """Remove the lock file on request"""
        if os.path.isfile(lock_file):
            os.unlink(lock_file)

    atexit.register(unlock)
    with open(lock_file, 'w') as fhl:
        fhl.write(str(datetime.now()))

def annotate(vcf_file):
    """Attempt to annotate the given file"""
    var_file = vcf_file[:-4] + '.var'
    if os.path.isfile(var_file):
        return # var file already exists, ignore

    with open(var_file, 'wb') as fhl:
        Popen(['perl', ANNO, FASTA, CODING, NONCODING, vcf_file, '15', '0.1', 'PASS'], stdout=fhl)

if __name__ == '__main__':
    if not os.path.isfile(ANNO):
        sys.stderr.write("Can't find annotator program! {}\n".format(ANNO))
        sys.exit(1)
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.stderr.write("You must provide a directory to parse for vcf files.\n")
        sys.exit(2)

    for fname in (FASTA, CODING, NONCODING):
        if not os.path.isfile(fname):
            sys.stderr.write("Can't find data file: {}\n".format(fname))
            sys.exit(3)

    lock_dir(sys.argv[1])

    prepare_lmod()

    for root, dirnames, filenames in os.walk(sys.argv[1]):
        for filename in fnmatch.filter(filenames, '*.vcf'):
            annotate(os.path.join(root, filename))
