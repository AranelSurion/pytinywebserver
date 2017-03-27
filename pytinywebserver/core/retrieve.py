#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import errno
import logging
import os.path

import core.config
from core.utils import response_code, get_date, gen_error_page


def parse_request(request):
    """
    Takes <bytes>, converts to <string>.
    Then parses it and returns request fields as a <dict>.

    Returns False on bad requests.

    :param request: bytes of HTTP request.
    :returns: dictionary of HTTP request fields or False if cannot be parsed.

    """

    try:
        request = request.decode("utf-8")
        fields = {}

        # Example: GET / HTTP/1.1
        fields['_method'], fields['_uri'], fields['_protocol'], *remainder = request.split(None, 3)

        # Parse remaining request fields.
        for item in remainder[0].split("\r\n"):
            split = item.split(":", 1)
            if split[0]:
                fields[split[0]] = split[1].strip()
        return fields
    except:
        # Bad Request
        return False


class Response(object):
    """
    Takes a "request". (dict of HTTP request fields, see: parse_request())

    Response object has these attributes, availability depending on the method requested:
    response_fields: dictionary,  of HTTP response fields.
    response: string, HTTP response code. number + name.
    message_body: string, HTTP message body.

    :param request: dictionary, HTTP request fields, see: parse_request()
    """

    def __init__(self, request):
        self.response_fields = {}
        self.response_fields['Date'] = get_date()

        if request is False:
            # That means parser failed, most likely a Bad Request.
            self.response = response_code(400)
            self.message_body = gen_error_page(400)

        elif request['_method'] == "HEAD":
            resource = Resource(request['_uri'], get=False)
            self.response = resource.response

            if hasattr(resource, "last_modified"):
                self.response_fields['Last-Modified'] = resource.last_modified

        elif request['_method'] == "GET":
            resource = Resource(request['_uri'], get=True)
            self.response = resource.response

            if hasattr(resource, "last_modified"):
                self.response_fields['Last-Modified'] = resource.last_modified

            if hasattr(resource, "message_body"):
                self.message_body = resource.message_body

        elif request['_method'] == "POST":
            # TODO Implement this.
            self.response = response_code(501)
            self.message_body = gen_error_page(501)

        else:
            # Method Not Allowed
            self.response = response_code(405)
            self.message_body = gen_error_page(405)


def make_sendbuf(Response):
    """
    Takes a Response object.
    Returns a buffer of the complete HTTP response, as bytes.

    :param Response: a Response object.
    :returns: bytes, a complete HTTP response.

    """

    buf = "HTTP/1.1 %s\r\n" % (Response.response)

    for field in Response.response_fields:
        buf += "%s: %s\r\n" % (field, Response.response_fields[field])

    buf += "Server: pytinywebserver\r\n\r\n"

    # Now encode the buffer to bytes.
    buf = buf.encode("utf-8")
    if hasattr(Response, "message_body"):
        buf += Response.message_body

    return buf


class Resource(object):
    """
    Takes the file name requested, and information about HTTP method used.

    Response object attributes:
    response: string, number + name of the response code returned.
    message_body: bytes, file contents on success, an error page on failure.
    last_modified: string, time of last modification. Available only on success.

    :param fname: string, File name requested by the visitor.
    :param get: bool, True if HTTP method is GET, False otherwise.

    """

    def __init__(self, fname, get):
        """
        Sets the absolute path and iterates over index files in directories.

        """

        absolute_path = "%s%s" % (core.config.PATH_WWW, fname.rstrip("/"))

        if os.path.isdir(absolute_path) is True:  # IF directory or wwwroot
            for item in core.config.INDEX_FNAMES:
                # Iterate over possible index files.
                absolute_path_item = "%s/%s" % (absolute_path, item)
                self.retrieve(absolute_path_item, get)
                if self.response == response_code(200):
                    # Found one.
                    break

        else:  # It is not a directory
            self.retrieve(absolute_path, get)

    def retrieve(self, absolute_path, get):
        """
        Takes two parameters, opens the resource for retrieval.
        Sets response, message_body, last_modified attributes of the object.

        :param absolute_path: string, absolute path of a file.
        :param get: bool, True if HTTP method is GET, False otherwise.
        """
        try:
            f = open(absolute_path, "rb")
        except IOError as e:

            if e.errno == errno.ENOENT:  # 404
                self.response = response_code(404)
                self.message_body = gen_error_page(404)

            elif e.errno == errno.EPERM or e.errno == errno.EACCES:  # 403
                self.response = response_code(403)
                self.message_body = gen_error_page(403)

            else:  # 500
                logging.warning("An unexpected errno %i was returned on retrieve() operation.") % (e.errno)
                self.response = response_code(500)
                self.message_body = gen_error_page(500)

        else:
            self.response = response_code(200)

            # Last-modified time and formatting
            last_modified = os.path.getmtime(f.fileno())
            self.last_modified = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                               time.localtime(last_modified))
            # If this is a GET method:
            if get is True:
                self.message_body = f.read()

            f.close()
