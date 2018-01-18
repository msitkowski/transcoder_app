# -*- encoding: utf-8 -*-

"""
App starter module.

"""

try:
    from ptpython import repl as _ptpython_repl
except ImportError:
    _ptpython_repl = None


from core.acl import ACL
from core.location import Location
from core.bucket.bucket import Bucket


if __name__ == "__main__":
    if _ptpython_repl:
        _ptpython_repl.embed(globals(), locals())
