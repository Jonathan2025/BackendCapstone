# file: ./custom_storage/custom_azure.py
from storages.backends.azure_storage import AzureStorage

class PublicAzureStorage(AzureStorage):
    account_name = 'capstonefilestorage'
    account_key = '8A6hI9IadWzmLIRIHphVlbfFk/P7OytzB47Q8CaCwBBOLA0KFNCqnRVAPc/OeaKdlzd+gDEr1w0E+AStLlkB5g=='
    azure_container = 'capstonecontainer'
    expiration_secs = None

    