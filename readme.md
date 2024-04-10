fabulation
==========

[fabulation](//github.com/michibo/fabulation) is a simple tool to narrate a story in a non-linear fashion. In other words it can be used to create very simple text adventures. You can write a set of 'scenes' and jump from scene to scene using links. Each scene can be decorated with audio or pictures. 

Fabulation generates a html-file that you can access via browser and publish on the internet. 


Requirements:
============

To run **fabulation** a python3 installation is required. **fabulation** additionally requires
- [Mistune](//mistune.readthedocs.io/) as its Markdown implementation (mistune v3 is now required), 
- [Jinja2](//jinja.palletsprojects.com/) as a template engine and 
- [PyYAML](//pyyaml.org/) to read and write configuration files. 

The extra python packages can be installed for instance with *pip*

    pip install mistune jinja2 pyyaml

Howto:
======

See example.yml for an example on how to write a fabulation input file. The result is

[example.html](//htmlpreview.github.io/?https://github.com/michibo/fabulation/blob/master/example.html)

To generate an output (example.html) from an input (example.yml) file all

    python fabulation.py example.yml example.html

The output.html uses [jQuery](//jquery.com/) and [HowlerJS](//howlerjs.com/) for sounds.

A very eleborate example can be found here: http://tmtnslt.com/jonas/
