#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018, Silvio Peroni <essepuntato@gmail.com>
# Copyright (c) 2022, Arcangelo Massari <arcangelo.massari@unibo.it>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

from __future__ import annotations

__author__ = 'Arcangelo Massari'

import re
from json import loads
from typing import List, Tuple
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
    if r is not None and not all([i in ('', None) for i in r]):
        ids_to_search = [identifier for identifier in r[0]['id'].split() if not identifier.startswith('meta:')]
    for identifier in ids_to_search:
        scheme_literal_value = identifier.split(':')
        scheme = scheme_literal_value[0].lower()
        literal_value = quote(scheme_literal_value[1])
        literal_value = literal_value.lower() if scheme == 'doi' else literal_value
        if scheme == 'doi':
            id_searches.append(f'<http://dx.doi.org/{literal_value}>')
            id_searches.append(f'<https://doi.org/{literal_value}>')
        elif scheme in {'pmid', 'pmcid'}:
            id_searches.append(f'<https://pubmed.ncbi.nlm.nih.gov/{literal_value}>')
    ids_search = ' '.join(id_searches)
    return ids_search, 

def metadata(res: list, get_metadata_from_meta: str, id_schemas: str = None):
    get_metadata_from_meta = True if get_metadata_from_meta == 'True' else False
    if not res[1:]:
        return res, True
    res = replace_schemas_and_decode(res)
    header = res[0]
    id_field = header.index('id')
    citation_field = header.index('citation')
    reference_field = header.index('reference')
    additional_fields = ['author', 'editor', 'pub_date', 'title', 'venue', 'volume', 'issue', 'page']
    if get_metadata_from_meta:
        additional_fields.append('citation_count')
    header.extend(additional_fields)
    rows_to_remove = []
    processed_metaids = set()
    identifiers = set()
    for row in res[1:]:
        citation = filter(None, row[citation_field][1].split('; '))
        reference = filter(None, row[reference_field][1].split('; '))
        identifiers.add(row[id_field][1])
        if get_metadata_from_meta:
            identifiers.update(citation)
            identifiers.update(reference)
    r = __meta_parser('__'.join(identifiers))
    index_by_id = index_meta_results(r)
    for row in res[1:]:
        starting_id = [row[id_field][1]][0]
        if starting_id not in index_by_id:
            rows_to_remove.append(row)
            continue
        relevant_index = index_by_id[starting_id]
        metaid = relevant_index['metaid']
        if metaid in processed_metaids:
            rows_to_remove.append(row)
            continue
        metadata = r[relevant_index['index']]
        all_ids = metadata['id'].split()
        if get_metadata_from_meta:
            citations = row[citation_field][1].split('; ')
            references = row[reference_field][1].split('; ')
            for field, sequence in {citation_field: citations, reference_field: references}.items():
                new_sequence = set()
                for real_id in sequence:
                    if real_id in index_by_id:
                        new_sequence.add(index_by_id[real_id]['metaid'])
                row[field] = (' '.join(new_sequence), ' '.join(new_sequence))
        processed_metaids.add(metaid)
        row[id_field] = (' '.join(all_ids), ' '.join(all_ids))
        row.extend([
            (metadata['author'], metadata['author']),
            (metadata['editor'], metadata['editor']), 
            (metadata['pub_date'], metadata['pub_date']),
            (metadata['title'], metadata['title']), 
            (metadata['venue'], metadata['venue']),
            (metadata['volume'], metadata['volume']), 
            (metadata['issue'], metadata['issue']),
            (metadata['page'], metadata['page'])])
        if get_metadata_from_meta:
            row.extend([(len(row[citation_field][1].split()), len(row[citation_field][1].split()))])
    for row in rows_to_remove:
        res.remove(row)
    return res, True

def index_meta_results(meta_results: list) -> dict:
    index_by_id = dict()
    for i, metadata in enumerate(meta_results):
        all_ids = metadata['id'].split()
        metaid = [identifier for identifier in all_ids if identifier.startswith('meta:')][0]
        for identifier in all_ids:
            index_by_id[identifier] = {'index': i, 'metaid': metaid}
    return index_by_id

def replace_schemas_and_decode(res: List[List[Tuple[str, str]]]) -> list:
    new_res = [res[0]]
    for row in res[1:]:
        new_row = list()
        for row_tuple in row:
            new_el = row_tuple[1] \
                .replace('https://doi.org/', 'doi:') \
                .replace('http://dx.doi.org/', 'doi:') \
                .replace('https://pubmed.ncbi.nlm.nih.gov/', 'pmid:')
            new_row.append((new_el, unquote(new_el)))
        new_res.append(new_row)
    return new_res

def process_citations(res, *args):
    if not res[1:]:
        return res, True
    res = replace_schemas_and_decode(res)
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
    if input_id not in index_by_id:
        return [header], True
    input_id_index = index_by_id[input_id]['index']
    input_id_metadata = r[input_id_index]
    input_creation = input_id_metadata['pub_date']
    input_venue_ids = re.search(IDS_WITHIN_SQUARE_BRACKETS, input_id_metadata['venue'])
    input_venue_ids = set(input_venue_ids.group(1).split()) if input_venue_ids else set()
    input_authors_ids = get_all_authors_ids(input_id_metadata['author'])
    rows_to_remove = list()
    for row in res[1:]:
        other_id = row[other_field][1]
        if other_id not in index_by_id:
            rows_to_remove.append(row)
            continue
        row[input_field] = (input_id_metadata['id'], input_id_metadata['id'])
        other_id_index = index_by_id[other_id]['index']
        other_metadata = r[other_id_index]
        row[other_field] = (other_metadata['id'], other_metadata['id'])
        other_creation = other_metadata['pub_date']
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
    for row in rows_to_remove:
        res.remove(row)
    return res, True

def calculate_timespan(citing_pub_date: str, cited_pub_date: str) -> str:
    citing_contains_month = citing_pub_date is not None and len(citing_pub_date) >= 7
    cited_contains_month = cited_pub_date is not None and len(cited_pub_date) >= 7
    citing_contains_day = citing_pub_date is not None and len(citing_pub_date) >= 10
    cited_contains_day = cited_pub_date is not None and len(cited_pub_date) >= 10
    citing_pub_datetime = parse(citing_pub_date)
    cited_pub_datetime = parse(cited_pub_date)
    consider_months = citing_contains_month and cited_contains_month
    consider_days = citing_contains_day and cited_contains_day
    delta = relativedelta(citing_pub_datetime, cited_pub_datetime)
    result = ''
    if (
        delta.years < 0
        or (delta.years == 0 and delta.months < 0 and consider_months)
        or (
            delta.years == 0
            and delta.months == 0
            and delta.days < 0
        )
    ):
        result += '-'
    result += 'P%sY' % abs(delta.years)
    if consider_months:
        result += "%sM" % abs(delta.months)
    if consider_days:
        result += "%sD" % abs(delta.days)
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
    if not res[1:]:
        return res, True
    res = replace_schemas_and_decode(res)
    r = __meta_parser('__'.join([row[0][0] for row in res[1:]]))
    count = 0
    if r:
        count = len(r)
    return [['count'], [(count, count)]], True

def __meta_parser(doi):
    api = 'https://test.opencitations.net/meta/api/v1/metadata/%s'
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