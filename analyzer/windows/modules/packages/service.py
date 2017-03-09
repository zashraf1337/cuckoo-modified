# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import shutil
import sys

from lib.common.abstracts import Package
import logging
from lib.common.defines import ADVAPI32
import traceback

log = logging.getLogger(__name__)

class Service(Package):
    """Service analysis package."""

    def start(self, path):
      PATHS = [
		("SystemRoot", "system32", "sc.exe"),
      ]

      try:
        sc = self.get_path("sc.exe")
        servicename = self.options.get("servicename", "zOOmService")
        servicedesc = self.options.get("servicedesc", "zOOmService (inc.)")
        arguments = self.options.get("arguments")



	sc_handle = ADVAPI32.OpenSCManagerA(None, None, 0x0001)
	serv_handle = ADVAPI32.OpenServiceA(sc_handle, servicename, 0x0005)


        binPath = "\"{0}\"".format(path)
        if arguments:
            binPath += " {0}".format(arguments)
	
	serv_handle = ADVAPI32.CreateServiceA(
		sc_handle,
		servicename,
		servicedesc,
		0x000F003F,    # SERVICE_ALL_ACCESS,
		0x00000010, # SERVICE_WIN32_OWN_PROCESS,
		0x00000002, # SERVICE_AUTO_START,
		0x00000001, # SERVICE_ERROR_NORMAL,
                binPath, None, None, None, None, None)
    	ADVAPI32.CloseServiceHandle(sc_handle)
        return self.execute(sc, "start", servicename, arguments)


      except Exception as e:
        log.info(sys.exc_info()[0])  
        log.info(e)
        log.info(e.__dict__)  
        log.info(e.__class__)  
        log.exception(e)
