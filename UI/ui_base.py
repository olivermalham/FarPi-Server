""" Mockip UI definition file to try and work out how to build the system.

I want this to be as simple and intuitive as possible, whilst also being
powerful and easily extensible. It also needs to be pure python.

Themes is a directory holding a bunch of python packages.
ui is the GUI instance that the server is looking for. When converted to a
string it should output an HTML page with embedded hooks for the JavaScript
parts to interact with.

I like the relative elegance of nested function calls, as demoed below, 
for capturing the hierarchical structure of HTML.

The various GUI components will inherit from one of  a pair of base classes,
one for containers, the other for components.

All UI classes implement the __call__() method. Containers use *args to 
iterate through all children, simply outputting whatever they evaluate to 
when converted to strings, wrapped with a preamble and post-amble.

Components are simpler, and just return a fragment of HTML when called. Just
use simple .format() call with the **kwargs dictionary.

As well as outputting HTML, there should also be hooks for generating 
additional JavaScript and CSS for appending to the primary JS and CSS files.
By augmenting these static files rather than creating new ones it reduces the 
number of web requests that have to be made.

Example:
import themes.vanilla.*
ui = panel(
            row(
                horizontal_bar(value="bcm23", label="Temperature"),
                toggle_switch(value"bcm01", label="Fan")
                ),
            row(
                dial_meter(value="bcm12", label="Volts")
                )
               )
               
Javascript part. Basic updating of the UI with state values from the HAL
is dealt with by the basic FarPi framework. However, it is inevitable that
some components will want to run handlers when certain things happen. The
JS fragments will be collated and sent to the client, so can in theory do
anything JS can do. I should also provide hooks for code to run when the
state is updated. Given the JS frags will be run on load, there needs to be
a mechanism to register callbacks.


"""
from tornado.template import Template


class Container(object):
    """ Base class for FarPi UI generation.

    Designed to be used in a functional programming style. Concrete instances only need to define the
    HTML, JavaScript and CSS fragments as python string templates, with standard {param} placeholders.
    Returns HTML, JavaScript and CSS stylesheet strings for sending to the client.
    """

    # These should all be strings with {param} placeholders for the .format operator

    # Opening HTML fragment for the main container
    _prefix="""<div>\n"""

    # Closing HTML fragment for the main container
    _postfix="""\n</div>\n"""

    # HTML fragment added immediately before each child HTML section
    _child_prefix=""""""

    # HTML fragment added immediately after each child HTML section
    _child_postfix=""""""

    # Javascript template to provide extra functionality not available in the base code. Optional.
    _javascript = ""

    # CSS stylesheet template to provide extra styles if required. Option.
    _css = ""

    # Page template defines the page that will surround the GUI defined by the UI
    # objects. Should be a string. Topmost container must contain at least a {% raw far_pi %} tag.
    _page_template = """"""

    # Store the constructors keyword arguments for page template population
    _parameters = {}

    def __init__(self, *args, **kwargs):
        """ Wraps all child element HTML in it's own.
        All positional arguments are assumed to be Component subclasses.
        Keyword arguments are used to populate template parameters.

        :return (html, javascript, CSS) tuple of string
        """
        self.html_prefix = Template(self._prefix).generate(**kwargs)
        self.html_postfix = Template(self._postfix).generate(**kwargs)
        self.js = Template(self._javascript).generate(**kwargs)
        self.css = Template(self._css).generate(**kwargs)
        self.child_prefix = Template(self._child_prefix).generate(**kwargs)
        self.child_postfix = Template(self._child_postfix).generate(**kwargs)
        self._parameters = kwargs
        self._children = args

    def __call__(self):
        """ Wraps all child element HTML in it's own.

        :return (html, javascript, CSS) tuple of string
        """
        html = self.html_prefix
        js = self.js
        css = self.css
        
        for child in self._children:
            child_html, child_js, child_css = child()
            html += self.child_prefix + child_html + self.child_postfix
            js += child_js
            css += child_css
            
        html += self.html_postfix

        # If we have a page template defined, then process it and return as the HTML chunk
        if len(self._page_template) > 0:
            parameters = self._parameters
            parameters["far_pi"] = html
            html = Template(self._page_template).generate(**parameters)

        return html, js, css


class Component(object):
    """ Base class for FarPi UI components.
    """
    _html = """<some html>"""
    _js = """<some js>"""
    _css = """<some css>"""

    # Class counter, used to ensure JS callbacks have unique names
    _id = 0

    def __init__(self, *args, **kwargs):
        kwargs["_id"] = Component._id
        self.html = Template(self._html).generate(**kwargs)
        self.js = Template(self._js).generate(**kwargs)
        self.css = Template(self._css).generate(**kwargs)
        Component._id += 1

    def __call__(self, *args, **kwargs):
        return self.html, self.js, self.css
