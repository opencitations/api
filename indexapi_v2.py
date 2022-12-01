#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
# Copyright (c) 2022, Arcangelo Massari <arcangelo.massari@unibo.it>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

__author__ = 'essepuntato'
from urllib.parse import quote, unquote
from requests import get
from json import loads


def lower(s):
    return s.lower(),

def encode(s):
    return quote(s),

def decode_doi(res, *args):
    print(*args)
    header = res[0]
    field_idx = []
    for field in args:
        field_idx.append(header.index(field))
    for row in res[1:]:
        for idx in field_idx:
            t, v = row[idx]
            row[idx] = t, unquote(v)
    return res, True

def merge(res, *args):
    final_result = []
    header = res[0]
    final_result.append(header)
    prefix_idx = header.index(args[0])
    citing_idx = header.index(args[1])
    cited_idx = header.index(args[2])
    citations = {}
    row_idx = 0
    for row in res[1:]:
        source = row[prefix_idx][1]
        citation = row[citing_idx][1], row[cited_idx][1]
        for idx in range(len(header)):
            t, v = row[idx]
            row[idx] = t, source.replace("/", " => ") + v
        if citation in citations:
            processed_row = citations[citation]
            for idx in range(len(header)):
                t, v = final_result[processed_row][idx]
                final_result[processed_row][idx] = t, v + "; " + row[idx][1]
        else:
            row_idx += 1
            citations[citation] = row_idx
            final_result.append(list(row))
    for row in final_result:
        row.pop(prefix_idx)
    return final_result, False

def split_ids(s):
    return "\"%s\"" % "\" \"".join(s.split("__")),

def metadata(res, *args):
    header = res[0]
    doi_field = header.index("id")
    additional_fields = ["author", "pub_date", "title", "venue", "volume", "issue", "page"]
    header.extend(additional_fields)
    rows_to_remove = []
    for row in res[1:]:
        citing_doi = row[doi_field][1]
        r = __meta_parser(citing_doi)
        if r is None or all([i in ("", None) for i in r]):
            rows_to_remove.append(row)
        else:
            row.extend(r)
    for row in rows_to_remove:
        res.remove(row)
    return res, True

def __meta_parser(doi):
    api = "https://test.opencitations.net/meta/api/v1/metadata/doi:%s"
    try:
        r = get(api % doi, timeout=30)
        if r.status_code == 200:
            json_res = loads(r.text)[0]
            authors = json_res["author"]
            pub_date = json_res["date"]
            title = json_res["title"]
            venue = json_res["venue"]
            volume = json_res["volume"]
            issue = json_res["issue"]
            page = json_res["page"]
            return [authors, pub_date, title, venue, volume, issue, page]
    except Exception as e:
        print(e)
        pass  # do nothing

    except Exception as e:
        pass  # do nothing

    except Exception as e:
        pass  # do nothing

def oalink(res, *args):
    base_api_url = "https://api.unpaywall.org/v2/%s?email=contact@opencitations.net"
    # doi, reference, citation_count
    header = res[0]
    doi_field = header.index("id")
    additional_fields = ["oa_link"]
    header.extend(additional_fields)
    for row in res[1:]:
        citing_doi = row[doi_field][1]
        try:
            r = get(base_api_url % citing_doi,
                    headers={"User-Agent": "COCI REST API (via OpenCitations - "
                                           "http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=30)
            if r.status_code == 200:
                res_json = loads(r.text)
                if "best_oa_location" in res_json and res_json["best_oa_location"] is not None and \
                        "url" in res_json["best_oa_location"]:
                    row.append(res_json["best_oa_location"]["url"])
                else:
                    row.append("")  # empty element
            else:
                row.append("")  # empty element
        except Exception as e:
            row.append("")  # empty element
    return res, True