
Fabulation
==========

Fabulation is a simple tool to narrate a story in a non-linear fashion. You can write a set of 'scenes' and jump from scene to scene using links. Each scene can be decorated with audio or pictures. 

Fabulation generates a html-file that you can access via browser and publish on the internet. 

Requirements:
============

fabulation needs:
-   python3 (maybe 2 also works?)
-   pyyaml
-   jinja2
-   mistune

Howto:
======

See example.yml how to write a fabulation input file.

Call

    python fabulation.py input.yml output.html

to use fabulation. The output.html uses jQuery and HowlerJS for sound.
