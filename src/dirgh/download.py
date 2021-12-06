import httpx
import trio
from pathlib import Path
from functools import partial


async def api(endpoint, token=None):
    async with httpx.AsyncClient() as client:
        headers = {'user-agent': 'dirgh/0.0.1'}
        if token is not None:
            headers["Authorization"] = f'token {token}'
        req_string = f'https://api.github.com/repos/{endpoint}'

        response = await client.get(req_string, headers=headers)

        return response.json()


async def get_contents(user, repository, directory, ref, token, do_print=False):
    endpoint = f'{user}/{repository}/contents/{directory}?ref={ref}'
    if do_print:
        print(f"Requesting API contents from {endpoint}")

    return await api(endpoint, token)


async def download(url, path: str, root_dir=None, target=None, token=None):
    if root_dir is None:
        root_dir = 'download'
    root_dir.replace('\\', '/').removesuffix('/')

    if target is None:
        target = f"./{root_dir}"
    target = target.replace('\\', '/').removesuffix('/')
    target_path = Path(target)

    if len(target_path.parents) > 0:
        path = path.removeprefix(f"{root_dir}").removeprefix('/')
    download_path = target_path.joinpath(path)
    parent_path = download_path.parent
    parent_path.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as client:
        headers = {'user-agent': 'dirgh/0.1.0'}
        if token is not None:
            headers["Authorization"] = f'token {token}'
        with open(download_path, 'xb') as f:
            response = await client.get(url, headers=headers)
            f.write(response.read())


async def download_contents(contents, root_dir=None, target=None, token=None):
    async with trio.open_nursery() as nursery:
        for cont in contents:
            download_fn = partial(download, cont['down'], cont['path'], root_dir=root_dir, target=target, token=token)
            nursery.start_soon(download_fn)
    print("Download successful!")


async def via_contents_prod(send_channel, user, repository, directory, jsn_list=None, ref="HEAD", token=None, recursive=True):
    if jsn_list is None:
        jsn_list = await get_contents(user, repository, directory, ref, token)
    async with trio.open_nursery() as nursery:
        async with send_channel:
            for jsn in jsn_list:
                path = jsn['path']
                if jsn['type'] == 'file':
                    await send_channel.send({'path': path, 'down': jsn['download_url']})
                elif recursive and jsn['type'] == 'dir':
                    via_content = partial(via_contents_prod, send_channel.clone(), user, repository, path, ref=ref,
                                          token=token, recursive=recursive)
                    nursery.start_soon(via_content)


async def via_contents(user, repository, directory, ref="HEAD", token=None, recursive=True):
    final_results = []
    async with trio.open_nursery() as nursery:
        send_channel, receive_channel = trio.open_memory_channel(0)
        async with send_channel:
            jsn_list = await get_contents(user, repository, directory, ref, token, do_print=True)
            via_content = partial(via_contents_prod, send_channel.clone(), user, repository, directory,
                                  jsn_list=jsn_list, ref=ref, token=token, recursive=recursive)
            nursery.start_soon(via_content)
        async with receive_channel:
            async for value in receive_channel:
                final_results.append(value)

    return final_results


async def find_download(owner, repository, directory=None, target=None, ref='HEAD', recursive=True, token=None):
    if directory is None:
        directory = ''
        root_dir = None
    else:
        root_dir = directory
    directory = directory.replace('\\', '/').removeprefix('/').removesuffix('/')
    contents = await via_contents(owner, repository, directory, ref=ref, recursive=recursive, token=token)
    print(f"Found {len(contents)} files, starting download...")
    await download_contents(contents, root_dir=root_dir, target=target, token=token)
