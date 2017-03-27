#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pytinywebserver by Yekta Leblebici <yekta@iamyekta.com>

import socket
import logging
import select

import core.config
import core.retrieve
from core.retrieve import make_sendbuf

logger = logging.getLogger(__name__)


class Server(object):
    """
    Binds to a port, then polls for connections and calls necessary functions on its main loop.

    This object does not take any parameters and does not have any attributes.
    """

    def __init__(self):
        logger.info("Server is initializing.")
        sock = self.listen()

        # Register to epoll events. Level-triggered mode.
        epoll = select.epoll()
        epoll.register(sock.fileno(), select.EPOLLIN)

        connections = {}
        while True:
            events = epoll.poll(1)
            for fd, event in events:
                if fd == sock.fileno():
                    # An event happened on our socket file descriptor.
                    conn, address = sock.accept()
                    conn.setblocking(0)
                    epoll.register(conn.fileno(), select.EPOLLIN)
                    connections[conn.fileno()] = {'connection': conn,
                                                  'request': b'',
                                                  'response': b'',
                                                  'peername': conn.getpeername()
                                                  }

                # Incoming
                elif event == select.EPOLLIN or event == select.EPOLLPRI:
                    try:
                        connections[fd]['request'] += connections[fd]['connection'].recv(1024)
                    except BlockingIOError:
                        pass

                    # If request seems to be ending:
                    if b'\n\n' in connections[fd]['request'] or b'\n\r\n' in connections[fd]['request']:
                        # Parse the request, and make a response.
                        fields_dict = core.retrieve.parse_request(connections[fd]['request'])
                        Response = core.retrieve.Response(fields_dict)

                        # Logging
                        remote_ip_addr = connections[fd]['peername']
                        uri = ""
                        method = ""

                        if fields_dict is not False:
                            if '_uri' in fields_dict.keys():
                                uri = fields_dict['_uri']
                            if '_method' in fields_dict.keys():
                                method = fields_dict['_method']

                        logger.info("%s: %s %s - %s" % (remote_ip_addr, method, uri, Response.response))
                        
                        # Write buffer to response key.
                        connections[fd]['response'] = make_sendbuf(Response)
                        epoll.modify(fd, select.EPOLLOUT)

                # Outgoing
                elif event == select.EPOLLOUT:
                    # Start sending the buffered response.
                    bytes_written = connections[fd]['connection'].send(connections[fd]['response'])
                    connections[fd]['response'] = connections[fd]['response'][bytes_written:]
                    if len(connections[fd]['response']) == 0:  # All sent.
                            epoll.modify(fd, 0)
                            connections[fd]['connection'].close()

                # Hang-up
                elif event == select.EPOLLHUP:
                    epoll.unregister(fd)
                    connections[fd]['connection'].close()
                    del connections[fd]

    def listen(self):
        """
        Creates a new socket and binds to it, in a non-blocking way.
        Returns a socket object.

        :returns: socket object.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((core.config.LISTEN_HOST, core.config.LISTEN_PORT))
            sock.listen(50)
            sock.setblocking(0)
        except:
            logger.critical("Could not bind to port :%i" %
                            (core.config.LISTEN_PORT))
            raise IOError("Could not bind to port :%i" %
                          (core.config.LISTEN_PORT))

        logger.info("Now listening to port :%i" % (core.config.LISTEN_PORT))
        return sock
