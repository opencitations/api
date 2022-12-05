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
            {'id': 'doi:10.1016/j.compedu.2018.11.010; meta:br/06220662347', 
            'citation_count': '3', 
            'citation': 'meta:br/06150578417; meta:br/06150578486; meta:br/06150578485', 
            'reference': 'meta:br/06150903011; meta:br/061701938723; meta:br/062403286732', 
            'author': 'Voogt, Joke [orcid:0000-0001-5035-9263]; Smits, Anneke [orcid:0000-0003-4396-7177]; Farjon, Daan', 
            'editor': '', 
            'pub_date': '2019-03', 
            'title': 'Technology Integration Of Pre-Service Teachers Explained By Attitudes And Beliefs, Competency, Access, And Experience', 
            'venue': 'Computers & Education [issn:0360-1315]', 
            'volume': "130", 
            'issue': '', 
            'page': '81-93', 
            'oa_link': ''}]
        results = [{k: '; '.join(sorted(v.split('; ')))} if k in {'citation', 'author', 'reference', 'id'} else {k:v} for result in json.loads(results) for k, v in result.items()]
        result_expected = [{k: '; '.join(sorted(v.split('; ')))} if k in {'citation', 'author', 'reference', 'id'} else {k:v} for result in result_expected for k, v in result.items()]
        format_expected = 'application/json'
        output = status, results, format
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)