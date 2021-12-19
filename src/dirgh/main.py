import functools
import logging

import trio

import dirgh

if __name__ == '__main__':
    owner = "tiptenbrink"
    repo = "tiauth"
    directory = "ci"
    ref = "HEAD"
    recursive = True
    target = None
    token = None
    logging.basicConfig(level=logging.INFO)

    find_download = functools.partial(dirgh.find_download, owner, repo, directory, target=target, ref=ref,
                                      recursive=recursive, token=token, overwrite=True)
    trio.run(find_download)
