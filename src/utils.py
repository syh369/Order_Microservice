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


def wrap_pagination(results, pagesize, offset, total):
    header = dict()
    header["count"] = len(results)
    header["pagesize"], header["page"] = pagesize, offset
    header["total"] = total
    header["total_page"] = math.ceil(total / pagesize)
    return {"metadata": {"result_set": header}, "results": results}


def wrap_link(href: str, rel: str):
    link = dict()
    link["href"] = href
    link["rel"] = rel
    return link
