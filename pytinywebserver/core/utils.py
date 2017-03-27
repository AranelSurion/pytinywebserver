#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def response_code(code):
    """
    Takes a HTTP response code, returns its full name.

    :param code: integer HTTP response code.
    :returns: string, code + its full name.

    """

    response_codes = {
            100: "Continue",
            101: "Switching Protocols",
            102: "Processing",
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            207: "Multi-Status",
            208: "Already Reported",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            307: "Temporary Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Request Entity Too Large",
            414: "Request-URI Too Long",
            415: "Unsupported Media Type",
            416: "Requested Range Not Satisfiable",
            417: "Expectation Failed",
            418: "I'm a teapot",
            422: "Unprocessable Entity",
            423: "Locked",
            424: "Failed Dependency",
            426: "Upgrade Required",
            428: "Precondition Required",
            429: "Too Many Requests",
            431: "Request Header Fields Too Large",
            444: "No Response",
            451: "Unavailable For Legal Reasons",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported",
            507: "Insufficient Storage",
            508: "Loop Detected",
            510: "Not Extended",
            511: "Network Authentication Required",
            }

    return "%i %s" % (code, response_codes[code])


def get_date():
    """
    Returns HTTP-compatible datetime string.

    :returns: string, HTTP-compatible datetime.

    """

    return time.strftime("%a, %d %b %Y %H:%M:%S GMT")


def gen_error_page(code):
    """
    Takes a response code, generates a simple HTML error page.

    :param code: integer, response code.
    :returns: bytes, an error page.

    """

    page = ("<div align=\"center\">\r\n"
            "    <h1>%s</h1>\r\n"
            "    <br>\r\n"
            "    <hr>\r\n"
            "    <i>pytinywebserver</i>\r\n"
            "</div>") % (response_code(code))

    # Encode it to bytes.
    page = page.encode("utf-8")

    return page
