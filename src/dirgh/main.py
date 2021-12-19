import functools

import trio

import dirgh

if __name__ == '__main__':
    owner = ""
    repo = ""
    directory = "somefolder"
    ref = "HEAD"
    recursive = True
    target = None
    token = ""

    find_download = functools.partial(dirgh.find_download, owner, repo, directory, target=target, ref=ref,
                                      recursive=recursive, token=token)
    trio.run(find_download)
