#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version_info[:1] < (3,):
        print("This software does not work on versions older than Python 3.")
        sys.exit(1)

__version__ = "1.0.0"
