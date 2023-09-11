#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
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
from rdflib import Graph, URIRef
from re import sub,findall
from json import loads


def lower(s):
    return s.lower(),


def encode(s):
    return quote(s),


def decode_doi(res, *args):
    header = res[0]
    field_idx = []

    for field in args:
        field_idx.append(header.index(field))

    for row in res[1:]:
        for idx in field_idx:
            t, v = row[idx]
            row[idx] = t, unquote(v)

    return res, True


def decode_pmid(res, *args):
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


def split_dois(s):
    return "\"%s\"" % "\" \"".join(s.split("__")),

def split_dois2omids(s):
    #return "\"%s\"" % "\" \"".join([__get_omid_of_doi(d) for d in s.split("__")]),
    return " ".join(["<https://w3id.org/oc/meta/br/"+str(__get_omid_of_doi(d))+">" for d in s.split("__")]),



def doi2omid(s):
    return __get_omid_of_doi(s),

def __get_omid_of_doi(s):
    api = "https://test.opencitations.net/meta/api/v1/metadata/doi:%s"
    try:
        r = get(api % s,
                headers={"User-Agent": "INDEX REST API (via OpenCitations - http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=60)
        if r.status_code == 200:
            json_res = loads(r.text)
            if len(json_res) > 0:
                #take the one and only result given back by META
                body = json_res[0]
                matches = findall(r'omid:br/[\dA-Za-z/]+', body["id"])
                if matches:
                    return matches[0].replace("omid:br/","")

    except Exception as e:
        return ""
    return ""

def metadata(res, *args):
    header = res[0]
    field_idx = []
    if len(args) > 0:
        for field in args:
            field_idx.append(header.index(field))

    field_idx = [header.index("val")]

    additional_fields = ["author", "year", "pub_date", "title",
                         "source_title", "volume", "issue", "page", "source_id"]

    header.extend(additional_fields)

    rows_to_remove = []

    for row in res[1:]:

        for f in field_idx:
            # org value: <https://w3id.org/oc/meta/br/06NNNNNN>
            entity = row[f][1].split("oc/meta/")[1][:-1]

            # ["author", "year", "pub_date", "title", "source_title", "volume", "issue", "page", "source_id"]
            r = __ocmeta_parser(entity,"omid")
            if r is None or all([i in ("", None) for i in r]):
                rows_to_remove.append(row)
            else:
                # remove "pub_date"
                #r = r[:1] + r[2:]
                row.extend(r)

    for row in rows_to_remove:
        res.remove(row)

    return res, True

# args must contain the [[citing]] and [[cited]]
def citations_info(res, *args):
    header = res[0]
    fields = {"citing":header.index(args[0]), "cited": header.index(args[1])}
    index_meta = {}

    additional_fields = ["creation", "timespan", "journal_sc","author_sc"]
    header.extend(additional_fields)

    for row in res[1:]:
        entities_data = {"citing":None,"cited":None}
        for f in fields:

            f_col = fields[f]
            # org value: <https://w3id.org/oc/meta/br/06NNNNNN>
            entity = row[f_col][1].split("oc/meta/")[1][:-1]

            if f == "cited":
                continue


            # ["author", "year", "pub_date", "title", "source_title", "volume", "issue", "page", "source_id"]
            r = __ocmeta_parser(entity,"omid")
            index_meta[entity] = r

            entities_data[f] = r

        # process and elaborate additional fields
        creation = entities_data["citing"][1]

        row.extend([
            creation,
            "",
            "",
            ""
        ])

        #row.extend(["","","",""])

    return res, True


def __get_issn(body):
    cur_id = ""
    if "ISSN" in body and len(body["ISSN"]):
        cur_id = "; ".join("issn:" + cur_issn for cur_issn in body["ISSN"])
    return __normalise(cur_id)


def __get_isbn(body):
    cur_id = ""
    if "ISBN" in body and len(body["ISBN"]):
        cur_id = "; ".join("isbn:" + cur_issn for cur_issn in body["ISBN"])
    return __normalise(cur_id)


def __get_id(body, f_list):
    cur_id = ""
    for f in f_list:
        if cur_id == "":
            cur_id = f(body)
    return __normalise(cur_id)


def __create_title_from_list(title_list):
    cur_title = ""

    for title in title_list:
        strip_title = title.strip()
        if strip_title != "":
            if cur_title == "":
                cur_title = strip_title
            else:
                cur_title += " - " + strip_title

    return __create_title(cur_title)


def __create_title(cur_title):
    return __normalise(cur_title.title())


def __normalise(o):
    if o is None:
        s = ""
    else:
        s = str(o)
    return sub("\s+", " ", s).strip()

def __ocmeta_parser(doi,pre="doi"):
    api = "http://127.0.0.1/meta/api/v1/metadata/"+pre+":%s"

    try:
        r = get(api % doi,
                headers={"User-Agent": "INDEX REST API (via OpenCitations - http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=60)
        if r.status_code == 200:
            json_res = loads(r.text)
            if len(json_res) > 0:
                #take the one and only result given back by META
                body = json_res[0]

                authors = []
                if "author" in body:
                    if body["author"] != "":
                        for author in body["author"].split(";"):
                            author_string = author
                            author_orcid = findall(r"orcid\:([\d\-^\]]{1,})",author)
                            author_ids = findall(r"\[.{1,}\]",author)
                            if len(author_ids) > 0:
                                author_string = author.replace(author_ids[0],"").strip()
                                if len(author_orcid) > 0:
                                    author_string = author_string+", "+author_orcid[0].strip()
                            if author_string is not None:
                                authors.append(__normalise(author_string))

                source_title = ""
                source_id = ""
                if "venue" in body:
                    if body["venue"] != "":
                        source_title_string = body["venue"]
                        source_issn = findall(r"(issn\:[\d\-^\]]{1,})",source_title_string)
                        source_isbn = findall(r"(isbn\:[\d\-^\]]{1,})",source_title_string)
                        source_ids = findall(r"\[.{1,}\]",source_title_string)
                        if len(source_ids) > 0:
                            source_title_string = source_title_string.replace(source_ids[0],"").strip()
                        if len(source_issn) > 0:
                            source_id = source_issn[0]
                        elif len(source_isbn) > 0:
                            source_id = source_isbn[0]
                        source_title = source_title_string

                year = ""
                pub_date = ""
                if "pub_date" in body:
                    pub_date = __normalise(body["pub_date"])
                    if len(body["pub_date"]) >= 4:
                        year = __normalise(body["pub_date"][:4])

                title = ""
                if "title" in body:
                    title = body["title"]

                volume = ""
                if "volume" in body:
                    volume = __normalise(body["volume"])

                issue = ""
                if "issue" in body:
                    issue = __normalise(body["issue"])

                page = ""
                if "page" in body:
                    page = __normalise(body["page"])

                # ["author", "year", "pub_date", "title", "source_title", "volume", "issue", "page", "source_id"]
                return ["; ".join(authors),year,pub_date,title,source_title,source_id,volume,issue,pages]

    except Exception as e:
        # ["author", "year", "pub_date", "title", "source_title", "volume", "issue", "page", "source_id"]
        return ["","","","","","","","",""]

def __crossref_parser(doi):
    api = "https://api.crossref.org/works/%s"

    try:
        r = get(api % doi,
                headers={"User-Agent": "COCI REST API (via OpenCitations - http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=30)
        if r.status_code == 200:
            json_res = loads(r.text)
            if "message" in json_res:
                body = json_res["message"]

                authors = []
                if "author" in body:
                    for author in body["author"]:
                        author_string = None
                        if "family" in author:
                            author_string = author["family"].title()
                            if "given" in author:
                                author_string += ", " + author["given"].title()
                                if "ORCID" in author:
                                    author_string += ", " + \
                                        author["ORCID"].replace(
                                            "http://orcid.org/", "")
                        if author_string is not None:
                            authors.append(__normalise(author_string))

                year = ""
                if "issued" in body and "date-parts" in body["issued"] and len(body["issued"]["date-parts"]) and \
                        len(body["issued"]["date-parts"][0]):
                    year = __normalise(body["issued"]["date-parts"][0][0])

                title = ""
                if "title" in body:
                    title = __create_title_from_list(body["title"])

                source_title = ""
                if "container-title" in body:
                    source_title = __create_title_from_list(
                        body["container-title"])

                volume = ""
                if "volume" in body:
                    volume = __normalise(body["volume"])

                issue = ""
                if "issue" in body:
                    issue = __normalise(body["issue"])

                page = ""
                if "page" in body:
                    page = __normalise(body["page"])

                source_id = ""
                if "type" in body:
                    if body["type"] == "book-chapter":
                        source_id = __get_isbn(body)
                    else:
                        source_id = __get_issn(body)
                else:
                    source_id = __get_id(body, [__get_issn, __get_isbn])

                return ["; ".join(authors), year, title, source_title, volume, issue, page, source_id]

    except Exception as e:
        return ["", "", "", "", "", "", "", ""]


def __datacite_parser(doi):
    api = "https://api.datacite.org/works/%s"

    try:
        r = get(api % doi,
                headers={"User-Agent": "COCI REST API (via OpenCitations - "
                                       "http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=30)
        if r.status_code == 200:
            json_res = loads(r.text)
            if "data" in json_res and "attributes" in json_res["data"]:
                body = json_res["data"]["attributes"]

                authors = []
                if "author" in body:
                    for author in body["author"]:
                        author_string = None
                        if "family" in author:
                            author_string = author["family"].title()
                            if "given" in author:
                                author_string += ", " + author["given"].title()
                                if "ORCID" in author:
                                    author_string += ", " + \
                                        author["ORCID"].replace(
                                            "http://orcid.org/", "")
                        if author_string is not None:
                            authors.append(__normalise(author_string))

                year = ""
                if "published" in body:
                    year = __normalise(body["published"])

                title = ""
                if "title" in body:
                    title = __create_title(body["title"])

                source_title = ""
                if "container-title" in body:
                    source_title = __create_title(body["container-title"])

                volume = ""
                issue = ""
                page = ""
                source_id = ""
                return ["; ".join(authors), year, title, source_title, volume, issue, page, source_id]

    except Exception as e:
        return ["", "", "", "", "", "", "", ""]


def oalink(res, *args):
    base_api_url = "https://api.unpaywall.org/v2/%s?email=contact@opencitations.net"

    # doi, reference, citation_count
    header = res[0]
    doi_field = header.index("doi")
    additional_fields = ["oa_link"]

    header.extend(additional_fields)

    for row in res[1:]:
        row.append("")  # empty element
        # citing_doi = row[doi_field][1]
        #
        # try:
        #     r = get(base_api_url % citing_doi,
        #             headers={"User-Agent": "COCI REST API (via OpenCitations - "
        #                                    "http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=30)
        #     if r.status_code == 200:
        #         res_json = loads(r.text)
        #         if "best_oa_location" in res_json and res_json["best_oa_location"] is not None and \
        #                 "url" in res_json["best_oa_location"]:
        #             row.append(res_json["best_oa_location"]["url"])
        #         else:
        #             row.append("")  # empty element
        #     else:
        #         row.append("")  # empty element
        # except Exception as e:
        #     row.append("")  # empty element

    return res, True

def oc_coci_references(res, *args):
    api = "http://127.0.0.1/index/coci/api/v1/references/%s"

    header = res[0]
    doi_field = header.index("doi")
    additional_fields = ["reference"]

    header.extend(additional_fields)

    for row in res[1:]:
        citing_doi = row[doi_field][1]

        try:
            r = get(api % citing_doi, headers={"User-Agent": "COCI REST API (via OpenCitations - http://opencitations.net; mailto:contact@opencitations.net)"}, timeout=30)
            if r.status_code == 200:
                cited_dois = []
                res_json = loads(r.text)
                if len(res_json) > 0:
                    for item in res_json:
                        cited_dois.append(item["cited"])
                    row.append("; ".join(cited_dois))  # list of dois
                else:
                    row.append("")  # empty element
            else:
                row.append("")  # empty element
        except Exception as e:
            row.append("")  # empty element

    return res, True
