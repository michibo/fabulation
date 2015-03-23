
import sys
import yaml

import mistune
from jinja2 import Template

import argparse

class Scene:
    def __init__( self, name, content, **kwargs ):
        self.name = name
        self.content = content

    def render( self, md ):
        pass

def renderScenes( raw_scenes ):
    md = mistune.Markdown()

    def renderScene( name, attrib ):
        out = dict()

        content = attrib['content']
        html_scene = md.render(content)

        out['id'] = 0
        out['name'] = name
        out['content'] = html_scene

        return out

    return [ renderScene( *item ) for item in raw_scenes.iteritems() ] 

def main():
    frame_file = "frame.html"

    parser = argparse.ArgumentParser(description='Render a story as html5.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')

    args = parser.parse_args()

    syu_in_file = args.input
    html_out_file = args.output

    with open(syu_in_file, "r") as i:
        raw_scenes = yaml.load( i.read() )['scenes']

    scenes = renderScenes( raw_scenes )

    with open(frame_file, "r") as i:
        template = Template(i.read())

    with open(html_out_file, "w") as o:
        o.write(template.render(scenes=scenes))

if __name__ == "__main__":
    main()
