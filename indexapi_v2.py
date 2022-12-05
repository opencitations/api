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
    header = res[0]
    field_idx = []
    for field in args:
        field_idx.append(header.index(field))
    for row in res[1:]:
        for idx in field_idx:
            t, v = row[idx]
            row[idx] = t, unquote(v)
    return res, True

def generate_id_search(ids:str):
    id_searches = list()
    r = __meta_parser(ids)
    ids_to_search = ids.split('__')
    if r is not None and not all([i in ("", None) for i in r]):
        ids_to_search = [identifier for identifier in r[0]['id'].split() if not identifier.startswith('meta:')]
    for identifier in ids_to_search:
        scheme_literal_value = identifier.split(':')
        scheme = scheme_literal_value[0].lower()
        literal_value = quote(scheme_literal_value[1])
        literal_value = literal_value.lower() if scheme == 'doi' else literal_value
        if scheme == 'doi':
            id_searches.append(f'"http://dx.doi.org/{literal_value}"')
        elif scheme in {'pmid', 'pmcid'}:
            id_searches.append(f'"https://pubmed.ncbi.nlm.nih.gov/{literal_value}"')
    ids_search = ' '.join(id_searches)
    return ids_search, 

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

def find_all_ids(ids):
    pass

def metadata(res, *args):
    header = res[0]
    id_field = header.index("id")
    citation_field = header.index("citation")
    reference_field = header.index("reference")
    additional_fields = ["author", "editor", "pub_date", "title", "venue", "volume", "issue", "page"]
    header.extend(additional_fields)
    rows_to_remove = []
    for row in res[1:]:
        starting_ids = [row[id_field][1]]
        citations = row[citation_field][1].split('; ')
        references = row[reference_field][1].split('; ')
        to_be_search_by_meta = set(starting_ids + citations + references)
        r = __meta_parser('__'.join(to_be_search_by_meta))
        if r is None or all([i in ("", None) for i in r]):
            rows_to_remove.append(row)
        else:
            for field, sequence in {citation_field: citations, reference_field: references}.items():
                new_sequence = set()
                for real_id in sequence:
                    for metadata in r:
                        metadata_id = metadata['id'].split()
                        if real_id in metadata_id:
                            new_sequence.add([identifier for identifier in metadata_id if identifier.startswith('meta:')][0])
                row[field] = ('; '.join(new_sequence), '; '.join(new_sequence))
            for metadata in r:
                all_ids = metadata['id'].split()
                if set(starting_ids).intersection(all_ids):
                    row[id_field] = ('; '.join(all_ids), '; '.join(all_ids))
                    row.extend([
                        metadata["author"], metadata["editor"], 
                        metadata["date"], metadata["title"], 
                        metadata["venue"], metadata["volume"], 
                        metadata["issue"], metadata["page"]])
    for row in rows_to_remove:
        res.remove(row)
    return res, True

def __meta_parser(doi):
    api = "https://test.opencitations.net/meta/api/v1/metadata/%s"
    try:
        r = get(api % doi, timeout=30)
        if r.status_code == 200:
            return loads(r.text)
    except Exception as e:
        print(e)
        pass  # do nothing
    except Exception as e:
        pass  # do nothing
    except Exception as e:
        pass  # do nothing

def oalink(res, *args):
    base_api_url = "https://api.unpaywall.org/v2/%s?email=contact@opencitations.net"
    # id, reference, citation_count
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