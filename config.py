import os
from dynaconf import Dynaconf

import re
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


def load_azure_key_vault(obj, env=None, silent=False, key=None, filename=None):
    """
    Reads and loads in to "obj" a single key or all keys from source
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    """

    key_vault_name = os.getenv("KEY_VAULT_NAME")
    if key_vault_name is None:
        return

    key_vault_url = f"https://{key_vault_name}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    all_secrets = client.list_properties_of_secrets()

    new_settings = {}

    regex = re.compile(r"^(\w+)-(\w+)$")

    for s in all_secrets:
        name = s.name
        value = client.get_secret(name).value

        if m := regex.match(name):
            new_settings[m.group(1)] = {m.group(2): value}
        else:
            new_settings[name] = value

    obj.update(new_settings)


settings = Dynaconf(
    envvar_prefix="DYNACONF",
)

load_azure_key_vault(settings)
