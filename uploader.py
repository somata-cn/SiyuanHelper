#!/usr/bin/python3

"""思源上传助手主程序, 用于将本地Markdown上传至思源笔记本。

file: /uploader.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-10-7
"""

import re
from os.path import basename, dirname
from os.path import join as pathjoin
from os.path import normcase
from sys import stderr

from loguru import logger
from argparser import uploader_parser

from api import Siyuan

USAGE = """文件上传助手, 请在 config.py 配置基础信息
usage: python3 ./uploader.py <FILE[ FILE...]>
"""


def choose_notebook(siyuan: Siyuan) -> str:
    """交互式选择一个笔记本"""
    notebooks = siyuan.ls_notebooks()
    i = 0
    for notebook in notebooks:
        print(f"[{i}] - \"{notebook[0]}\"")
        i += 1
    target_notebook_id = notebooks[int(input("请选择笔记本:"))][1]
    logger.debug(f"target notebook id: {target_notebook_id}")
    return target_notebook_id


def upload_note(siyuan: Siyuan, notebook: str, markdown_file: str) -> bool:
    """解析图片后上传笔记
    :arg notebook: 笔记本ID
    :arg markdown_file: 笔记路径
    """
    try:
        with open(markdown_file, mode='r', encoding='utf-8') as file_pointer:
            markdown = file_pointer.read()
    except FileNotFoundError:
        logger.error(f"{markdown_file} file not found")
        return False

    # 查找markdown中的本地图像, 上传, 替换路径
    img_pattern = re.compile(r"!\[(.*?)\]\((.*)\)")
    net_pattern = re.compile(r"^https?:\/\/")

    # TODO: 相同文件去重
    for match in img_pattern.finditer(markdown):
        matched_str = match.group(0)
        desc, path = match.group(1, 2)
        logger.debug(f"match resource {path}")

        # 判断资源是否为本地路径
        if net_pattern.match(path):
            logger.debug(f"network resource {path}")
            continue

        path = normcase(pathjoin(dirname(markdown_file), path))
        server_path = siyuan.upload_asset(path)
        logger.info(f"upload file {path} success")

        markdown = markdown.replace(matched_str, f"![{desc}]({server_path})")

        # 替换文档名称
    document_name = basename(markdown_file).replace(".md", "")
    title_pattern = re.compile(rf"^# {document_name}\n")
    markdown = title_pattern.sub("", markdown)

    # 上传Markdown
    document_id = siyuan.create_markdown_document(
        notebook, document_name, markdown)
    logger.info(f"uploaded document id: {document_id}")
    return True


@logger.catch
def main():
    """主函数
    """
    args = uploader_parser()

    logger.remove()
    logger.add(stderr, level=args.log_level)

    siyuan = Siyuan(args.url, args.token, args.verify, args.dry_run)

    # 交互式获取笔记本 ID
    if args.interactive:
        target_notebook_id = choose_notebook(siyuan)
    else:
        target_notebook_id = args.notebook_id

    # 开始上传文件
    for file in args.files:
        if file.endswith(".md"):
            upload_note(siyuan, target_notebook_id, file)
        else:
            logger.warning("please input a markdown-type file.")


if __name__ == "__main__":
    main()
