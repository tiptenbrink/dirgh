# dirgh

With `dirgh` you can easily download a directory from GitHub programmatically from Python or using the CLI.

## CLI

```shell
usage: dirgh [-h] -r REPO [-o OWNER] [-d DIRECTORY] [-t TARGET] [--ref REF] [-R] [-O] [-a AUTH]

Download single directories from GitHub.
GitHub rate limits are 60 requests/hour when unauthenticated and 5,000/hour
 when using a token. Each subfolder  requires extra requests.

examples:
dirgh -r tiauth -o tiptenbrink -d deployment --ref cf51bff1a79b280388ba65f18998717b2fa5e1e3
dirgh -r tiptenbrink/tiauth -d deployment -R -t 'C:\Users\dirgher'\Cool projects/dürghé'
(You can use both forward and backwardslashes, even interchangeably)
dirgh -r tiptenbrink/tiauth -R -t './dürghé'

optional arguments:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  repository on GitHub using the format <owner>/<repository> or just <repository> if owner is also specified. If both are specified, owner is ignored.
  -o OWNER, --owner OWNER
                        repository owner on GitHub, can be an organization or user. Only necessary when not provided in the --repo option.
  -d DIRECTORY, --directory DIRECTORY
                        initial directory path in the format <subfolder1>/<subfolder2> etc. Defaults to root directory.
  -t TARGET, --target TARGET
                        output directory. If requesting a directory, this will overwrite the directory name. By default, the content will be placed in './dirgh/1673538759'.
  --ref REF             commit reference, can be in any branch. (default: HEAD)
  -R, --recursive       recursively enter all subfolders to get all files.
  -O, --overwrite       Overwrite target directory.
  -a AUTH, --auth AUTH  user authentication token, OAuth or personal access token. Not required but increases rate limits.
```
