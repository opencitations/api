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

from ramose import APIManager

CONFIG = 'meta_v1.hf'
api_manager = APIManager([CONFIG])
api_base = 'http://127.0.0.1:8081/api/v1'

class test_metaapi_v1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if not s.connect_ex(('localhost', 3013)) == 0:
                Popen(['java', '-server', '-Xmx4g', F'-Dcom.bigdata.journal.AbstractJournal.file=test/meta.jnl',f'-Djetty.port=3013', '-jar', f'test/blazegraph.jar'])
                time.sleep(10)

    def test_metadata(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__doi:10.1088/0022-3727/39/14/017__doi:10.1162/qss_a_00023'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            },
            {
                "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne [omid:ra/0604]; Ebert, Ute [orcid:0000-0003-3891-6869 omid:ra/0605]",
                "pub_date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727 omid:br/0604]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266 omid:ra/0606]",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_order_of_authors(self):
        operation_url = 'metadata'
        request = 'doi:10.1038/sdata.2016.18'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1038/sdata.2016.18 omid:br/06101",
                "title": "Influence Of Dielectric Properties, State, And Electrodes On Electric Strength",
                "author": "Hoen, Peter-Bram 'T [orcid:0000-0003-4450-3112 omid:ra/06101]; Martone, Maryann E [orcid:0000-0002-8406-3871 omid:ra/06102]; Roos, Marco [orcid:0000-0002-8691-772X omid:ra/06103]; Swertz, Morris [orcid:0000-0002-0979-3401 omid:ra/06104]; Dumontier, Michel [orcid:0000-0003-4727-9435 omid:ra/06105]; Evelo, Chris [orcid:0000-0002-5301-3142 omid:ra/06106]; Persson, Bengt [orcid:0000-0003-3165-5344 omid:ra/06107]; Finkers, Richard [orcid:0000-0002-4368-8058 omid:ra/06108]; Wilkinson, Mark [orcid:0000-0001-6960-357X omid:ra/06109]; Mons, Barend [orcid:0000-0003-3934-0072 omid:ra/061010]; Grethe, Jeffrey [orcid:0000-0001-5212-7052 omid:ra/061011]; Waagmeester, Andra [orcid:0000-0001-9773-4008 omid:ra/061012]; Schultes, Erik Anthony [orcid:0000-0001-8888-635X omid:ra/061013]; Hooft, Rob [orcid:0000-0001-6825-9439 omid:ra/061014]; Sansone, Susanna-Assunta [orcid:0000-0001-5306-5690 omid:ra/061015]; Blomberg, Niklas [orcid:0000-0003-4155-5910 omid:ra/061016]; Aalbersberg, IJsbrand Jan [orcid:0000-0002-0209-4480 omid:ra/061017]; Goble, Carole [orcid:0000-0003-1219-2137 omid:ra/061018]; Wolstencroft, Katy [orcid:0000-0002-1279-5133 omid:ra/061019]; Groth, Paul [orcid:0000-0003-0183-6910 omid:ra/061020]; Axton, Myles [orcid:0000-0002-8042-4131 omid:ra/061021]; Van Mulligen, Erik [orcid:0000-0003-1377-9386 omid:ra/061022]; Clark, Timothy [orcid:0000-0003-4060-7360 omid:ra/061023]; Bourne, Philip E [orcid:0000-0002-7618-7292 omid:ra/061024]; Brookes, Anthony J. [orcid:0000-0001-8686-0017 omid:ra/061025]; Crosas, Mercè [orcid:0000-0003-1304-1939 omid:ra/061026]; Dillo, Ingrid [orcid:0000-0001-5654-2392 omid:ra/061027]; Velterop, Jan [orcid:0000-0002-4836-6568 omid:ra/061028]; Kuhn, Tobias [orcid:0000-0002-1267-0234 omid:ra/061029]; Gray, Alasdair [orcid:0000-0002-5711-4872 omid:ra/061030]; Edmunds, Scott C [orcid:0000-0001-6444-1436 omid:ra/061031]; Boiten, Jan-Willem [orcid:0000-0003-0327-638X omid:ra/061032]; Sengstag, Thierry [orcid:0000-0002-7516-6246 omid:ra/061033]; Zhao, Jun [orcid:0000-0001-6935-9028 omid:ra/061034]; Appleton, Gaby [orcid:0000-0003-0179-7384 omid:ra/061035]; Thompson, Mark [orcid:0000-0002-7633-1442 omid:ra/061036]; Heringa, Jaap [orcid:0000-0001-8641-4930 omid:ra/061037]; Kok, Ruben [omid:ra/061038]; Kok, Joost [orcid:0000-0002-7352-1400 omid:ra/061039]; Lusher, Scott J. [orcid:0000-0003-2401-4223 omid:ra/061040]; Mons, Albert [omid:ra/061041]; Van Schaik, Rene [omid:ra/061042]; Rocca-Serra, Philippe [orcid:0000-0001-9853-5668 omid:ra/061043]; Packer, Abel L [orcid:0000-0001-9610-5728 omid:ra/061044]; Santos, Luiz Olavo Bonino Da Silva [orcid:0000-0002-1164-1351 omid:ra/061045]; Slater, Ted [orcid:0000-0003-1386-0731 omid:ra/061046]; Baak, Arie [orcid:0000-0003-2829-6715 omid:ra/061047]; Strawn, George [omid:ra/061048]; Van Der Lei, Johan [omid:ra/061049]; Wittenburg, Peter [omid:ra/061050]; Bouwman, Jildau [omid:ra/061051]; Dumon, Olivier [orcid:0000-0001-8599-7345 omid:ra/061052]; Gonzalez-Beltran, Alejandra [orcid:0000-0003-3499-8262 omid:ra/061053]",
                "pub_date": "2016-03-15",
                "page": "3",
                "issue": "",
                "volume": "",
                "venue": "Scientific Data [issn:2052-4463 omid:br/06102]",
                "type": "journal article",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_two_schemes(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__issn:0022-3727'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            },
            {
                "id": "issn:0022-3727 omid:br/0604",
                "title": "Journal Of Physics D: Applied Physics",
                "author": "",
                "pub_date": "",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "journal",
                "publisher": "",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_metadata_two_schemes_and_metaid(self):
        operation_url = 'metadata'
        request = 'doi:10.1007/978-1-4020-9632-7__issn:0022-3727__omid:br/0602'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne [omid:ra/0604]; Ebert, Ute [orcid:0000-0003-3891-6869 omid:ra/0605]",
                "pub_date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727 omid:br/0604]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266 omid:ra/0606]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            },
            {
                "id": "issn:0022-3727 omid:br/0604",
                "title": "Journal Of Physics D: Applied Physics",
                "author": "",
                "pub_date": "",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "journal",
                "publisher": "",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:x['pub_date']), format
        result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:x['pub_date'])
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_author(self):
        operation_url = 'author'
        request = '0000-0002-0209-4480'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1038/sdata.2016.18 omid:br/06101",
                "title": "Influence Of Dielectric Properties, State, And Electrodes On Electric Strength",
                "author": "Hoen, Peter-Bram 'T [orcid:0000-0003-4450-3112 omid:ra/06101]; Martone, Maryann E [orcid:0000-0002-8406-3871 omid:ra/06102]; Roos, Marco [orcid:0000-0002-8691-772X omid:ra/06103]; Swertz, Morris [orcid:0000-0002-0979-3401 omid:ra/06104]; Dumontier, Michel [orcid:0000-0003-4727-9435 omid:ra/06105]; Evelo, Chris [orcid:0000-0002-5301-3142 omid:ra/06106]; Persson, Bengt [orcid:0000-0003-3165-5344 omid:ra/06107]; Finkers, Richard [orcid:0000-0002-4368-8058 omid:ra/06108]; Wilkinson, Mark [orcid:0000-0001-6960-357X omid:ra/06109]; Mons, Barend [orcid:0000-0003-3934-0072 omid:ra/061010]; Grethe, Jeffrey [orcid:0000-0001-5212-7052 omid:ra/061011]; Waagmeester, Andra [orcid:0000-0001-9773-4008 omid:ra/061012]; Schultes, Erik Anthony [orcid:0000-0001-8888-635X omid:ra/061013]; Hooft, Rob [orcid:0000-0001-6825-9439 omid:ra/061014]; Sansone, Susanna-Assunta [orcid:0000-0001-5306-5690 omid:ra/061015]; Blomberg, Niklas [orcid:0000-0003-4155-5910 omid:ra/061016]; Aalbersberg, IJsbrand Jan [orcid:0000-0002-0209-4480 omid:ra/061017]; Goble, Carole [orcid:0000-0003-1219-2137 omid:ra/061018]; Wolstencroft, Katy [orcid:0000-0002-1279-5133 omid:ra/061019]; Groth, Paul [orcid:0000-0003-0183-6910 omid:ra/061020]; Axton, Myles [orcid:0000-0002-8042-4131 omid:ra/061021]; Van Mulligen, Erik [orcid:0000-0003-1377-9386 omid:ra/061022]; Clark, Timothy [orcid:0000-0003-4060-7360 omid:ra/061023]; Bourne, Philip E [orcid:0000-0002-7618-7292 omid:ra/061024]; Brookes, Anthony J. [orcid:0000-0001-8686-0017 omid:ra/061025]; Crosas, Mercè [orcid:0000-0003-1304-1939 omid:ra/061026]; Dillo, Ingrid [orcid:0000-0001-5654-2392 omid:ra/061027]; Velterop, Jan [orcid:0000-0002-4836-6568 omid:ra/061028]; Kuhn, Tobias [orcid:0000-0002-1267-0234 omid:ra/061029]; Gray, Alasdair [orcid:0000-0002-5711-4872 omid:ra/061030]; Edmunds, Scott C [orcid:0000-0001-6444-1436 omid:ra/061031]; Boiten, Jan-Willem [orcid:0000-0003-0327-638X omid:ra/061032]; Sengstag, Thierry [orcid:0000-0002-7516-6246 omid:ra/061033]; Zhao, Jun [orcid:0000-0001-6935-9028 omid:ra/061034]; Appleton, Gaby [orcid:0000-0003-0179-7384 omid:ra/061035]; Thompson, Mark [orcid:0000-0002-7633-1442 omid:ra/061036]; Heringa, Jaap [orcid:0000-0001-8641-4930 omid:ra/061037]; Kok, Ruben [omid:ra/061038]; Kok, Joost [orcid:0000-0002-7352-1400 omid:ra/061039]; Lusher, Scott J. [orcid:0000-0003-2401-4223 omid:ra/061040]; Mons, Albert [omid:ra/061041]; Van Schaik, Rene [omid:ra/061042]; Rocca-Serra, Philippe [orcid:0000-0001-9853-5668 omid:ra/061043]; Packer, Abel L [orcid:0000-0001-9610-5728 omid:ra/061044]; Santos, Luiz Olavo Bonino Da Silva [orcid:0000-0002-1164-1351 omid:ra/061045]; Slater, Ted [orcid:0000-0003-1386-0731 omid:ra/061046]; Baak, Arie [orcid:0000-0003-2829-6715 omid:ra/061047]; Strawn, George [omid:ra/061048]; Van Der Lei, Johan [omid:ra/061049]; Wittenburg, Peter [omid:ra/061050]; Bouwman, Jildau [omid:ra/061051]; Dumon, Olivier [orcid:0000-0001-8599-7345 omid:ra/061052]; Gonzalez-Beltran, Alejandra [orcid:0000-0003-3499-8262 omid:ra/061053]",
                "pub_date": "2016-03-15",
                "page": "3",
                "issue": "",
                "volume": "",
                "venue": "Scientific Data [issn:2052-4463 omid:br/06102]",
                "type": "journal article",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": ""
            }
        ]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_author_by_omid(self):
        operation_url = 'author'
        request = 'omid:ra/0604'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne [omid:ra/0604]; Ebert, Ute [orcid:0000-0003-3891-6869 omid:ra/0605]",
                "pub_date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727 omid:br/0604]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266 omid:ra/0606]",
                "editor": ""
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_author_by_orcid(self):
        operation_url = 'author'
        request = 'orcid:0000-0003-3891-6869'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
                "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
                "author": "Montijn, Carolynne [omid:ra/0604]; Ebert, Ute [orcid:0000-0003-3891-6869 omid:ra/0605]",
                "pub_date": "2006-06-30",
                "page": "2979-2992",
                "issue": "14",
                "volume": "39",
                "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727 omid:br/0604]",
                "type": "journal article",
                "publisher": "Iop Publishing [crossref:266 omid:ra/0606]",
                "editor": ""
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_editor(self):
        operation_url = 'editor'
        request = '0000-0003-2098-4759'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_editor_by_omid(self):
        operation_url = 'editor'
        request = 'omid:ra/0602'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    def test_editor_by_orcid(self):
        operation_url = 'editor'
        request = 'orcid:0000-0003-2098-4759'
        call = "%s/%s/%s" % (api_base, operation_url, request)
        op = api_manager.get_op(call)
        status, result, format = op.exec()
        status_expected = 200
        result_expected = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "page": "",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0601]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/0602]; Stankey, George H. [omid:ra/0603]"
            }]
        format_expected = 'application/json'
        output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
        result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
        expected_output = status_expected, result_expected, format_expected
        self.assertEqual(output, expected_output)

    # def test_text_search_id(self):
    #     operation_url = 'search'
    #     request = 'id=doi:10.1007/978-1-4020-9632-7'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 omid:br/0601",
    #             "title": "Adaptive Environmental Management",
    #             "author": "",
    #             "pub_date": "2009",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "book",
    #             "publisher": "Springer Science And Business Media Llc [crossref:297]",
    #             "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_title(self):
    #     operation_url = 'search'
    #     request = 'title=Adaptive Environmental Management'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 omid:br/0601",
    #             "title": "Adaptive Environmental Management",
    #             "author": "",
    #             "pub_date": "2009",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "book",
    #             "publisher": "Springer Science And Business Media Llc [crossref:297]",
    #             "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_author(self):
    #     operation_url = 'search'
    #     request = 'author=Montijn,Carolynne'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_given_name(self):
    #     operation_url = 'search'
    #     request = 'author=,Carolynne'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_foaf_name(self):
    #     operation_url = 'search'
    #     request = 'author=F42 Committee'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1520/f2792-10e01 omid:br/0603",
    #             "title": "Terminology For Additive Manufacturing Technologies,",
    #             "author": "F42 Committee",
    #             "pub_date": "",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "standard",
    #             "publisher": "Astm International [crossref:381]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_editor(self):
    #     operation_url = 'search'
    #     request = 'editor=Stankey, George H.'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 omid:br/0601",
    #             "title": "Adaptive Environmental Management",
    #             "author": "",
    #             "pub_date": "2009",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "book",
    #             "publisher": "Springer Science And Business Media Llc [crossref:297]",
    #             "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_publisher(self):
    #     operation_url = 'search'
    #     request = 'publisher=Springer Science And Business Media Llc'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1007/978-1-4020-9632-7 isbn:9789048127108 isbn:9781402096327 omid:br/0601",
    #             "title": "Adaptive Environmental Management",
    #             "author": "",
    #             "pub_date": "2009",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "book",
    #             "publisher": "Springer Science And Business Media Llc [crossref:297]",
    #             "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
    #         }
    #     ]
    #     output = status, [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], format
    #     result_expected = [{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected]
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_venue(self):
    #     operation_url = 'search'
    #     request = 'venue=Physics'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
    #     result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_volume_and_issue(self):
    #     operation_url = 'search'
    #     request = 'venue=Physics&&volume=39&&issue=14'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
    #     result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_volume_and_issue_error(self):
    #     operation_url = 'search'
    #     request = 'volume=39||issue=14'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, _, _ = op.exec()
    #     self.assertEqual(status, 500)

    # def test_text_search_venue_and_author(self):
    #     operation_url = 'search'
    #     request = 'venue=Physics&&author=Montijn, Carolynne'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         }
    #     ]
    #     output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
    #     result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_author_or_editor(self):
    #     operation_url = 'search'
    #     request = 'editor=Allan, Catherine||author=Montijn, Carolynne'
    #     call = "%s/%s/%s" % (api_base, operation_url, request)
    #     op = api_manager.get_op(call)
    #     status, result, format = op.exec()
    #     status_expected = 200
    #     format_expected = 'application/json'
    #     result_expected = [
    #         {
    #             "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
    #             "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
    #             "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
    #             "pub_date": "2006-06-30",
    #             "page": "2979-2992",
    #             "issue": "14",
    #             "volume": "39",
    #             "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
    #             "type": "journal article",
    #             "publisher": "Iop Publishing [crossref:266]",
    #             "editor": ""
    #         },
    #         {
    #             "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
    #             "title": "Adaptive Environmental Management",
    #             "author": "",
    #             "pub_date": "2009",
    #             "page": "",
    #             "issue": "",
    #             "volume": "",
    #             "venue": "",
    #             "type": "book",
    #             "publisher": "Springer Science And Business Media Llc [crossref:297]",
    #             "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
    #         }
    #     ]
    #     output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
    #     result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
    #     expected_output = status_expected, result_expected, format_expected
    #     self.assertEqual(output, expected_output)

    # def test_text_search_author_and_publisher_or_editor_and_title(self):
        # operation_url = 'search'
        # request = 'author=Montijn, Carolynne&&publisher=Iop Publishing||editor=Allan, Catherine&&title=Adaptive Environmental Management'
        # call = "%s/%s/%s" % (api_base, operation_url, request)
        # op = api_manager.get_op(call)
        # status, result, format = op.exec()
        # status_expected = 200
        # format_expected = 'application/json'
        # result_expected = [
        #     {
        #         "id": "doi:10.1088/0022-3727/39/14/017 omid:br/0602",
        #         "title": "Diffusion Correction To The Raether–Meek Criterion For The Avalanche-To-Streamer Transition",
        #         "author": "Montijn, Carolynne; Ebert, Ute [orcid:0000-0003-3891-6869]",
        #         "pub_date": "2006-06-30",
        #         "page": "2979-2992",
        #         "issue": "14",
        #         "volume": "39",
        #         "venue": "Journal Of Physics D: Applied Physics [issn:0022-3727]",
        #         "type": "journal article",
        #         "publisher": "Iop Publishing [crossref:266]",
        #         "editor": ""
        #     },
        #     {
        #         "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0601 isbn:9789048127108 isbn:9781402096327",
        #         "title": "Adaptive Environmental Management",
        #         "author": "",
        #         "pub_date": "2009",
        #         "page": "",
        #         "issue": "",
        #         "volume": "",
        #         "venue": "",
        #         "type": "book",
        #         "publisher": "Springer Science And Business Media Llc [crossref:297]",
        #         "editor": "Allan, Catherine [orcid:0000-0003-2098-4759]; Stankey, George H."
        #     }
        # ]
        # output = status, sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in json.loads(result)], key=lambda x:''.join(x['id'])), format
        # result_expected = sorted([{k:set(v.split('; ')) if k in {'author', 'editor'} else sorted(v.split()) if k == 'id' else v for k,v in el.items()} for el in result_expected], key=lambda x:''.join(x['id']))
        # expected_output = status_expected, result_expected, format_expected
        # self.assertEqual(output, expected_output)