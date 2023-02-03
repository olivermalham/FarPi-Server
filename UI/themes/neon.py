from .. import ui_base


class Panel(ui_base.Container):
    """ Basic control console.

    """
    # Opening HTML fragment for the main container
    _prefix = """<!-- Panel -->\n<div class="panel">\n"""

    # Closing HTML fragment for the main container
    _postfix = """</div> <!-- End Panel -->\n"""

    # HTML fragment added immediately before each child HTML section
    _child_prefix = """ """

    # HTML fragment added immediately after each child HTML section
    _child_postfix = """ """

    # Javascript template to provide extra functionality not available in the base code. Optional.
    _javascript = """ """

    # CSS stylesheet template to provide extra styles if required. Option.
    _css = ""

    # Page template defines the page that will surround the GUI defined by the UI
    # objects. Should be a string, will be run through the Python .format method
    # to replace {far_pi} with the generated control panel.
    _page_template = """
<!doctype html>
<html lang="en">

<head>
    <title>FarPi</title>
    <script src="/js/farpi.js"></script>
    <script src="/farpiGUI.js"></script>
    <link rel="stylesheet" href="/css/farpi.css">
    <link rel="stylesheet" href="/css/Abel.css">
    <link rel="stylesheet" href="/farpiGUI.css">
</head>
<body onload="FarPi.onLoad('farpi');">
<div class="HeartBeat" id="HeartBeat">- FarPi -</div>
<div id="title">- {{name}} -</div>
<hr />
<center>

{% raw far_pi %}

</center>
</body>
</html>
"""


class LED(ui_base.Component):
    _html = """
<div class="LED" id="LED_{{pin}}_{{_id}}">
    <span class="LED_indicator">&nbsp;</span>
    <span class="label">{{label}}</span>
</div>

"""

    _js = """
/* LED js */
console.log("LED {{pin}}_{{_id}} JS run");

FarPi.registerCallback(function(){
    let LED_element = document.getElementById("LED_{{pin}}_{{_id}}");
    if(FarPi.state["{{pin}}"].state){
        LED_element.classList.add("on_glow");
        LED_element.querySelectorAll(".LED_indicator")[0].classList.add("LED_on", "on_glow");
    } else {
        LED_element.classList.remove("on_glow");
        LED_element.querySelectorAll(".LED_indicator")[0].classList.remove("LED_on", "on_glow");
    }
});

"""


class ToggleSwitch(ui_base.Component):
    _html = """
<div class="LED interactive" id="Toggle_{{pin}}_{{_id}}" onclick="Toggle_{{pin}}_{{_id}}()">
    <span class="toggle_switch"><span class="toggle_indicator">&nbsp;</span></span>
    <span class="label">{{label}}</span>
</div>
"""

    _js = """
/* ToggleSwitch js */
console.log("ToggleSwitch {{pin}}_{{_id}} JS run");

function Toggle_{{pin}}_{{_id}} (){
    console.log("Toggle pin {{pin}}_{{_id}}");
    FarPi.action("{{action}}", '');
}

FarPi.registerCallback(function(){
    let switch_element = document.getElementById("Toggle_{{pin}}_{{_id}}");
    if(FarPi.state["{{pin}}"].state){
        switch_element.classList.add("on_glow");
        switch_element.querySelectorAll(".toggle_switch")[0].classList.add("toggle_switch_on", "on_glow");
        switch_element.querySelectorAll(".toggle_switch")[0].querySelectorAll(".toggle_indicator")[0].classList.add("toggle_on");
    } else {
        switch_element.classList.remove("on_glow");
        switch_element.querySelectorAll(".toggle_switch")[0].classList.remove("toggle_switch_on", "on_glow");
        switch_element.querySelectorAll(".toggle_switch")[0].querySelectorAll(".toggle_indicator")[0].classList.remove("toggle_on");
    }
});

"""


class PushButtonSwitch(ui_base.Component):
    _html = """
<div class="LED interactive" id="PushButton_{{pin}}_{{_id}}" onmousedown="ButtonDown_{{pin}}_{{_id}}()" onmouseup="ButtonUp_{{pin}}_{{_id}}()"
  ontouchstart="ButtonDown_{{pin}}_{{_id}}()" ontouchend="ButtonUp_{{pin}}_{{_id}}()" oncontextmenu="FarPi.trap_context()">
    <span class="LED_indicator">&nbsp;</span>
    <span class="label">{{label}}</span>
</div>
"""

    _js = """
/* PushButtonSwitch js */
console.log("PushbuttonSwitch {{pin}}_{{_id}} JS run");

function ButtonDown_{{pin}}_{{_id}} (){
    console.log("Button {{pin}} down");
    FarPi.action("{{pin}}.action_set", '"value":1');
}

function ButtonUp_{{pin}}_{{_id}} (){
    console.log("Button {{pin}} up");
    FarPi.action("{{pin}}.action_set", '"value":0');
}

FarPi.registerCallback(function(){
    let LED_element = document.getElementById("PushButton_{{pin}}_{{_id}}");
    if(FarPi.state["{{pin}}"].state){
        LED_element.classList.add("on_glow");
        LED_element.querySelectorAll(".LED_indicator")[0].classList.add("LED_on", "on_glow");
    } else {
        LED_element.classList.remove("on_glow");
        LED_element.querySelectorAll(".LED_indicator")[0].classList.remove("LED_on", "on_glow");
    }
});

"""


class LineGauge(ui_base.Component):
    _html = """
<div class="on_glow LineGauge" id="LineGauge_{{source}}_{{_id}}">
    <span class="LineGauge_indicator">
        <span class="LineGauge_bar">&nbsp;</span>
    </span>
    <span class="label">{{label}}</span>
</div>

"""

    _js = """
/* LineGauge js */
console.log("Line Gauge {{source}} JS run");

FarPi.registerCallback(function(){
    let gauge_element = document.getElementById("LineGauge_{{source}}_{{_id}}").querySelectorAll(".LineGauge_indicator")[0];
    let gauge_bar = gauge_element.querySelectorAll(".LineGauge_bar")[0];
    let gauge_max = gauge_element.clientWidth;
    let gauge_width = FarPi.state["{{source}}"].state * gauge_element.clientWidth;
    gauge_bar.style.width = gauge_width+"px";
});

"""


class Row(ui_base.Container):
    """ Basic row container.

    """
    # Opening HTML fragment for the main container
    _prefix = """\n<!-- Row -->\n<div class="row">\n"""

    # Closing HTML fragment for the main container
    _postfix = """\n</div> <!-- Row -->\n"""


class MessageBox(ui_base.Component):
    """ Simple textbox for displaying accumulated messages from the server

    """
    _html = """
    
<textarea readonly class="MessageBox" id="MessageBox_{{_id}}"></textarea>    
    
"""
    _js = """
/* MessageBox */

let MessageBoxBuffer_{{_id}};
FarPi.registerCallback(function(){
    let messageBox = document.getElementById("MessageBox_{{_id}}")
    if(FarPi.state["message"].length > 0){
        messageBox.value = messageBox.value + FarPi.state["message"] + "\\n";
        messageBox.scrollTop = messageBox.scrollHeight;
    }
});
    
"""
