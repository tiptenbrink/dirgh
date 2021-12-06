import httpx
from httpx import Response
import trio
from pathlib import Path


async def api(endpoint, token=None):
    async with httpx.AsyncClient() as client:
        headers = {'user-agent': 'dirgh/0.0.1'}
        if token is not None:
            headers["Authorization"] = f'Bearer {token}'
        req_string = f'https://api.github.com/repos/{endpoint}'
        #print(req_string)
        response = await client.get(req_string, headers=headers)
        #print(response)
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


async def via_contents(user, repository, directory, ref="HEAD", token=None, current_paths=None, recursive=True):
    if current_paths is None:
        current_paths = []

    jsn_list = await api(f'{user}/{repository}/contents/{directory}?ref={ref}', token)
    async with trio.open_nursery() as nursery:
        for jsn in jsn_list:
            path = jsn['path']
            if jsn['type'] == 'file':
                current_paths.append({'path': path, 'down': jsn['download_url']})
            elif recursive and jsn['type'] == 'dir':
                current_paths = await via_contents(user, repository, path, ref, token, current_paths, recursive)

    return current_paths




async def main():
    contents = await via_contents("tiptenbrink", "tiauth", "", ref="3b45b61a673ba30b7919c13848ebd37236c75161")
    print(contents)
    # for cont in contents:
    #     await download(cont['down'], cont['path'])


trio.run(main)
