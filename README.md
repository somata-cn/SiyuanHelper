# SiyuanHelper

一个简易的Markdown文档上传工具，思源笔记专用。

编写这个程序的原因：我一直使用的都是思源 Docker 镜像，但是在Web操作并不能直接导入本地Markdown格式的文件，所以这里编写了一个上传助手。


使用方法:
1. 安装依赖, 推荐使用 [pdm](https://github.com/pdm-project/pdm) 项目管理
    ```shell
    pdm install
    # or
    pip install requests loguru
    ```
2. 创建`config.py`, 并编写配置文件
   ```python
   URL = r"http://localhost:6806"
   TOKEN = r"your token"
   ```
3. 运行程序
   ```shell
   python main.py "文件路径"
   ```


文件内容摘要:
```
SiyuanHelper
├─api.py: 思源笔记的 API 方法实现
└─main.py: 文件上传助手
```