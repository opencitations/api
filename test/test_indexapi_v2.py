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
import socket
import time
import unittest
from subprocess import Popen

from ramose import APIManager

api_manager_index = APIManager(['index_v2.hf'])
api_manager_coci = APIManager(['coci_v2.hf'])
api_manager_doci = APIManager(['doci_v2.hf'])
api_base_index = 'http://127.0.0.1:8080/api/v2'
api_base_coci = 'http://127.0.0.1:8081/api/v2'
api_base_doci = 'http://127.0.0.1:8082/api/v2'

class test_indexapi_v2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if not s.connect_ex(('localhost', 3001)) == 0:
                Popen(['java', '-server', '-Xmx4g', F'-Dcom.bigdata.journal.AbstractJournal.file=test/index.jnl',f'-Djetty.port=3001', '-jar', f'test/blazegraph.jar'])
                time.sleep(10)
    
    def test_metadata_coci(self):
        operation_url = 'metadata'
        request = '10.1016/j.compedu.2018.11.010__10.1111/j.1365-2729.2010.00383.x__10.1111/j.1365-2729.2010.00383.k'
        call = "%s/%s/%s" % (api_base_coci, operation_url, request)
        op = api_manager_coci.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "citation_count": "1",
                "citation": "doi:10.1088/1742-6596/1511/1/012022",
                "reference": "doi:10.1111/j.1365-2729.2010.00383.x doi:10.1007/s11409-006-6893-0",
                "author": "Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan",
                "editor": "",
                "pub_date": "2019-03",
                "title": "Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience",
                "venue": "Computers & Education [issn:0360-1315]",
                "volume": "130",
                "issue": "",
                "page": "81-93"
            },
            {
                "id": "doi:10.1111/j.1365-2729.2010.00383.x meta:br/06150903011",
                "citation_count": "1",
                "citation": "doi:10.1016/j.compedu.2018.11.010",
                "reference": "",
                "author": "Zhu, Chang [orcid:0000-0002-0057-275X]; Valcke, Martin [orcid:0000-0001-9544-4197]; Tondeur, Jo [orcid:0000-0002-3807-5361]; Sang, Guoyuan; Van Braak, Johan",
                "editor": "",
                "pub_date": "2010-12-07",
                "title": "Predicting ICT Integration Into Classroom Teaching In Chinese Primary Schools: Exploring The Complex Interplay Of Teacher-Related Variables",
                "venue": "Journal Of Computer Assisted Learning [issn:1365-2729 issn:0266-4909]",
                "volume": "27",
                "issue": "2",
                "page": "160-172"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_doci(self):
        operation_url = 'metadata'
        request = '10.1016/j.compedu.2018.11.010__10.1111/j.1365-2729.2010.00383.x__10.1111/j.1365-2729.2010.00383.k'
        call = "%s/%s/%s" % (api_base_doci, operation_url, request)
        op = api_manager_doci.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "citation_count": "0",
                "citation": "",
                "reference": "",
                "author": "Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan",
                "editor": "",
                "pub_date": "2019-03",
                "title": "Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience",
                "venue": "Computers & Education [issn:0360-1315]",
                "volume": "130",
                "issue": "",
                "page": "81-93"
            },
            {
                "id": "doi:10.1111/j.1365-2729.2010.00383.x meta:br/06150903011",
                "citation_count": "0",
                "citation": "",
                "reference": "",
                "author": "Zhu, Chang [orcid:0000-0002-0057-275X]; Valcke, Martin [orcid:0000-0001-9544-4197]; Tondeur, Jo [orcid:0000-0002-3807-5361]; Sang, Guoyuan; Van Braak, Johan",
                "editor": "",
                "pub_date": "2010-12-07",
                "title": "Predicting ICT Integration Into Classroom Teaching In Chinese Primary Schools: Exploring The Complex Interplay Of Teacher-Related Variables",
                "venue": "Journal Of Computer Assisted Learning [issn:1365-2729 issn:0266-4909]",
                "volume": "27",
                "issue": "2",
                "page": "160-172"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata(self):
        operation_url = 'metadata'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "citation": "meta:br/06150578485 meta:br/06150578417",
                "reference": "meta:br/06901039881 meta:br/062403286732 meta:br/06150903011",
                "author": "Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan",
                "editor": "",
                "pub_date": "2019-03",
                "title": "Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience",
                "venue": "Computers & Education [issn:0360-1315]",
                "volume": "130",
                "issue": "",
                "page": "81-93",
                "citation_count": "2"
            }
        ]
        results = [{k: '; '.join(sorted(v.split('; ')))} if k == 'author' else {k: ' '.join(sorted(v.split()))} if k in {'citation', 'reference', 'id'} else {k:v} for result in json.loads(results) for k, v in result.items()]
        result_expected = [{k: '; '.join(sorted(v.split('; ')))} if k == 'author' else {k: ' '.join(sorted(v.split()))} if k in {'citation', 'reference', 'id'} else {k:v} for result in result_expected for k, v in result.items()]
        format_expected = 'application/json'
        output = status, results, format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_non_existing_input(self):
        operation_url = 'metadata'
        request = 'doi:12.1016/j.compedu.2018.11.010__doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "citation": "meta:br/06150578485 meta:br/06150578417",
                "reference": "meta:br/06901039881 meta:br/062403286732 meta:br/06150903011",
                "author": "Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan",
                "editor": "",
                "pub_date": "2019-03",
                "title": "Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience",
                "venue": "Computers & Education [issn:0360-1315]",
                "volume": "130",
                "issue": "",
                "page": "81-93",
                "citation_count": "2"
            }
        ]
        results = [{k: '; '.join(sorted(v.split('; ')))} if k == 'author' else {k: ' '.join(sorted(v.split()))} if k in {'citation', 'reference', 'id'} else {k:v} for result in json.loads(results) for k, v in result.items()]
        result_expected = [{k: '; '.join(sorted(v.split('; ')))} if k == 'author' else {k: ' '.join(sorted(v.split()))} if k in {'citation', 'reference', 'id'} else {k:v} for result in result_expected for k, v in result.items()]
        format_expected = 'application/json'
        output = status, results, format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_references_coci(self):
        operation_url = 'references'
        request = '10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_coci, operation_url, request)
        op = api_manager_coci.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000202-0200101010136193701030605630207020937020000000308033733",
                "citing": "doi:10.1016/j.compedu.2018.11.010",
                "cited": "doi:10.1111/j.1365-2729.2010.00383.x",
                "creation": "2020-03",
                "timespan": "P9Y3M",
                "journal_sc": "no",
                "author_sc": "no"
            },
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000209-02001000007362801010400096300000663060809036300",
                "citing": "doi:10.1016/j.compedu.2018.11.010",
                "cited": "doi:10.1007/s11409-006-6893-0",
                "creation": "2020-03",
                "timespan": "P14Y0M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['id']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['id']), format_expected
        self.assertEqual(output, expected_output)

    def test_references(self):
        operation_url = 'references'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000202-0200101010136193701030605630207020937020000000308033733",
                "citing": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "cited": "doi:10.1111/j.1365-2729.2010.00383.x meta:br/06150903011",
                "creation": "2019-03",
                "timespan": "P8Y3M",
                "journal_sc": "no",
                "author_sc": "no"
            },
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000209-02001000007362801010400096300000663060809036300",
                "citing": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "cited": "doi:10.1007/s11409-006-6893-0 meta:br/062403286732",
                "creation": "2019-03",
                "timespan": "P13Y0M",
                "journal_sc": "no",
                "author_sc": "no"
            },
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000307-0200101010136193701030605630209020937020000053700020200053733",
                "citing": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "cited": "doi:10.1111/j.1365-2929.2005.02205.x meta:br/06901039881",
                "creation": "2019-03",
                "timespan": "P13Y8M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['id']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['id']), format_expected
        self.assertEqual(output, expected_output)

    def test_references_non_existing_input(self):
        operation_url = 'references'
        request = 'doi:10.1016/j.compeda.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = []
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['id']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['id']), format_expected
        self.assertEqual(output, expected_output)

    def test_citations_coci(self):
        operation_url = 'citations'
        request = '10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_coci, operation_url, request)
        op = api_manager_coci.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100",
                "citing": "doi:10.1088/1742-6596/1511/1/012022",
                "cited": "doi:10.1016/j.compedu.2018.11.010",
                "creation": "2020-03",
                "timespan": "P1Y0M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['id']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['id']), format_expected
        self.assertEqual(output, expected_output)

    def test_citations(self):
        operation_url = 'citations'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100",
                "citing": "doi:10.1088/1742-6596/1511/1/012022 meta:br/06150578485",
                "cited": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "creation": "2019-03",
                "timespan": "P0Y11M",
                "journal_sc": "no",
                "author_sc": "no"
            },
            {
                "id": "oci:02001000808360107040263060509063601050101360136000102000307-020010209070336181914281437020001033702010810",
                "citing": "doi:10.1088/1742-6596/1511/1/012037 meta:br/06150578417",
                "cited": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "creation": "2019-03",
                "timespan": "P0Y11M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, sorted(json.loads(results), key=lambda x: x['id']), format
        expected_output = status_expected, sorted(result_expected, key=lambda x: x['id']), format_expected
        self.assertEqual(output, expected_output)

    def test_citation_count(self):
        operation_url = 'citation-count'
        request = 'doi:10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
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
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
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

    def test_reference_count_non_existing_input(self):
        operation_url = 'reference-count'
        request = 'doi:10.1016/j.compeda.2018.11.010'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = []
        format_expected = 'application/json'
        output = status, json.loads(results), format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_citation_oci_coci(self):
        operation_url = 'citation'
        request = '02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100'
        call = "%s/%s/%s" % (api_base_coci, operation_url, request)
        op = api_manager_coci.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "oci": "oci:02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100",
                "citing": "doi:10.1088/1742-6596/1511/1/012022",
                "cited": "doi:10.1016/j.compedu.2018.11.010",
                "creation": "2020-03",
                "timespan": "P1Y0M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, json.loads(results), format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_citation_oci(self):
        operation_url = 'citation'
        request = '02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100'
        call = "%s/%s/%s" % (api_base_index, operation_url, request)
        op = api_manager_index.get_op(call)
        status, results, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "02001000808360107040263060509063601050101360136000102000202-0200100010636193712242225141330370200010837010137000100",
                "citing": "doi:10.1088/1742-6596/1511/1/012022 meta:br/06150578485",
                "cited": "doi:10.1016/j.compedu.2018.11.010 meta:br/06220662347",
                "creation": "2020-03-01",
                "timespan": "P0Y11M",
                "journal_sc": "no",
                "author_sc": "no"
            }
        ]
        format_expected = 'application/json'
        output = status, json.loads(results), format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)