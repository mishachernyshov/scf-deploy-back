from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'smartconstructor' # Must be replaced by your <storage_account_name>
    account_key = 'uZp5iYrqHVY3kakumO/QkNJKhqKHAXpRIp5kC9VsgOL8ZDR3f3nU7sUUPRxzxnKSXQ9nQ9JK+ZzMEhML8CEhwQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'smartconstructor' # Must be replaced by your storage_account_name
    account_key = 'uZp5iYrqHVY3kakumO/QkNJKhqKHAXpRIp5kC9VsgOL8ZDR3f3nU7sUUPRxzxnKSXQ9nQ9JK+ZzMEhML8CEhwQ==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None