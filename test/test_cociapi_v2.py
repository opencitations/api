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

import json
import socket
import time
import unittest
from subprocess import Popen

from psutil import AccessDenied, process_iter
from ramose import APIManager

CONFIG = 'coci_v2.hf'
api_manager = APIManager([CONFIG])
api_base = 'http://127.0.0.1:8083/api/v2'

class test_cociapi_v2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if not s.connect_ex(('localhost', 3001)) == 0:
                Popen(['java', '-server', '-Xmx4g', F'-Dcom.bigdata.journal.AbstractJournal.file=test/meta.jnl',f'-Djetty.port=3001', '-jar', f'test/blazegraph.jar'])
                time.sleep(10)

    def test_metadata(self):
        operation_url = 'metadata'
        request = '10.1016/j.compedu.2018.11.010'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
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
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)