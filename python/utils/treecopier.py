import logging
import multiprocessing as mp
import os
import Queue
import re
import subprocess as sp

import ROOT

from context_managers import open_root, gfalFS_mount


ROOT.gROOT.SetBatch(True)

class TreeCopier(object):
    """
    Copy all files of a sample and merge them into a single file.

    Parameters
    ----------
    prep_in  : str
               The GRID storage location of the samples.
    prep_out : str
               The local output directory storing the copied .root files.
    sample   : str
               The sample subdirectory within the GRID storage location.
               e.g. V14/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8
    prefix   : str
               A prefix for the merged sample file name.
    cut      : str
               The sample selection cut.
    temp     : bool
               Flag whether the copies are temporary and should be removed
               after merging. The default is True.
    """
    def __init__(self, prep_in, prep_out, sample, prefix, cut, temp=True):

        logging.basicConfig(
            format = '%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n',
            datefmt = '%d-%b-%Y %H:%M:%S',
            level = logging.DEBUG
        )

        self.logger = logging.getLogger('TreeCopier')
       
        source = os.path.join(prep_in, sample)
        file_paths = self._check_files(prep_out, source)

        outdir = os.path.join(prep_out, sample)
        copy_paths = self._copy_files(file_paths, outdir, cut)

        merge_path = os.path.join(prep_out, prefix + sample + '.root')
        self._merge_files(copy_paths, merge_path)

        if temp:
            for copy_path in copy_paths:
                os.remove(copy_path)
            os.rmdir(outdir)

    def _check_files(self, mount_path, remote_url):

        self.logger.debug('Checking for .root files in "%s".', remote_url)

        # Substitute the protocol in front of the LFN's base path with
        # an xrootd redirector recognized by ROOT for remote file access.
        # Investigate TGFALFile syntax for use in ROOT 6.
        xrd_prefix = 'root://cms-xrd-global.cern.ch//'
        basepath = re.sub('.*(?=/store/)', xrd_prefix, remote_url)

        # Search the directory tree for .root files.
        file_paths = []

        with gfalFS_mount(mount_path, remote_url) as mount:
            for dirpath, dirnames, filenames in os.walk(mount):
                if filenames:
                    relpath = os.path.relpath(dirpath, mount)
                    file_paths.extend([
                        os.path.join(basepath, relpath, filename)
                        for filename in filenames if filename.endswith('.root')
                    ])

        if file_paths:
            self.logger.debug('Located %s .root files.', len(file_paths))
            return file_paths
        else:
            raise IOError('Unable to locate any .root files.')
        
    def _copy_files(self, file_paths, copy_dir, cut):
        """
        Copy files in parallel and return a list of successfully copied files.
        """
        self.logger.debug('Copying files to "%s".', copy_dir)
        self.logger.debug('The selection cut is "%s".', cut)

        # Safely create the output directory of the copied files.
        try:
            os.makedirs(copy_dir)
        except OSError:
            if not os.path.isdir(copy_dir):
                raise

        # Fill the task queue with tuples of paths to the file and copy, respectively.
        task_queue = mp.Queue()
        for file_path in file_paths:
            copy_path = os.path.join(copy_dir, os.path.basename(file_path))
            task_queue.put((file_path, copy_path))

        # Prepare a message queue to receive log messages.
        message_queue = mp.Queue()

        # Instantiate the file copy worker processes.
        workers = [
            mp.Process(target = self._copy_file_worker, args = (task_queue, message_queue, cut))
            for cpu in xrange(mp.cpu_count() - 2)
        ]

        # Instantiate and start the message listener process.
        listener = mp.Process(target = self._message_listener, args = (message_queue,))
        listener.start()

        # For each worker process, queue a sentinel value and start running.
        for worker in workers:
            task_queue.put(None)
            worker.start()

        # Ensure the calling process waits for the workers to terminate.
        for worker in workers:
            worker.join()

        # Ensure the calling process waits for the listener to terminate.
        message_queue.put(None)
        listener.join()

        return [os.path.join(copy_dir, filename) for filename in os.listdir(copy_dir)]

    def _copy_file_worker(self, task_queue, message_queue, cut):

        # Consume tasks from the queue until the sentinel value is received.
        for file_path, copy_path in iter(task_queue.get, None):
        
            with open_root(file_path, 'r') as infile, open_root(copy_path, 'w'):
                # Copy any objects present besides the tree.
                for key in infile.GetListOfKeys():
                    if key.GetName() == 'tree':
                        continue
                    obj = key.ReadObj()
                    obj.Write()
                # Copy the tree with the selection.
                intree = infile.Get('tree')
                outtree = intree.CopyTree(cut)
                n_in = intree.GetEntriesFast()
                n_out = outtree.GetEntriesFast()
                outtree.Write()

            message_queue.put_nowait('[PID {0!s}] Selected {1!s} out of {2!s} entries from "{3}".'.format(os.getpid(), n_out, n_in, file_path))

    def _message_listener(self, message_queue):
        while True:
            try:
                message = message_queue.get_nowait()
                if message is None:
                    break
                self.logger.info(message)
            except Queue.Empty:
                pass

    def _merge_files(self, file_paths, merge_path):

        self.logger.debug('Merging the files to "%s"', merge_path)

        # Set the first positional argument, isLocal, to false to prevent the
        # files to merge from being copied to a temporary directory, as they 
        # are already available locally. PyROOT doesn't support keyword args.
        merge_file = ROOT.TFileMerger(ROOT.kFALSE)
        merge_file.OutputFile(merge_path, 'RECREATE')
        for file_path in file_paths:
            merge_file.AddFile(file_path)
        merge_file.Merge()

