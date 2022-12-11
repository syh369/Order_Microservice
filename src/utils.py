"""
{
   "metadata": {
      "result_set": {
         "count": 25,
         "offset": 0,
         "limit": 25,
         "total": 77
      },
      ...
"""
import math

PAGE = 1
PAGESIZE = 10


def wrap_pagination(results, pagesize, page, total):
    header = dict()
    header["count"] = len(results)
    header["pagesize"], header["page"] = pagesize, page
    header["total"] = total
    header["total_page"] = math.ceil(total / pagesize)
    return {"metadata": {"result_set": header}, "results": results}


def wrap_link(href: str, rel: str):
    link = dict()
    link["href"] = href
    link["rel"] = rel
    return link


def wrap_pg_dict(page=PAGE, pagesize=PAGESIZE, enable=False):
    if not page:
        page = PAGE
    if not pagesize:
        pagesize = PAGESIZE
    limit, offset = pagesize, (page - 1) * pagesize
    pg_dict = {"limit": limit,
               "offset": offset,
               "pg_flag": enable}
    return page, pagesize, pg_dict
