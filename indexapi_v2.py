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

import re
from json import loads
from urllib.parse import quote, unquote

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from requests import get

IDS_WITHIN_SQUARE_BRACKETS = '\[((?:[^\s]+:[^\s]+)(?:\s[^\s]+:[^\s]+)*)\]'

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

def split_dois(s):
    return "\"%s\"" % "\" \"".join(s.split("__")),

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

def metadata(res):
    header = res[0]
    id_field = header.index("id")
    citation_field = header.index("citation")
    reference_field = header.index("reference")
    additional_fields = ["author", "editor", "pub_date", "title", "venue", "volume", "issue", "page"]
    header.extend(additional_fields)
    rows_to_remove = []
    processed_metaids = set()
    identifiers = set()
    for row in res[1:]:
        identifiers.add(row[id_field][1])
        identifiers.update(row[citation_field][1].split('; '))
        identifiers.update(row[reference_field][1].split('; '))
    r = __meta_parser('__'.join(identifiers))
    index_by_id = index_meta_results(r)
    for row in res[1:]:
        starting_ids = [row[id_field][1]]
        citations = row[citation_field][1].split('; ')
        references = row[reference_field][1].split('; ')
        relevant_index = index_by_id[starting_ids[0]]
        metadata = r[relevant_index['index']]
        all_ids = metadata['id'].split()
        metaid = relevant_index['metaid']
        if metaid in processed_metaids:
            rows_to_remove.append(row)
        else:
            processed_metaids.add(metaid)
            row[id_field] = (' '.join(all_ids), ' '.join(all_ids))
            row.extend([
                (metadata["author"], metadata["author"]),
                (metadata["editor"], metadata["editor"]), 
                (metadata["date"], metadata["date"]),
                (metadata["title"], metadata["title"]), 
                (metadata["venue"], metadata["venue"]),
                (metadata["volume"], metadata["volume"]), 
                (metadata["issue"], metadata["issue"]),
                (metadata["page"], metadata["page"])])
            for field, sequence in {citation_field: citations, reference_field: references}.items():
                new_sequence = set()
                for real_id in sequence:
                    new_sequence.add(index_by_id[real_id]['metaid'])
                row[field] = (' '.join(new_sequence), ' '.join(new_sequence))
    return res, True

def index_meta_results(meta_results: list) -> dict:
    index_by_id = dict()
    for i, metadata in enumerate(meta_results):
        all_ids = metadata['id'].split()
        metaid = [identifier for identifier in all_ids if identifier.startswith('meta:')][0]
        for identifier in all_ids:
            index_by_id[identifier] = {'index': i, 'metaid': metaid}
    return index_by_id

def process_citations(res, *args):
    header = res[0]
    input_field = header.index(args[0])
    other_field = header.index(args[1])
    additional_fields = ['creation', 'timespan', 'journal_sc', 'author_sc']
    header.extend(additional_fields)
    identifiers = set()
    for row in res[1:]:
        identifiers.add(row[input_field][1])
        identifiers.add(row[other_field][1])
    r = __meta_parser('__'.join(identifiers))
    index_by_id = index_meta_results(r)
    input_id = res[1][input_field][1]
    input_id_index = index_by_id[input_id]['index']
    input_id_metadata = r[input_id_index]
    input_creation = input_id_metadata['date']
    input_venue_ids = re.search(IDS_WITHIN_SQUARE_BRACKETS, input_id_metadata['venue'])
    input_venue_ids = set(input_venue_ids.group(1).split()) if input_venue_ids else set()
    input_authors_ids = get_all_authors_ids(input_id_metadata['author'])
    for row in res[1:]:
        row[input_field] = (input_id_metadata['id'], input_id_metadata['id'])
        other_id = row[other_field][1]
        other_id_index = index_by_id[other_id]['index']
        other_metadata = r[other_id_index]
        row[other_field] = (other_metadata['id'], other_metadata['id'])
        other_creation = other_metadata['date']
        other_venue_ids = re.search(IDS_WITHIN_SQUARE_BRACKETS, other_metadata['venue'])
        journal_sc = 'no'
        author_sc = 'no'
        if other_venue_ids and input_venue_ids:
            other_venue_ids = other_venue_ids.group(1).split()
            if input_venue_ids.intersection(other_venue_ids):
                journal_sc = 'yes'
        other_authors_ids = get_all_authors_ids(other_metadata['author'])
        if input_authors_ids.intersection(other_authors_ids):
            author_sc = 'yes'
        timespan = calculate_timespan(input_creation, other_creation) if args[0] == 'citing' else calculate_timespan(other_creation, input_creation)
        row.extend([
            (input_creation, input_creation),
            (timespan, timespan),
            (journal_sc, journal_sc),
            (author_sc, author_sc)])
    return res, True

def calculate_timespan(citing_pub_date: str, cited_pub_date: str) -> str:
    citing_pub_datetime = parse(citing_pub_date)
    cited_pub_datetime = parse(cited_pub_date)
    delta = relativedelta(citing_pub_datetime, cited_pub_datetime)
    result = ''
    if (
        delta.years < 0
        or (delta.years == 0 and delta.months < 0)
        or (
            delta.years == 0
            and delta.months == 0
            and delta.days < 0
        )
    ):
        result += '-'
    result += 'P%sY' % abs(delta.years)
    result += '%sM' % abs(delta.months)
    result += '%sD' % abs(delta.days)
    return result

def get_all_authors_ids(authors: str) -> set:
    all_authors_ids = set()
    authors_list = authors.split('; ')
    for author in authors_list:
        author_ids = re.search(IDS_WITHIN_SQUARE_BRACKETS, author)
        if author_ids:
            all_authors_ids.update(author_ids.group(1).split())
    return all_authors_ids
        
def count_metaids(res):
    r = __meta_parser('__'.join([row[0][0] for row in res[1:]]))
    return [["count"], [(len(r), str(len(r)))]], True

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