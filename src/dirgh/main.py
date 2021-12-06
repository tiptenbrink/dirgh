import functools

import trio

import dirgh

if __name__ == '__main__':
    owner = "tiptenbrink"
    repo = "tiauth"
    directory = "deployment"
    ref = "HEAD"
    recursive = True
    target = 'download2'
    token = ""
    find_download = functools.partial(dirgh.find_download, owner, repo, directory, target=target, ref=ref,
                                      recursive=recursive, token=token)
    trio.run(find_download)
