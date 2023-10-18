#!/usr/bin/python3
# pylint: disable=C0116

"""思源上传助手上传功能, 用于将本地Markdown上传至思源笔记本。

file: /uploader.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-10-7
"""

import re
from os.path import normcase, basename, dirname
from os.path import join as pathjoin
from os.path import exists as pathexists
from sys import stderr

from loguru import logger
from PIL import Image
import argparser

from api import Siyuan

USAGE = """文件上传助手, 请在 config.py 配置基础信息
usage: python3 ./uploader.py <FILE[ FILE...]>
"""
VERSION = "v0.3.0"
IMAGE_SUFFIXES = [".png", ".jpeg", ".png", ".gif"]


def is_image(path: str) -> bool:
    for suffix in IMAGE_SUFFIXES:
        if path.lower().endswith(suffix):
            return True
    return False


def image_convert_to_webp(path: str) -> str:
    """将图片格式转换为WEBP格式

    :arg path: 源图片路径
    :return: 返回转换完成的文件路径
    """
    # 若文件格式已经是 WEBP 则直接返回路径
    if path.lower().endswith('.webp'):
        return path

    # 将文件路径替换为webp
    saved_path = ".".join(path.split('.')[:-1]) + '.webp'
    if pathexists(saved_path):
        logger.info(f'image already convert {path}')
        return saved_path

    im = Image.open(path)
    im.save(saved_path, "WEBP")

    logger.info(f'convert file {path} success')
    return saved_path


def choose_notebook(siyuan: Siyuan) -> str:
    notebooks = siyuan.ls_notebooks()

    for i, notebook in enumerate(notebooks):
        print(f"[{i}] - \"{notebook[0]}\" [{notebook[1]}]")

    try:
        target_notebook_id = notebooks[int(input("请选择笔记本:"))][1]
    except KeyboardInterrupt:
        logger.debug('user interrupted the program')
        exit(1)
    except ValueError:
        logger.error('please enter a number in the correct format')
        exit(129)
    except IndexError:
        logger.error('Please enter a value within the correct range')
        exit(129)

    logger.debug(f"target notebook id: {target_notebook_id}")
    return target_notebook_id


def upload_note(siyuan: Siyuan, notebook: str, markdown_file: str, convert: bool = False) -> bool:
    """上传笔记
    在上传之前会先将笔记内的资源上传至服务器再上传笔记

    :arg notebook: 笔记本ID
    :arg markdown_file: 笔记路径
    """
    try:
        with open(markdown_file, mode='r', encoding='utf-8') as file_pointer:
            markdown = file_pointer.read()
    except FileNotFoundError:
        logger.error(f"{markdown_file} file not found")
        return False

    # 查找markdown中的本地资源, 上传, 替换路径
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

        path = normcase(pathjoin(dirname(markdown_file), path))
        # 如果是图片资源则进行格式转换
        if convert and is_image(path):
            path = image_convert_to_webp(path)

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
def run(args):
    """主函数
    """

    if args.version:
        print(f"SiYuan uploader {VERSION}")
        exit(0)

    # 输出日志等级
    logger.remove()
    if args.verbose:
        logger.add(stderr, level='TRACE')
    else:
        logger.add(stderr, level=args.log_level)

    logger.debug(args)

    siyuan = Siyuan(args.url, args.token, args.verify, args.dry_run)

    # 交互式获取笔记本 ID
    target_notebook_id = ''
    if args.notebook_id:
        target_notebook_id = args.notebook_id
    elif args.interactive or not args.notebook_id:
        target_notebook_id = choose_notebook(siyuan)

    # 开始上传文件
    for file in args.files:
        if file.endswith(".md"):
            upload_note(siyuan, target_notebook_id, file, args.convert)
        else:
            logger.warning("please input a markdown-type file.")


if __name__ == "__main__":
    options = argparser.uploader_parser()
    run(options)
