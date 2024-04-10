
# Author: Michael Borinsky
# Github: https://github.com/michibo/fabulation

import sys
import yaml, json
from itertools import chain

import mistune
from jinja2 import Template

import argparse

class WrongLink(Exception):
    pass

class Text(object):
    def __init__( self, data ):
        self._content = data.pop('content', "")
        self._next = data.pop('next', "")

    def render( self, name, nodes ):
        link_dict = dict()
        back_link_dict = dict()

        def add_link(link):
            if link.startswith("BACK"):
                next_id = len(back_link_dict)
                link_ident = "b%s_%d" % (nodes[name]._ident, next_id)
                try:
                    back_link_dict[link_ident] = int(link[4:])
                except ValueError:
                    raise WrongLink("Cannot parse BACK-link \"%s\" in scene \"%s\"" % (link, name))
            else:
                next_id = len(link_dict)
                link_ident = "l%s_%d" % (nodes[name]._ident, next_id)
                try:
                    link_dict[link_ident] = nodes[link]._ident
                except KeyError:
                    raise WrongLink("Cannot find scene \"%s\" referenced in scene \"%s\"" % (link, name))
        

            return link_ident
        
        class Renderer( mistune.HTMLRenderer ):
            def link(self, text, url, title=None):
                link_ident = add_link(url)

                return '<span id="%s" class="fl">%s</span>' % (link_ident, text)

        md = mistune.Markdown(renderer=Renderer())
        html_scene = md(self._content)
        
        view = dict()
        view['content'] = html_scene

        meta = dict()
        if link_dict:
            meta['links'] = link_dict
        if back_link_dict:
            meta['backlinks'] = back_link_dict

        if self._next and (link_dict or back_link_dict):
            print("Warning: next-link %s together with links or backlinks set in scene %s. If there is only one link/backlink, next will be set automatically! Links/Backlinks are ignored." % (self._next, name))

        if self._next:
            if self._next.startswith("BACK"):
                try:
                    meta['bnxt'] = int(self._next[4:])
                except ValueError:
                    raise WrongLink("Cannot parse back-next-link \"%s\" in scene \"%s\"" % (self._next, name))

            else:
                try:
                    meta['nxt'] = "%s" % nodes[self._next]._ident
                except KeyError:
                    raise WrongLink("Cannot parse next-link \"%s\" in scene \"%s\"" % (self._next, name))
        #else:
        #    if len(link_dict) + len(back_link_dict) == 1:
        #        for _, tgt in link_dict.items():
        #            meta['nxt'] = tgt
        #
        #        for _, n in back_link_dict.items():
        #            meta['bnxt'] = n

        return view, meta

class Pic(object):
    def __init__( self, data ):
        self._pic = data.pop('pic', "")
        self._fullpic = data.pop('fullpic', "")

    def render( self, name, nodes ):
        meta = dict()
        if self._pic:
            meta['pic'] = "%s" % self._pic

        if self._fullpic:
            meta['fullpic'] = "%s" % self._fullpic

        return dict(), meta

class Audio(object):
    def __init__( self, data ):
        self._audio = data.pop('audio', "")
        self._stop = True if 'stopaudio' in data else False

    def render( self, name, nodes ):
        meta = dict()

        if self._audio:
            meta['audio'] = "%s" % self._audio

        if self._stop:
            meta['stopaudio'] = self._stop

        return dict(), meta

class Video(object):
    def __init__( self, data ):
        self._video = data.pop('video', "")


    def render( self, name, nodes ):
        meta = dict()
        meta['video'] = self._video

        return dict(), meta

class Node(object):
    def __init__( self, ident, data, Features ):
        self._ident = "n%d" % ident

        if not isinstance(data, dict):
            data = { "content" : data }

        self._features = [ feature(data) for feature in Features ]

    def render( self, name, nodes ):
        view = dict()
        view['id'] = self._ident
        
        meta = dict()

        for feature in self._features:
            v, m = feature.render( name, nodes)
            view.update( v )
            meta.update( m )

        return view, meta


class Event(object):
    def __init__( self, data ):
        self._enter_event = data.pop('onEntrance',"")
        self._exit_event = data.pop('onExit',"")

    def render( self, name, nodes ):
        meta = dict()
        if self._enter_event:
            meta['enter'] = "%s" % self._enter_event

        if self._exit_event:
            meta['exit'] = "%s" % self._exit_event

        return dict(), meta


def main():
    frame_file = "frame.html"

    parser = argparse.ArgumentParser(description='Render a story as html5.')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')

    args = parser.parse_args()

    syu_in_file = args.input
    html_out_file = args.output

    with open(syu_in_file, "r") as i:
        yaml_dict = yaml.load( i.read(), Loader=yaml.SafeLoader)

    nodes = { name : Node( i, data, [ Text, Pic, Audio, Event ] ) for i,(name,data) in enumerate(yaml_dict.items()) }

    info = { node._ident : node.render( name, nodes ) for name, node in nodes.items() }
    view = [ v for i,(v,m) in info.items() ]
    meta = { i : m for i,(v,m) in info.items() }

    root = nodes['root']._ident

    js_meta = json.dumps(meta)

    with open(frame_file, "r") as i:
        template = Template(i.read())

    with open(html_out_file, "w") as o:
        o.write(template.render(contexts=view,meta=js_meta,root=root))

if __name__ == "__main__":
    main()
