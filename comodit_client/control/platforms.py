# control.applications - Controller for comodit Applications entities.
# coding: utf-8
#
# Copyright 2010 Guardis SPRL, Liège, Belgium.
# Authors: Laurent Eschenauer <laurent.eschenauer@guardis.com>
#
# This software cannot be used and/or distributed without prior
# authorization from Guardis.

from __future__ import absolute_import
from __future__ import print_function

import json

from comodit_client.api.exporter import Export
from comodit_client.api.importer import Import
from comodit_client.control.doc import ActionDoc
from comodit_client.control.exceptions import ArgumentException
from comodit_client.control.files import PlatformFilesController
from comodit_client.control.organization_entity import OrganizationEntityController
from comodit_client.control.parameters import PlatformParametersController
from comodit_client.control.settings import PlatformSettingsController

from . import completions


class PlatformsController(OrganizationEntityController):

    _template = "platform.json"

    def __init__(self):
        super(PlatformsController, self).__init__()

        # subcontrollers
        self._register_subcontroller(["settings"], PlatformSettingsController())
        self._register_subcontroller(["files"], PlatformFilesController())
        self._register_subcontroller(["parameters"], PlatformParametersController())

        self._doc = "Platforms handling."

        # actions
        self._register(["import"], self._import, self._print_import_completions)
        self._register(["export"], self._export, self._print_export_completions)
        self._register(["images"], self._images, self._print_entity_completions)

        self._register_action_doc(self._export_doc())
        self._register_action_doc(self._import_doc())
        self._register_action_doc(self._images_doc())

    def _get_collection(self, org_name):
        return self._client.platforms(org_name)

    def _prune_json_update(self, json_wrapper):
        super(PlatformsController, self)._prune_json_update(json_wrapper)
        json_wrapper._del_field("organization")
        json_wrapper._del_field("settings")
        json_wrapper._del_field("files")
        json_wrapper._del_field("parameters")

    # Export

    def _print_export_completions(self, param_num, argv):
        if param_num < 2:
            self._print_entity_completions(param_num, argv)
        elif param_num == 2:
            completions.print_dir_completions()

    def _export(self, argv):
        self._options = self._config.options

        plat = self._get_entity(argv)

        root_folder = plat.name
        if len(argv) > 2:
            root_folder = argv[2]

        export = Export(self._config.options.force)
        export.export_platform(plat, root_folder)

    def _export_doc(self):
        return ActionDoc("export", "<org_name> <plat_name> [<output_folder>] [--force]", """
        Export platform onto disk. --force option causes existing files to
        be overwritten.""")

    # Import

    def _print_import_completions(self, param_num, argv):
        if param_num < 1:
            self._print_collection_completions(param_num, argv)
        elif param_num == 1:
            completions.print_dir_completions()

    def _import(self, argv):
        if len(argv) != 2:
            raise ArgumentException("Wrong number of arguments")

        org = self._client.organizations().get(argv[0])
        imp = Import(update_existing=self._config.options.update_existing)
        imp.import_platform(org, argv[1])

    def _import_doc(self):
        return ActionDoc("import", "<org_name> <src_folder> [--update-existing]", """
        Import platform from disk. --update-existing option causes existing entities
        on server to be updated.""")

    def _images(self, argv):
        plat = self._get_entity(argv)
        images = plat.list_images()
        if self._config.options.raw:
            print(json.dumps([image.get_json() for image in images], indent=4))
        else:
            for image in images:
                image.show()

    def _images_doc(self):
        return ActionDoc("images", "<org_name> <plat_name>", """
        Lists images associated with given platform.""")
