#!/usr/bin/python3

"""思源笔记API

file: /api.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-10-7
"""

from urllib.parse import urljoin

import requests
from loguru import logger
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from errors import CodeError, StatusError


class Siyuan:
    """思源笔记API实现类
    仅实现了思源助手相关 API, 其余未使用到的暂未编写
    """

    def __init__(self, url: str, token: str, verify: bool = True, dry_run: bool = False):
        """初始化

        :arg url: 思源笔记的基地址  e.g. http://localhost:6806/
        :arg verify: 是否验证 TLS 证书
        :arg dry_run: 不发送实际请求
        """
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {token}"
        self.session.verify = verify
        self.url = url
        self.dry_run = dry_run

        if not verify:
            disable_warnings(InsecureRequestWarning)

    def ls_notebooks(self) -> list:
        """列出所有笔记本

        :returns: 返回`名称-ID`键值对格式的数据
        :rtype: [(name, id), ...]
        """
        if self.dry_run:
            return [('思源笔记用户指南', '20210808180117-czj9bvb'), ('测试笔记本', '20210817205410-2kvfpfn')]

        request_url = urljoin(self.url, "/api/notebook/lsNotebooks")
        logger.debug(f"request url {request_url}")

        response = self.session.post(request_url)
        if response.status_code != 200:
            raise StatusError(response.status_code)

        response = response.json()
        logger.debug(response)

        # 判断返回码是否正常
        if response["code"] != 0:
            raise CodeError(f"Error Code {response['code']} {response['msg']}")

        result = []
        for notebook in response["data"]["notebooks"]:
            result.append([notebook['name'], notebook['id']])
        return result

    def upload_asset(self, file: str) -> str:
        """上传资源到 `/data/assets` 目录

        :param file: 本地资源路径，需要传入绝对路径。
        :returns: 服务端文件资源路径
        """
        if self.dry_run:
            return 'assets/foo-20210719092549-9j5y79r.png'

        request_url = urljoin(self.url, "/api/asset/upload")
        logger.debug(f"request url {request_url}")

        files = {'file[]': open(file, mode='rb')}
        data = {'assetsDirPath': '/assets/'}

        response = self.session.post(request_url, data=data, files=files)
        if response.status_code != 200:
            raise StatusError(response.status_code)

        response = response.json()
        logger.debug(response)

        if response["code"] != 0:
            raise CodeError(f"Error Code {response['code']} {response['msg']}")
        # 错误文件
        if response['data']['errFiles']:
            logger.warning("err file", response['data']['errFiles'])

        files['file[]'].close()
        return list(response['data']['succMap'].values())[0]

    def get_unused_assets(self) -> list:
        """列出所有未使用资源
        """
        if self.dry_run:
            return ['assets/foo-20210719092549-9j5y79r.png', 'assets/image-20230719092549-9j4mcgt.png']

        request_url = urljoin(self.url, "/api/asset/getUnusedAssets")
        logger.debug(f"request url {request_url}")

        response = self.session.post(request_url)
        if response.status_code != 200:
            raise StatusError(response.status_code)

        response = response.json()
        logger.debug(response)

        if response["code"] != 0:
            raise CodeError(f"Error Code {response['code']} {response['msg']}")

        return response['data']['unusedAssets']

    def remove_unused_assets(self) -> list:
        """删除所有未使用资源

        :returns: 已删除的文件列表
        """
        if self.dry_run:
            return ['assets/foo-20210719092549-9j5y79r.png', 'assets/image-20230719092549-9j4mcgt.png']

        request_url = urljoin(self.url, "/api/asset/removeUnusedAssets")
        logger.debug(f"request url {request_url}")

        response = self.session.post(request_url)
        if response.status_code != 200:
            raise StatusError(response.status_code)

        response = response.json()
        logger.debug(response)

        if response["code"] != 0:
            raise CodeError(f"Error Code {response['code']} {response['msg']}")

        return response['data']['paths']

    def create_markdown_document(self, notebook: str, doc_name: str, markdown: str) -> str:
        """直接在思源笔记根目录创建 Markdown 格式的文档
        注: 重复上传不会覆盖原有文档

        :param notebook: 笔记本 ID
        :param doc_name: 文档名称(实际上是文档路径)
        :param markdown: Markdown格式的文档(要先把 Markdown 中的图像上传至 assets 目录下)
        :returns: 新建文档的ID
        """
        if self.dry_run:
            return '20210914223645-oj2vnx2'

        request_url = urljoin(self.url, "/api/filetree/createDocWithMd")
        logger.debug(f"request url {request_url}")

        data = {
            "notebook": notebook,
            "path": "/" + doc_name,
            "markdown": markdown
        }

        response = self.session.post(request_url, json=data)
        if response.status_code != 200:
            raise StatusError(response.status_code)

        response = response.json()
        logger.debug(response)

        if response["code"] != 0:
            raise CodeError(f"Error Code {response['code']} {response['msg']}")

        return response['data']
