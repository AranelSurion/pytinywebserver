#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pytinywebserver by Yekta Leblebici <yekta@iamyekta.com>

# Imports
import signal
import logging
import sys

import core.config
import core.server


# Signal handler
def handle_sigint(signum, frame):
    print("Exiting now.")
    logging.warning("Got SIGINT, Exiting now.")
    sys.exit(1)


# Logging
logging.basicConfig(filename=core.config.PATH_LOGS + '/server.log',
                    level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


# Execution
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_sigint)
    server = core.server.Server()
