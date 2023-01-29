#!/usr/bin/python

import sys
import importlib
import logging
import traceback
import json
import datetime

import tornado.ioloop
import tornado.web
import tornado.websocket

log = logging.getLogger(__name__)


class FarPiStateHandler(tornado.websocket.WebSocketHandler):
    """ Core of the FarPi system

    Handles and dispatches messages in-coming from the JS client. Also the kicking off point for refreshing the
    state vector and broadcasting it to all listeners.

    """
    clients = []

    def open(self):
        """ Called when ever a new websocket connection is opened.

        Send a copy of the HAL state as soon as the connection opens.
        :return:
        """
        print("WebSocket opened to IP {}".format(self.request.remote_ip))
        FarPiStateHandler.clients.append(self)
        self.write_message(application.hal.serialise())

    def on_message(self, message):
        """ Called when a websocket message is received by the server.

        Messages from FarPi clients are assumed to be RPC calls into the HAL.
        This is the kick-off point for dispatching that call.
        :param message: Websocket message contents
        :return:
        """
        global application

        if len(message) > 0:
            try:
                self.dispatch(message)
            except Exception as e:
                # TODO: Need to handle errors better than this
                print("Exception:{}".format(e))
                application.hal.error = f"An Error Occurred - {e}"
                self.broadcast_state()

    def on_close(self):
        """ Close a websocket connection. Removes the instance from the client list so updates
        are no longer sent.

        :return:
        """
        print("WebSocket closed")
        FarPiStateHandler.clients.remove(self)

    def check_origin(self, origin):
        """ Note that this is probably a secutiry risk - this over-ride allows any origin URL
        """
        return True

    def dispatch(self, message):
        """ Dispatch a FarPi RPC call into the HAL.

        Message is assumed to be a JSON encoded object with two elements: "action",
        and "parameters".
        "Action" is a string matching a HAL component method.
        "Parameters" is a dictionary that gets passed on as keyword arguments to the HAL
        component action method

        :param message: JSON
        :return: Nothing, but an immediate state update broadcast is sent upon completion
        """
        parsed_msg = json.loads(message)
        print(f"Packet received: {message}")
        print(f"Parsed message: {parsed_msg}")

        if "action" in parsed_msg.keys():
            method_name = parsed_msg["action"]
            method_parameters = parsed_msg["parameters"] if "parameters" in parsed_msg.keys() else {}
            application.hal.action(method_name, **method_parameters)
            self.broadcast_state()

    @classmethod
    def refresh(cls):
        """ Refresh the current state of the HAL and send an update to all clients
        :return: Nothing
        """
        application.hal.refresh()
        cls.broadcast_state()

    @classmethod
    def broadcast_state(cls):
        """ Send a serialised copy of the HAL to all currently open websockets

        :return: Nothing
        """
        for client in cls.clients:
            client.write_message(application.hal.serialise())


if __name__ == "__main__":
    # TODO: Need to implement proper logging
    print("-------------------")
    print(" FarPi Server v0.1")
    print("-------------------")
    time = datetime.datetime.now()
    print("Starting at",time.isoformat())

    if len(sys.argv) != 2:
        print("No application specified!")
        exit()

    # The name of the application package is passed on the command line.
    # This gets imported and must define various attributes (see base_app.py)
    app_name = sys.argv[1].split(".")[0] if "." in sys.argv[1] else sys.argv[1]

    print("Loading Application {}".format(app_name))
    try:
        application = importlib.import_module(app_name)

    except Exception:
        print("Error loading {}!".format(app_name))
        traceback.print_exc()
        exit()

    # TODO: Need a better way of configuring the URLs in the application package
    urls = [
        (r"/farpi", FarPiStateHandler),
        (r"/(.*)", tornado.web.StaticFileHandler,
         dict(path=application.settings['static_path'], default_filename='index.html')),
        ]

    # Create the Tornado application, start it listening on the configured port
    app = tornado.web.Application(urls, **application.settings)
    app.listen(application.port)

    # Create a periodic callback for refreshing the HAL and broadcasting it to all connected clients
    periodic = tornado.ioloop.PeriodicCallback(FarPiStateHandler.refresh, application.refresh_ms)
    periodic.start()
    print("Server starting on port {}...".format(application.port))

    try:
        # Kick off the Tornado processing loop
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        application.hal.clean_up()
