
import sys
import yaml, json
from itertools import chain

import mistune
from jinja2 import Template

import argparse

class Node(object):
    def __init__( self, ident, name, yaml_tree ):
        self._name = name
        self._ident = "node%d" % ident

        self._nodes = [ type(self)(ident+i+1, name, vals) for i, (name, vals) in enumerate( yaml_tree.iteritems() ) ]

        super(Node, self).__init__()

    def render( self ):
        out = dict()
        out['id'] = self._ident
        out['name'] = self._name
        
        return out

    def __getitem__(self, key):
        if self._name == key:
            return self

        for leave in self:
            if leave._name == key:
                return leave

        raise KeyError()

    def __iter__(self):
        def gen():
            yield self
            for node in self._nodes:
                for leave in node:
                    yield leave

        return gen()

class Scene(Node):
    def __init__( self, ident, name, yaml_tree ):
        self._content = yaml_tree.pop('content', "")

        link_dict = self._link_dict = dict()

        class FabulaRenderer( mistune.Renderer ):
            def link(self, link, title, text):
                next_id = len(link_dict)
                link_ident = "link%d_%d" % (ident, next_id)
                link_dict[link_ident] = ( name, link )

                return '<a id="%s" class="flink" href="#">%s</a>' % (link_ident, text)

        self._renderer = FabulaRenderer()

        super(Scene, self).__init__(ident, name, yaml_tree)
    
    @property
    def visible(self):
        return self._content != ""

    def render( self ):
        md = mistune.Markdown(renderer=self._renderer)
        html_scene = md(self._content)

        out = super(Scene, self).render()
        out['content'] = html_scene

        return out

def FabulaTree(yaml_tree):
    return Scene( 0, "root", yaml_tree )

def main():
    frame_file = "frame.html"

    parser = argparse.ArgumentParser(description='Render a story as html5.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')

    args = parser.parse_args()

    syu_in_file = args.input
    html_out_file = args.output

    with open(syu_in_file, "r") as i:
        yaml_tree = yaml.load( i.read() )

    fabulaTree = FabulaTree( yaml_tree )
    scenes_contexts = [ leave.render() for leave in fabulaTree if leave.visible ]

    link_dict = dict(sum( (list(leave._link_dict.items()) for leave in fabulaTree), [] ))

    links_info = { i : {  "src" : fabulaTree[src]._ident, 
                          "tgt" : fabulaTree[tgt]._ident}
                  for i,(src,tgt) in link_dict.iteritems() }
    links_json = json.dumps(links_info)

    with open(frame_file, "r") as i:
        template = Template(i.read())

    with open(html_out_file, "w") as o:
        o.write(template.render(scenes=scenes_contexts,links=links_json))

if __name__ == "__main__":
    main()
