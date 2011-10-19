from cortex_client.rest.client import Client
from directory import Directory
from application_collection import ApplicationCollection
from change_request_collection import ChangeRequestCollection
from distribution_collection import DistributionCollection
from environment_collection import EnvironmentCollection
from file_collection import FileCollection
from host_collection import HostCollection
from organization_collection import OrganizationCollection
from platform_collection import PlatformCollection
from user_collection import UserCollection

class CortexApi(object):

    def __init__(self, endpoint, username, password):
        self._client = Client(endpoint, username, password)
        self._directory = Directory(self)

        self._appl_collection = ApplicationCollection(self)
        self._chan_collection = ChangeRequestCollection(self)
        self._dist_collection = DistributionCollection(self)
        self._envi_collection = EnvironmentCollection(self)
        self._file_collection = FileCollection(self)
        self._host_collection = HostCollection(self)
        self._orga_collection = OrganizationCollection(self)
        self._plat_collection = PlatformCollection(self)
        self._user_collection = UserCollection(self)

    def get_client(self):
        return self._client

    def get_directory(self):
        return self._directory

    def get_application_collection(self):
        return self._appl_collection

    def get_change_request_collection(self):
        return self._chan_collection
    
    def get_distribution_collection(self):
        return self._dist_collection

    def get_environment_collection(self):
        return self._envi_collection

    def get_file_collection(self):
        return self._file_collection

    def get_host_collection(self):
        return self._host_collection

    def get_organization_collection(self):
        return self._orga_collection

    def get_platform_collection(self):
        return self._plat_collection

    def get_user_collection(self):
        return self._user_collection
