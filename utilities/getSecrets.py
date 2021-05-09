import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def get_secret(secretName, keyVaultName):
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    
    client = SecretClient(vault_url=KVUri, credential=credential)

    print(f"Retrieving your secret from {keyVaultName}.")

    retrieved_secret = client.get_secret(secretName)

    print(f"Your secret {secretName} is successfully retrieved.")

    return retrieved_secret.value
