from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'smartconstructorstorage' # Must be replaced by your <storage_account_name>
    account_key = '9Crrc3cj6XgIIA2cFb6a4PXhFRGTN+kjvghcQDq/sDxh5DEzDQ14/1xgUyURgE/u7dPq8QVKVHAnJ448Qteq7g==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'smartconstructorstorage' # Must be replaced by your storage_account_name
    account_key = '9Crrc3cj6XgIIA2cFb6a4PXhFRGTN+kjvghcQDq/sDxh5DEzDQ14/1xgUyURgE/u7dPq8QVKVHAnJ448Qteq7g==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None