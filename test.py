import httpx
import trio


async def api(endpoint, token=None):
    async with httpx.AsyncClient() as client:
        headers = {'user-agent': 'githubfolder/0.0.1'}
        if token is not None:
            headers["Authorization"] = f'Bearer {token}'
        req_string = f'https://api.github.com/repos/{endpoint}'
        print(req_string)
        response = await client.get(req_string, headers=headers)
        print(response)
        print(response.json())


async def via_trees(user, repository, directory, ref="HEAD", token=None):
    await api(f'{user}/{repository}/contents/{directory}?ref={ref}', token)


async def main():
    await via_trees("tiptenbrink", "tiauth", "deployment", ref="3b45b61a673ba30b7919c13848ebd37236c75161")


trio.run(main)
