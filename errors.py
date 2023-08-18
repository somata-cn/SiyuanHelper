"""错误类型

file: /errors.py
author: somata
e-mail: somata@foxmail.com
license: Apache 2.0
date: 2023-7-17
"""


class CodeError(Exception):
    """思源笔记 Code 返回类型错误
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class StatusError(Exception):
    """思源笔记 状态码 返回类型错误
    """

    def __init__(self, status: int):
        self.status = status

    def __str__(self):
        return f"unexcept status with {self.status}"
