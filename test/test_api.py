#!python
# Copyright 2022, Arcangelo Massari <arcangelo.massari@unibo.it>
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

import json
import unittest
from ramose import APIManager

CONFIG = 'index_v2.hf'
api_manager = APIManager([CONFIG])
api_base = 'http://127.0.0.1:8080/api/v1'

class test_API(unittest.TestCase):
    def test_metadata(self):
        operation_url = 'metadata'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1016/j.compedu.2018.11.010; meta:br/06220662347",
                "citation_count": "2",
                "citation": "meta:br/06150578485; meta:br/06150578417",
                "reference": "meta:br/06901039881; meta:br/062403286732; meta:br/06150903011",
                "author": "Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan",
                "editor": "",
                "pub_date": "2019-03",
                "title": "Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience",
                "venue": "Computers & Education [issn:0360-1315]",
                "volume": "130",
                "issue": "",
                "page": "81-93",
                "oa_link": ""
            }
        ]
        results = [{k: '; '.join(sorted(v.split('; ')))} if k in {'citation', 'author', 'reference', 'id'} else {k:v} for result in json.loads(results) for k, v in result.items()]
        result_expected = [{k: '; '.join(sorted(v.split('; ')))} if k in {'citation', 'author', 'reference', 'id'} else {k:v} for result in result_expected for k, v in result.items()]
        format_expected = 'application/json'
        output = status, results, format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_references(self):
        operation_url = 'references'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "oci": "coci => 02001000808360107040263060509063601050101360136000102000202-0200101010136193701030605630207020937020000000308033733; doci => 02001000808360107040263060509063601050101360136000102000202-0200101010136193701030605630207020937020000000308033733",
                "citing": "coci => doi:10.1016/j.compedu.2018.11.010; doci => doi:10.1016/j.compedu.2018.11.010",
                "cited": "coci => doi:10.1111/j.1365-2729.2010.00383.x; doci => doi:10.1111/j.1365-2729.2010.00383.x",
                "creation": "coci => 2020-03; doci => 2020-03",
                "timespan": "coci => P9Y3M; doci => P9Y3M",
                "journal_sc": "coci => no; doci => no",
                "author_sc": "coci => no; doci => no"
            },
            {
                "oci": "coci => 02001000808360107040263060509063601050101360136000102000209-02001000007362801010400096300000663060809036300",
                "citing": "coci => doi:10.1016/j.compedu.2018.11.010",
                "cited": "coci => doi:10.1007/s11409-006-6893-0",
                "creation": "coci => 2020-03",
                "timespan": "coci => P14Y0M",
                "journal_sc": "coci => no",
                "author_sc": "coci => no"
            },
            {
                "oci": "doci => 02001000808360107040263060509063601050101360136000102000307-0200101010136193701030605630209020937020000053700020200053733",
                "citing": "doci => doi:10.1016/j.compedu.2018.11.010",
                "cited": "doci => doi:10.1111/j.1365-2929.2005.02205.x",
                "creation": "doci => 2020-03",
                "timespan": "doci => P14Y8M",
                "journal_sc": "doci => no",
                "author_sc": "doci => no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['oci']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['oci']), format_expected
        self.assertEqual(output, expected_output)

    def test_citations(self):
        operation_url = 'citations'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "oci": "coci => 02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100",
                "citing": "coci => doi:10.1088/1742-6596/1511/1/012022",
                "cited": "coci => doi:10.1016/j.compedu.2018.11.010",
                "creation": "coci => 2020-03",
                "timespan": "coci => P1Y0M",
                "journal_sc": "coci => no",
                "author_sc": "coci => no"
            },
            {
                "oci": "doci => 02001000808360107040263060509063601050101360136000102000307-020010209070336181914281437020001033702010810",
                "citing": "doci => doi:10.1088/1742-6596/1511/1/012037",
                "cited": "doci => doi:10.1016/j.compedu.2018.11.010",
                "creation": "doci => 2020-03",
                "timespan": "doci => P6Y5M",
                "journal_sc": "doci => no",
                "author_sc": "doci => no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['oci']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['oci']), format_expected
        self.assertEqual(output, expected_output)

    def test_citation_count(self):
        operation_url = 'citation-count'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "count": "2"
            }
        ]
        format_expected = 'application/json'
        output = status, json.loads(results), format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_reference_count(self):
        operation_url = 'reference-count'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "count": "3"
            }
        ]
        format_expected = 'application/json'
        output = status, json.loads(results), format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)