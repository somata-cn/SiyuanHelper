#!/usr/bin/python3

"""思源助手主程序, 用于将本地Markdown上传至思源笔记本。

file: /uploader.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-7-31
"""


import re
from os.path import join as pathjoin
from os.path import basename, normcase, dirname
from sys import argv, stderr
from sys import exit as broken
from loguru import logger
from api import Siyuan
from config import URL, TOKEN, VERIFY

logger.remove()
logger.add(stderr, level="INFO")


@logger.catch
def main():
    """主函数
    """
    if len(argv) != 2:
        logger.error("Please input filename.")
        broken(129)

    makrdown_file = argv[1]

    siyuan = Siyuan(URL, TOKEN, VERIFY)

    # 选择笔记本
    notebooks = siyuan.ls_notebooks()
    i = 0
    for notebook in notebooks:
        print(f"[{i}] - \"{notebook[0]}\"")
        i += 1
    target_notebook_id = notebooks[int(input("请选择笔记本:"))][1]
    logger.debug(f"target notebook id: {target_notebook_id}")

    with open(makrdown_file, mode='r', encoding='utf-8') as file_pointer:
        markdown = file_pointer.read()

    # 查找markdown中的本地图像, 上传, 替换路径
    img_pattern = re.compile(r"!\[(.*?)\]\((.*)\)")
    net_pattern = re.compile(r"^https?:\/\/")
    for match in img_pattern.finditer(markdown):
        matched_str = match.group(0)
        desc, path = match.group(1, 2)
        logger.debug(f"match resource {path}")
        # 判断资源是否为本地路径
        if net_pattern.match(path):
            logger.debug(f"network resource {path}")
            continue
        path = normcase(pathjoin(dirname(makrdown_file), path))

        server_path = siyuan.upload_asset(path)
        logger.info(f"upload file {path} success")

        markdown = markdown.replace(matched_str, f"![{desc}]({server_path})")

    # 上传Markdown
    document_name = basename(makrdown_file)
    document_id = siyuan.create_markdown_document(
        target_notebook_id, document_name, markdown)
    logger.info(f"uploaded document id: {document_id}")


if __name__ == "__main__":
    main()
