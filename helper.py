#!/usr/bin/python3
# pylint: disable=C0116

"""思源上传助手主程序

file: /helper.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-10-13
"""

import argparser


def main():
    args = argparser.helper_parser()
    # 如果用户运行了子命令, 则执行对应函数
    if args.func:
        args.func(args)


if __name__ == "__main__":
    main()
