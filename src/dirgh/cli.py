import argparse

import trio

import dirgh
from dirgh.download import default_download


def run():
    cli_name = 'dirgh'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Download single directories from GitHub.\n"
                                                 "GitHub rate limits are 60 requests/hour when unauthenticated and "
                                                 "5,000/hour\n when using a token. Each subfolder  requires extra "
                                                 "requests."
                                                 "\n\n"
                                                 "examples:\n"
                                                 f"{cli_name} -r tiauth -o tiptenbrink -d deployment --ref "
                                                 f"cf51bff1a79b280388ba65f18998717b2fa5e1e3\n"
                                                 f"{cli_name} -r tiptenbrink/tiauth -d deployment -R -t "
                                                 f"'C:\\Users\\dirgher'"
                                                 f"\\Cool projects/dürghé'\n(You can use both forward and backward"
                                                 f"slashes, even interchangeably)\n"
                                                 f"{cli_name} -r tiptenbrink/tiauth -R -t './dürghé'")

    repo_nm = 'repo'
    repo_help = "repository on GitHub using the format <owner>/<repository> or just \n" \
                "<repository> if owner is also specified. If both are specified, owner is ignored."
    parser.add_argument('-r', f'--{repo_nm}', help=repo_help, required=True)

    owner_nm = 'owner'
    owner_help = f"repository owner on GitHub, can be an organization or user. Only \n" \
                 f"necessary when not provided in the --{repo_nm} option."
    parser.add_argument('-o', f'--{owner_nm}', help=owner_help, default=None, required=False)

    dir_nm = 'directory'
    dir_help = "initial directory path in the format <subfolder1>/<subfolder2> etc. Defaults to root directory."
    parser.add_argument('-d', f'--{dir_nm}', help=dir_help, default=None, required=False)

    target_nm = 'target'
    target_help = f"output directory. If requesting a directory, this will overwrite the directory name of the " \
                  f"requested one. By default, the content will be placed in './{default_download}'."
    parser.add_argument('-t', f'--{target_nm}', help=target_help, default=None, required=False)

    ref_nm = 'ref'
    ref_default = 'HEAD'
    ref_help = f"commit reference, can be in any branch. (default: {ref_default})"
    parser.add_argument(f'--{ref_nm}', help=ref_help, default=ref_default, required=False)

    recursive_nm = 'recursive'
    recursive_help = "recursively enter all subfolders to get all files."
    parser.add_argument('-R', f'--{recursive_nm}', help=recursive_help, default=False, required=False,
                        action='store_true')

    overwrite_nm = 'overwrite'
    overwrite_help = "Overwrite target directory."
    parser.add_argument('-O', f'--{overwrite_nm}', help=overwrite_help, default=False, required=False,
                        action='store_true')

    token_nm = 'auth'
    token_help = f"user authentication token, OAuth or personal access token. Not required but increases rate limits."
    parser.add_argument('-a', f'--{token_nm}', help=token_help, default=None, required=False)

    config = vars(parser.parse_args())

    if "/" in config[repo_nm]:
        split_repo = config[repo_nm].split("/")
        owner = split_repo[0]
        repo = split_repo[1]
    elif config[owner_nm] is None:
        raise ValueError(f"Supply --{owner_nm} if not fully qualifying owner in --{repo_nm}")
    else:
        owner = config[owner_nm]
        repo = config[repo_nm]


    find_download = lambda: dirgh.find_download(owner, repo, config[dir_nm], target=config[target_nm],
                                      ref=config[ref_nm], recursive=config[recursive_nm], overwrite=config[overwrite_nm],
                                      token=config[token_nm])
    trio.run(find_download)
