# SiyuanHelper

一个简易的思源笔记管理工具，其核心功能为上传本地 Markdown 文件。

编写这个程序的原因：我一直使用的都是思源 Docker 镜像，但是在Web操作并不能直接导入本地Markdown格式的文件，所以这里编写了一个上传助手。


使用方法:
1. 安装依赖, 推荐使用 [pdm](https://github.com/pdm-project/pdm) 来管理你的项目管理
    ```shell
    pdm install
    # or
    pip install requests loguru pillow
    ```
2. 运行程序
    ```shell
    python uploader.py --help  # 查看帮助手册
    python uploader.py -u 'http://localhost:4343/' -t '123456' -i 'PATHTOYOUR.md'
    ```
3. 文本配置参数(可选), 以行为单位输入参数，文件名为 `args.txt`。用法见样例
    ```
    --url
    http://localhost:6806/
    --token
    123456
    ```


文件内容摘要:
```
SiyuanHelper
├─api.py: 思源笔记的 API 方法实现
├─argparser.py: 命令行参数解析器
├─args.txt: 命令行参数文件
├─errors.py: 所有错误类型
└─uploader.py: 文件上传助手
```