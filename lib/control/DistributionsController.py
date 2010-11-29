'''
Created on Nov 22, 2010

@author: eschenal
'''
from control.ResourceController import ResourceController
from util import globals
import json
from control.DefaultController import ControllerException
from rest.Client import Client

class DistributionsController(ResourceController):

    _resource = "distributions"

    def __init__(self):
        super(DistributionsController, self ).__init__()
        
    def _update(self, args):
        options = globals.options
                  
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
                uuid = item.get("uuid")
        elif options.json:
            item = json.loads(options.json)
            uuid = item.get("uuid")
        else:
            raise ControllerException("Updating a distribution is not possible in interactive mode.")
        
        client = Client(self._endpoint(), options.username, options.password)
        result = client.update(self._resource + "/" + uuid, item)
        
        if options.raw:
            print json.dumps(result, sort_keys=True, indent=4)
        else:
            self._render(result)

    def _render(self, item, detailed=False):
        if not detailed:
            print item['uuid'], item['name']
        else: 
            print "Name:", item['name']
            if item.has_key('description'): print "Description:", item['description']
            print "UUID:", item['uuid']
            if item.has_key('url'): print "Url:", item['url']             
            if item.has_key('parameters'):
                print "Parameters:"
                for p in item.get('parameters'):
                    print "   ", p.get('key')

    def _resolv(self, path):
        options = globals.options
        client = Client(self._endpoint(), options.username, options.password)
        result = client.read("directory/distribution/" + path)
        if result.has_key('uuid') : return result['uuid']            