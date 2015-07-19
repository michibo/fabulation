
import sys
import yaml, json

import mistune
from jinja2 import Template

import argparse

class RenderManager:
    def __init__(self):
        self._link_dict = dict()

    def getRenderer(self, scene):
        link_dict = self._link_dict
        class FabulaRenderer( mistune.Renderer ):
            def link(self, link, title, text):
                next_id = len(link_dict)
                identifier = "link%d" % next_id
                link_dict[identifier] = ( scene, link )

                return '<a id="%s" class="flink" href="#">%s</a>' % (identifier, text)

        renderer = FabulaRenderer()
        md = mistune.Markdown( renderer=renderer )
        return md

class Scene:
    def __init__( self, identifier, name, content, **kwargs ):
        self._name = name
        self._content = content

        self._identifier = identifier

    def render( self, md ):
        html_scene = md.render(self._content)

        out = dict()
        out['id'] = self._identifier
        out['name'] = self._name
        out['content'] = html_scene

        return out

def getScenesFromYAML( raw_scenes ):
    return { name : Scene( "scene%d" % i, name, **attribs ) for i, (name, attribs) in enumerate(raw_scenes.iteritems()) }

def main():
    frame_file = "frame.html"

    parser = argparse.ArgumentParser(description='Render a story as html5.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')

    args = parser.parse_args()

    syu_in_file = args.input
    html_out_file = args.output

    with open(syu_in_file, "r") as i:
        yaml_scenes = yaml.load( i.read() )['scenes']

    scene_dict = getScenesFromYAML( yaml_scenes )
    renderManager = RenderManager()

    scenes_contexts = [ 
        scene.render(renderManager.getRenderer(name)) 
                    for name,scene in scene_dict.iteritems() ]

    link_dict = renderManager._link_dict

    links_info = { i : 
                       {  "src" : scene_dict[src]._identifier, 
                          "tgt" : scene_dict[tgt]._identifier }
                  for i,(src,tgt) in link_dict.iteritems() }
    links_json = json.dumps(links_info)

    with open(frame_file, "r") as i:
        template = Template(i.read())

    with open(html_out_file, "w") as o:
        o.write(template.render(scenes=scenes_contexts,links=links_json))

if __name__ == "__main__":
    main()
