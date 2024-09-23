import json
import os
import sys
import unittest
from io import StringIO

from ramose import APIManager


class TestMetaAPI(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(current_dir, "meta_v1_test.hf")
        cls.api_manager = APIManager([config_file])

    def execute_operation(self, operation_url):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        op = self.api_manager.get_op(operation_url)
        if isinstance(op, tuple):
            print(f"Error: {op[1]}")
        else:
            status, result, _ = op.exec(method="get", content_type="application/json")
            print(result)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return output

    def normalize_string(self, s):
        original = s
        new_s = s.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
        if original != new_s:
            print(f"Normalized: '{original}' to '{new_s}'")
        return new_s

    def normalize_json(self, json_data):
        if isinstance(json_data, dict):
            return {k: self.normalize_json(v) for k, v in json_data.items()}
        elif isinstance(json_data, list):
            return [self.normalize_json(item) for item in json_data]
        elif isinstance(json_data, str):
            return self.normalize_string(json_data)
        else:
            return json_data

    def test_metadata_retrieval(self):
        output = self.execute_operation("/api/v1/metadata/doi:10.1007/978-1-4020-9632-7")
        expected_output = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 omid:br/0612058700",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "page": "",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0610116006]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/069012996]; Stankey, George H. [omid:ra/061808486861]"
            }
        ]
        try:
            output_json = json.loads(output)
        except json.JSONDecodeError:
            self.fail("L'output non è un JSON valido")
        normalized_output = self.normalize_json(output_json)
        normalized_expected = self.normalize_json(expected_output)
        self.assertEqual(normalized_output, normalized_expected)


    def test_author_works_retrieval(self):
        output = self.execute_operation("/api/v1/author/orcid:0000-0002-8420-0696")
        expected_output = [
            {
                "id": "doi:10.5281/zenodo.4733920 omid:br/060504628",
                "title": "Classes Of Errors In DOI Names (Data Management Plan)",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-05-03",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601747332]",
                "editor": ""
            },
            {
                "id": "doi:10.32388/x2dx81 openalex:W3153150899 omid:br/062203845802",
                "title": "Review Of: \"Investigating Invalid DOIs In COCI\"",
                "author": "Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]",
                "pub_date": "2021-04-19",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "journal article",
                "page": "",
                "publisher": "Qeios Ltd [crossref:17262 omid:ra/0640115413]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4733919 omid:br/060504627",
                "title": "Classes Of Errors In DOI Names (Data Management Plan)",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-06-09",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601747331]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4734513 omid:br/060504676",
                "title": "Cleaning Different Types Of DOI Errors Found In Cited References On Crossref Using Automated Methods",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-05-03",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "report",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601747493]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/s11192-022-04367-w openalex:W3214893238 omid:br/061202127149",
                "title": "Identifying And Correcting Invalid Citations Due To DOI Errors In Crossref Data",
                "author": "Cioffi, Alessia [orcid:0000-0002-9812-4065 omid:ra/061206532419]; Coppini, Sara [orcid:0000-0002-6279-3830 omid:ra/061206532420]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Moretti, Arianna [orcid:0000-0001-5486-7070 omid:ra/061206532421]; Peroni, Silvio [orcid:0000-0003-0530-4305 omid:ra/0614010840729]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Shahidzadeh, Nooshin [orcid:0000-0003-4114-074X omid:ra/06220110984]",
                "pub_date": "2022-06",
                "issue": "6",
                "volume": "127",
                "venue": "Scientometrics [issn:0138-9130 issn:1588-2861 openalex:S148561398 omid:br/0626055628]",
                "type": "journal article",
                "page": "3593-3612",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0610116006]",
                "editor": ""
            },
            {
                "id": "doi:10.5334/johd.178 omid:br/06404693975",
                "title": "The Integration Of The Japan Link Center's Bibliographic Data Into OpenCitations",
                "author": "Heibi, Ivan [orcid:0000-0001-5366-5194 omid:ra/064013186642]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/064013186643]; Moretti, Arianna [orcid:0000-0001-5486-7070 omid:ra/061206532421]; Peroni, Silvio [orcid:0000-0003-0530-4305 omid:ra/064013186644]; Rizzetto, Elia [orcid:0009-0003-7161-9310 omid:ra/064013186645]; Soricetti, Marta [orcid:0009-0008-1466-7742 omid:ra/064013186641]",
                "pub_date": "2024",
                "issue": "",
                "volume": "10",
                "venue": "Journal Of Open Humanities Data [issn:2059-481X openalex:S4210240912 omid:br/06160186133]",
                "type": "journal article",
                "page": "",
                "publisher": "Ubiquity Press, Ltd. [crossref:3285 omid:ra/0610116010]",
                "editor": ""
            },
            {
                "id": "doi:10.17504/protocols.io.buuknwuw openalex:W4229763694 omid:br/06903005993",
                "title": "Protocol: Investigating DOIs Classes Of Errors V5",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-05-08",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "web content",
                "page": "",
                "publisher": "ZappyLab, Inc. [crossref:7078 omid:ra/0640115421]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4734512 omid:br/060504675",
                "title": "Cleaning Different Types Of DOI Errors Found In Cited References On Crossref Using Automated Methods",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-06-08",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "report",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601747492]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4914003 omid:br/060522891",
                "title": "Cleaning Different Types Of DOI Errors Found In Cited References On Crossref Using Automated Methods",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-06-08",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "report",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601805162]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4928592 omid:br/060528347",
                "title": "Classes Of Errors In DOI Names (Data Management Plan)",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-06-09",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601822363]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4738553 omid:br/060505044",
                "title": "Presentation Of \"Cleaning Different Types Of DOI Errors Found In Cited References On Crossref Using Automated Methods\"",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-05-05",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "report",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601748478]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4738552 omid:br/060505043",
                "title": "Presentation Of \"Cleaning Different Types Of DOI Errors Found In Cited References On Crossref Using Automated Methods\"",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-05-05",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "report",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601748477]",
                "editor": ""
            },
            {
                "id": "doi:10.5281/zenodo.4913741 omid:br/060522768",
                "title": "Classes Of Errors In DOI Names (Data Management Plan)",
                "author": "Boente, Ricarda [orcid:0000-0002-2133-8735 omid:ra/06908359558]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Santini, Cristian [orcid:0000-0001-7363-6737 omid:ra/067099715]; Tural, Deniz [orcid:0000-0002-6391-4198 omid:ra/06908359559]",
                "pub_date": "2021-06-08",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "",
                "page": "",
                "publisher": "Zenodo [omid:ra/0601804641]",
                "editor": ""
            },
            {
                "id": "doi:10.1007/978-3-031-16802-4_36 openalex:W4295990858 omid:br/061603442625",
                "title": "Enabling Portability And Reusability Of Open Science Infrastructures",
                "author": "Grieco, Giuseppe [orcid:0000-0001-5439-4576 omid:ra/061609362356]; Heibi, Ivan [orcid:0000-0001-5366-5194 omid:ra/063011864088]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/06250110138]; Moretti, Arianna [orcid:0000-0001-5486-7070 omid:ra/061206532421]; Peroni, Silvio [orcid:0000-0003-0530-4305 omid:ra/0614010840729]",
                "pub_date": "2022",
                "issue": "",
                "volume": "",
                "venue": "Linking Theory And Practice Of Digital Libraries [isbn:9783031168017 isbn:9783031168024 omid:br/061603442934]",
                "type": "book chapter",
                "page": "379-385",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0610116006]",
                "editor": ""
            }
        ]
        
        try:
            output_json = json.loads(output)
        except json.JSONDecodeError:
            self.fail("L'output non è un JSON valido")
        normalized_output = self.normalize_json(output_json)
        normalized_expected = self.normalize_json(expected_output)
        self.assertEqual(normalized_output, normalized_expected)

    def test_editor_works_retrieval(self):
        output = self.execute_operation("/api/v1/editor/orcid:0000-0003-2098-4759")
        expected_output = [
            {
                "id": "doi:10.1007/978-1-4020-9632-7 isbn:9781402096327 isbn:9789048127108 openalex:W4249829199 omid:br/0612058700",
                "title": "Adaptive Environmental Management",
                "author": "",
                "pub_date": "2009",
                "issue": "",
                "volume": "",
                "venue": "",
                "type": "book",
                "page": "",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0610116006]",
                "editor": "Allan, Catherine [orcid:0000-0003-2098-4759 omid:ra/069012996]; Stankey, George H. [omid:ra/061808486861]"
            }
        ]

        try:
            output_json = json.loads(output)
        except json.JSONDecodeError:
            self.fail("L'output non è un JSON valido")
        normalized_output = self.normalize_json(output_json)
        normalized_expected = self.normalize_json(expected_output)        
        self.assertEqual(normalized_output, normalized_expected)

if __name__ == '__main__':
    unittest.main()