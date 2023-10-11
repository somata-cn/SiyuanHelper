# SiyuanHelper

a simple SiYuan notes management tool, the core of this tool is to upload your markdown-type files to server.


usage:
1. Installation dependencies, recommand using [pdm](https://github.com/pdm-project/pdm) to manage your project.
    ```shell
    pdm install
    # or
    pip install requests loguru
    ```
2. running program
    ```shell
    python uploader.py --help
    python uploader.py -u 'http://localhost:4343/' -t '123456' -i 'PATHTOYOUR.md'
    ```
3. command line argument file(optional), Input parameters in behavioral units. the file name is `args.txt`. see examples for usage
    ```
    -u
    http://localhost:6806/
    -t
    123456
    -i
    ```


summary:
```
SiyuanHelper
├─api.py: SiYuan API implement
├─argparser.py: command line args parser
├─args.txt: command line argument file
├─errors.py: all error types
└─uploader.py: file uploader
```