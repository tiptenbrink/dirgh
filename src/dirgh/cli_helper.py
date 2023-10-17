import getpass
import os


def find_token(env_prefix: str = "", ask_token: bool = False):
    # <env_prefix>DIRGH_GH_TOKEN
    pass_key = f"{env_prefix}dirgh_gh_token".replace('-', '_')
    pass_key_env = pass_key.upper()
    if ask_token:
        key_pass = getpass.getpass("Input your token:\n")
    else:
        key_pass = os.environ.get(pass_key_env)
        if key_pass is None:
            raise ValueError(f"Please supply token or set the {pass_key_env} environment variable!")

    return key_pass
