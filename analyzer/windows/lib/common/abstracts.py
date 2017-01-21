# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import glob
import os


from lib.api.process import Process
from lib.api.utils import Utils
from lib.common.exceptions import CuckooPackageError

import logging
log = logging.getLogger(__name__)


class Package(object):
    """Base abstract analysis package."""
    PATHS = []

    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.config = config
        self.options = options
        self.pids = []

    def set_pids(self, pids):
        """Update list of monitored PIDs in the package context.
        @param pids: list of pids.
        """
        self.pids = pids

    def start(self):
        """Run analysis package.
        @raise NotImplementedError: this method is abstract.
        """
        raise NotImplementedError

    def check(self):
        """Check."""
        return True

    def enum_paths(self):
        """Enumerate available paths."""
        for path in self.PATHS:
            basedir = path[0]
            sys32 = False
            if len(path) > 1 and path[1].lower() == "system32":
                sys32 = True
            if basedir == "SystemRoot":
                if not sys32 or "PE32+" not in self.config.file_type:
                    yield os.path.join(os.getenv("SystemRoot"), *path[1:])
                elif sys32:
                    yield os.path.join(os.getenv("SystemRoot"), "sysnative", *path[2:])
            elif basedir == "ProgramFiles":
                if os.getenv("ProgramFiles(x86)"):
                    yield os.path.join(os.getenv("ProgramFiles(x86)"),
                                       *path[1:])
                yield os.path.join(os.getenv("ProgramFiles").replace(" (x86)", ""), *path[1:])
            elif basedir == "HomeDrive":
                # os.path.join() does not work well when giving just C:
                # instead of C:\\, so we manually add the backslash.
                homedrive = os.getenv("HomeDrive") + "\\"
                yield os.path.join(homedrive, *path[1:])
            else:
                yield os.path.join(*path)

    def get_path(self, application):
        """Search for the application in all available paths.
        @param application: application executable name
        @return: executable path
        """
        for path in self.enum_paths():
            log.info(" path %s" % path)
            if os.path.isfile(path):
                return path
        raise CuckooPackageError("Unable to find any %s executable." %
                                 application)

    def get_path_glob(self, application):
        """Search for the application in all available paths with glob support.
        @param application: application executable name
        @return: executable path
        """
        for path in self.enum_paths():
            for path in glob.iglob(path):
                if os.path.isfile(path):
                    return path


        raise CuckooPackageError("Unable to find any %s executable." %
                                 application)

    def get_path_app_in_path(self, application):
        """Search for the application in all available paths.
        @param application: application executable name
        @return: executable path
        """
        for path in self.enum_paths():
            if os.path.isfile(path):
                if application and application.lower() not in path.lower():
                    continue
                else:
                    return path

        raise CuckooPackageError("Unable to find any %s executable." %
                                 application)

    def execute(self, path, args, interest):
        """Starts an executable for analysis.
        @param path: executable path
        @param args: executable arguments
        @param interest: file of interest, passed to the cuckoomon config
        @return: process pid
        """
        dll = self.options.get("dll")
        free = self.options.get("free")
        gw = self.options.get("setgw", None)

        u = Utils()
        if gw:
            u.set_default_gw(gw)

        suspended = True
        if free:
            suspended = False
        kernel_analysis = self.options.get("kernel_analysis", False)
        
        if kernel_analysis != False:
            kernel_analysis = True

        p = Process()
        if not p.execute(path=path, args=args, suspended=suspended, kernel_analysis=kernel_analysis):
            raise CuckooPackageError("Unable to execute the initial process, "
                                     "analysis aborted.")

        if free:
            return None

        if not kernel_analysis:
            p.inject(dll, interest)
        p.resume()
        p.close()
        
        return p.pid

    def package_files(self):
        """A list of files to upload to host.
        The list should be a list of tuples (<path on guest>, <name of file in package_files folder>).
        (package_files is a folder that will be created in analysis folder). 
        """
        return None
    
    def finish(self):
        """Finish run.
        If specified to do so, this method dumps the memory of
        all running processes.
        """
        if self.options.get("procmemdump"):
            for pid in self.pids:
                p = Process(pid=pid)
                p.dump_memory()
        
        return True

class Auxiliary(object):
    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.options = options
        self.config = config

    def add_pid(self, pid):
        pass

    def del_pid(self, pid):
        pass
