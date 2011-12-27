# control.resource - Generic controller for managing cortex resources.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

import json, os

from cortex_client.config import Config
from cortex_client.control.abstract import AbstractController
from cortex_client.util import globals, prompt
from cortex_client.util.editor import edit_text


class ResourceController(AbstractController):

    def __init__(self):
        super(ResourceController, self).__init__()
        self._register(["list"], self._list, self._print_collection_completions)
        self._register(["show"], self._show, self._print_resource_completions)
        self._register(["add"], self._add, self._print_collection_completions)
        self._register(["update"], self._update, self._print_resource_completions)
        self._register(["delete"], self._delete, self._print_resource_completions)
        self._register(["help"], self._help)
        self._default_action = self._help

    def _print_list_completions(self, param_num, argv):
        pass

    def _list(self, argv):
        resources_list = self._get_resources(argv)
        if(len(resources_list) == 0):
            print "No resources to list"
        else:
            for r in resources_list:
                print r.get_identifier()

    def _print_identifiers(self, collection):
        self._print_resource_identifiers(collection.get_resources())

    def _print_collection_completions(self, param_num, argv):
        pass

    def _print_resource_completions(self, param_num, argv):
        pass

    def _show(self, argv):
        res = self._get_resource(argv)

        # Display the result
        options = globals.options
        if options.raw:
            res.show(as_json = True)
        else:
            res.show()

    def _complete_template(self, argv, template_json):
        pass

    def _add(self, argv):
        options = globals.options

        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        else :
            template_json = json.load(open(os.path.join(Config().templates_path, self._template)))
            #template = "# To abort the request; just exit your editor without saving this file.\n\n" + template
            self._complete_template(argv, template_json)
            updated = edit_text(json.dumps(template_json, indent = 4))
            #updated = re.sub(r'#.*$', "", updated)
            item = json.loads(updated)

        res = self.get_collection(argv)._new_resource(item)
        res.create()
        res.show(as_json = options.raw)

    def _update(self, argv):
        # First, get resource
        res = self._get_resource(argv)

        options = globals.options
        if options.filename:
            with open(options.filename, 'r') as f:
                item = json.load(f)
        elif options.json:
            item = json.loads(options.json)
        elif len(argv) > 0:
            # Edit the resource
            original = json.dumps(res.get_json(), sort_keys = True, indent = 4)
            #original = "# To abort the request; just exit your editor without saving this file.\n\n" + original
            updated = edit_text(original)
            #updated = re.sub(r'#.*$', "", updated)
            item = json.loads(updated)

        # Check if name has changed
        new_name = item["name"]
        res.rename(new_name)

        # Update resource
        res.set_json(item)
        res.commit(options.force)
        res.show(as_json = options.raw)

    def _delete(self, argv):
        res = self._get_resource(argv)
        if (prompt.confirm(prompt = "Delete " + res.get_name() + " ?", resp = False)) :
            res.delete()

    def _help(self, argv):
        print "Oops, this piece is missing some documentation"

    def _get_resource(self, argv):
        return self.get_collection(argv).get_resource(self._get_name_argument(argv))

    def _get_resources(self, argv):
        return self.get_collection(argv).get_resources()

    def get_collection(self, argv):
        raise NotImplementedError
