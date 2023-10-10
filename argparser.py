#!/usr/bin/python3
# pylint: disable=C0116

"""命令解析器

file: /argparser.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-10-10
"""

import argparse


def root_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-u', '--url',
                        help='SiYuan host URL', required=True)
    parser.add_argument('-t', '--token', required=True)
    parser.add_argument('-g', '--ignore-tls', dest='verify',
                        action='store_true', help='do not verify certificate')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='do not send any requests')

    parser.add_argument('--version',
                        action='store_true', help="print the program version information")
    parser.add_argument('-l', '--log-level',
                        default='INFO', help="define the loguru level",
                        choices=["TRACE", "DEBUG", "INFO", "SUCCESS",
                                 "WARNING",  "ERROR", "CRITICAL"])
    parser.add_argument('-v', '--verbose',
                        action='store_true', help="print the detail information. eq -l DEBUG")

    return parser


def uploader_argument(parser: argparse.ArgumentParser):
    parser.add_argument('files', metavar='FILE', nargs='*')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', '--notebook-id',
                       metavar='ID')
    group.add_argument('-i', '--interactive',
                       action='store_true', help='interactive choose your notebook')


def notebook_argument(parser: argparse.ArgumentParser):
    sub_args = parser.add_subparsers()

    sub_parser = sub_args.add_parser('create')
    sub_parser.add_argument('-n', '--name', help='create your nootbook')


def helper_parser():
    parser = argparse.ArgumentParser(
        description="SiYuan helper", parents=[root_parser()])
    sub_args = parser.add_subparsers(help="sub commands")

    sub_parser = sub_args.add_parser(
        'upload', help="upload your markdown-type file")
    uploader_argument(sub_parser)

    sub_parser = sub_args.add_parser('notebook', help="manage your notebooks")
    notebook_argument(sub_parser)

    sub_args.add_parser('document', help="manage your documents")

    args = parser.parse_args()
    return args


def uploader_parser() -> argparse.Namespace:
    """uploader使用的参数解析器
    可用的键值: url, token, verify, dry_run, version, log_level, verbose, files, notebook_id, interactive
    """
    parser = argparse.ArgumentParser(
        description="Upload your markdown-type file to remote SiYuan host.",
        parents=[root_parser()])
    uploader_argument(parser)
    args = parser.parse_args()
    print(args)
    return args


def notebook_parser():
    parser = argparse.ArgumentParser(parents=[root_parser()])
    notebook_argument(parser)

    args = parser.parse_args()
    return args
