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


summary:
```
SiyuanHelper
├─api.py: SiYuan API implement
├─argparser.py: command line args parser
└─uploader.py: file uploader
```