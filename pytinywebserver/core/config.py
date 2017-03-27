#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pytinywebserver by Yekta Leblebici <yekta@iamyekta.com>

# Imports
import os

# Full path of the files to serve. If empty, working directory will be used.
PATH_WWW = "/var/www"

# Full path to keep logs. If empty, working directory will be used.
PATH_LOGS = "/var/logs/pytinywebserver"

# Server host to listen on. Empty means all interfaces.
LISTEN_HOST = ""

# Port number to listen on. Default is 80.
# Cannot be empty.
LISTEN_PORT = 80

# Index file names to lookup for all directories, in the order of preference.
# Cannot be empty.
INDEX_FNAMES = ["index.htm", "index.html"]

# DO NOT CHANGE ANYTHING AFTER THIS LINE #
if not PATH_WWW:
    PATH_WWW = os.getcwd()

if not PATH_LOGS:
    PATH_LOGS = os.getcwd()

PATH_WWW = PATH_WWW.rstrip("/")
PATH_LOGS = PATH_LOGS.rstrip("/")
