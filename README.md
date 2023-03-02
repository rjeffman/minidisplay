minidisplay
===========

minidisplay is a framework to render data in a SSD1306 OLED display. It's
being implemented so that information can be displayed using data plugins,
and a configuration file is used to describe the application behavior.

A simulator to test how data will be rendered is also available.

Current implementation works, but all structure is still in a very early
stage of development and will mot certainly change it the near future.


Installation
------------

To install minidisplay, download the repository, and install it with `pip`.
It is strongly suggested that you use a Python virtual environment.

To run the simulator, run the module with `-s`. You may try with the example
application.

```
git clone --depth 1 https://github.com/rjeffman/minidisplay
cd minidisplay
pip install .[simulator,examples]
cd examples
python -m minidisplay -s user_app.yaml
```

The main goal of this project is to use the SSD1306 OLED display with
some Raspberry-Pi boards. To run the example application using the actual
hardware, use:

```
cd minidisplay
pip install .[raspberry,examples]
cd examples
python -m minidisplay user_app.yaml
```

