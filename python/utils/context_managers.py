from contextlib import contextmanager
import tempfile as tf
import subprocess as sp
import os

import ROOT


ROOT.gROOT.SetBatch(True)

@contextmanager
def open_root(filename='', mode=''):
    """
    A context manager for ROOT TFiles. The syntax mimics the built-in open function.
    """
    open_modes = {
        'r': 'READ',
        'w': 'RECREATE',
        'a': 'UPDATE',
        'r+': 'UPDATE',
        'w+': 'RECREATE',
        'a+': 'UPDATE',
    }

    if mode in open_modes:
        mode = open_modes[mode]
    else:
        mode = 'READ'

    root_file = ROOT.TFile.Open(filename, mode)
    if not root_file:
        raise IOError('Failed to open {}.'.format(filename))

    try:
        ROOT.SetOwnership(root_file, True)
        yield root_file
    finally:
        root_file.Close()

@contextmanager
def gfalFS_mount(mount_path='', remote_url=''):
    """
    A context manager for temporary gfalFS mounts.
    """
    tmpdir = tf.mkdtemp(dir = mount_path)
    sp.check_call(['gfalFS', tmpdir, remote_url])

    try:
        if not os.path.ismount(tmpdir):
            raise RuntimeError('Failed to mount "{}". Please check your GRID proxy and the status of the remote file system.'.format(remote_url))
        yield tmpdir
    finally:
        sp.check_call(['gfalFS_umount', tmpdir])
        os.rmdir(tmpdir)

