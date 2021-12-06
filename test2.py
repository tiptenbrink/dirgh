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
        print(req_string)
        response = await client.get(req_string, headers=headers)
        # print(response)
        return response.json()


async def download(url, path: str, token=None):
    async with httpx.AsyncClient() as client:
        dir_path = ''.join(path.rsplit('/')[:-1])
        parent_path = Path(f'./{dir_path}')
        parent_path.mkdir(parents=True, exist_ok=True)

        headers = {'user-agent': 'dirgh/0.0.1'}
        if token is not None:
            headers["Authorization"] = f'Bearer {token}'
        response = await client.get(url, headers=headers)
        with open(f'{path}', 'xb') as f:
            f.write(response.read())


async def download_contents(contents, token=None):
    async with trio.open_nursery() as nursery:
        for cont in contents:
            download_fn = partial(download, cont['down'], cont['path'], token=token)
            nursery.start_soon(download_fn)


async def via_contents_prod(send_channel, user, repository, directory, ref="HEAD", token=None, recursive=True):
    jsn_list = await api(f'{user}/{repository}/contents/{directory}?ref={ref}', token)
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
            via_content = partial(via_contents_prod, send_channel.clone(), user, repository, directory, ref=ref,
                                  token=token, recursive=recursive)
            nursery.start_soon(via_content)
        async with receive_channel:
            async for value in receive_channel:
                final_results.append(value)

    return final_results


async def main():

    #contents = await via_contents("tiptenbrink", "tiauth", "deployment", ref="3b45b61a673ba30b7919c13848ebd37236c75161", token=token)
    #print(contents)
    #await download_contents(contents)
    x = await api("tiptenbrink/tiauth/contents/deployment?ref=3b45b61a673ba30b7919c13848ebd37236c75161", token)
    print(x)


trio.run(main)
