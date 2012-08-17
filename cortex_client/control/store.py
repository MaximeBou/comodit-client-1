import json, os

from cortex_client.control.root_resource import RootResourceController
from cortex_client.control.exceptions import ArgumentException
from cortex_client.config import Config
from cortex_client.util.editor import edit_text

class StoreController(RootResourceController):

    def __init__(self):
        super(StoreController, self).__init__()

        self._template = "purchased_entity.json"

        self._unregister("add")
        self._unregister("update")
        self._unregister("delete")

        self._register("purchase", self._purchase, self._print_purchase_completions)

    def _print_purchase_completions(self, param_num, argv):
        if param_num == 0:
            self._print_identifiers(self.get_collection(argv))
        elif param_num == 1:
            self._print_identifiers(self._api.organizations())

    def _purchase(self, argv):
        if len(argv) < 2:
            raise ArgumentException("A published entity UUID and an organization name must be provided")

        pub = self._get_resource(argv)
        org = self._api.organizations().get_resource(argv[1])

        template_json = json.load(open(os.path.join(Config()._get_templates_path(), self._template)))
        template_json["published"] = pub.get_uuid()
        template_json["name"] = pub.get_name()
        updated = edit_text(json.dumps(template_json, indent = 4))

        pur_app = self.get_purchased_collection(org)._new_resource(json.loads(updated))
        pur_app.create()

class AppStoreController(StoreController):

    def __init__(self):
        super(AppStoreController, self).__init__()
        self._doc = "Application store handling."

    def get_collection(self, argv):
        return self._api.app_store()

    def get_purchased_collection(self, org):
        return org.purchased_apps()

class DistStoreController(StoreController):

    def __init__(self):
        super(DistStoreController, self).__init__()
        self._doc = "Distribution store handling."

    def get_collection(self, argv):
        return self._api.dist_store()

    def get_purchased_collection(self, org):
        return org.purchased_dists()