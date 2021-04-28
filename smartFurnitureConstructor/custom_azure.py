from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'smartconstructorstorage' # Must be replaced by your <storage_account_name>
    account_key = '01GtJjOaEeNRdCSkh6xFfU2PSpx8OU7jNqzghNjVAY632sc38d8Hib7DPbF6ODcSkQyLvesMh96n6RKsjbY6lw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'smartconstructorstorage' # Must be replaced by your storage_account_name
    account_key = '01GtJjOaEeNRdCSkh6xFfU2PSpx8OU7jNqzghNjVAY632sc38d8Hib7DPbF6ODcSkQyLvesMh96n6RKsjbY6lw==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None