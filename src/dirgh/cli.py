import argparse
import functools

import trio

import dirgh


def run():
    cli_name = 'dirgh'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Download single directories from GitHub.\n"
                                                 "GitHub rate limits are 60 requests/hour when unauthenticated and\n"
                                                 "5,000/hour when using a token. Each subfolder incurs requires \n"
                                                 "extra requests."
                                                 "\n\n"
                                                 "examples:\n"
                                                 f"{cli_name} -r tiptenbrink/tiauth -d deployment -rf "
                                                 f"cf51bff1a79b280388ba65f18998717b2fa5e1e3\n")

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

    ref_nm = 'ref'
    ref_default = 'HEAD'
    ref_help = f"commit reference, can be in any branch. (default: {ref_default})"
    parser.add_argument('-rf', f'--{ref_nm}', help=ref_help, default=ref_default, required=False)

    recursive_nm = 'recursive'
    recursive_help = "recursively enter all subfolders to get all files."
    parser.add_argument('-R', f'--{recursive_nm}', help=recursive_help, default=False, required=False,
                        action='store_true')
    token_nm = 'token'
    token_help = f"user authentication token, OAuth or personal access token. Not required but increases rate limits."
    parser.add_argument('-t', f'--{token_nm}', help=token_help, default=None, required=False)

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

    find_download = functools.partial(dirgh.find_download, owner, repo, config[dir_nm], ref=config[ref_nm],
                                      recursive=config[recursive_nm], token=config[token_nm])
    trio.run(find_download)
