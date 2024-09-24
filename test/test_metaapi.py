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
        return s.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')

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

    def test_metadata_retrieval_editor_inbook(self):
        # https://github.com/opencitations/api/issues/16

        output = self.execute_operation("/api/v1/metadata/omid:br/061702784433")
        expected_output = [
            {
                "id": "doi:10.1007/978-3-642-30859-8_14 openalex:W1555136325 omid:br/061702784433",
                "title": "Analysing Students’ Use Of Recorded Lectures Through Methodological Triangulation",
                "author": "Gorissen, Pierre [omid:ra/061707839728]; Van Bruggen, Jan [omid:ra/061707839729]; Jochems, Wim [omid:ra/061707839730]",
                "pub_date": "2012",
                "issue": "",
                "volume": "",
                "venue": "Advances In Intelligent Systems And Computing [doi:10.1007/978-3-642-30859-8 isbn:9783642308581 isbn:9783642308598 openalex:W2221102889 omid:br/061702785338]",
                "type": "book chapter",
                "page": "145-156",
                "publisher": "Springer Science And Business Media Llc [crossref:297 omid:ra/0610116006]",
                "editor": "Uden, Lorna [omid:ra/062409604521]; Corchado, Juan Manuel [orcid:0000-0002-2829-1829 omid:ra/064010719912]; De Paz Santana, Juan F. [omid:ra/062409604522]; Prieta, Fernando De La [orcid:0000-0002-8239-5020 omid:ra/069026742]"
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
                "author": "Moretti, Arianna [orcid:0000-0001-5486-7070 omid:ra/061206532421]; Soricetti, Marta [orcid:0009-0008-1466-7742 omid:ra/064013186641]; Heibi, Ivan [orcid:0000-0001-5366-5194 omid:ra/064013186642]; Massari, Arcangelo [orcid:0000-0002-8420-0696 omid:ra/064013186643]; Peroni, Silvio [orcid:0000-0003-0530-4305 omid:ra/064013186644]; Rizzetto, Elia [orcid:0009-0003-7161-9310 omid:ra/064013186645]",
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

    def test_venue_without_external_id(self):
        # https://github.com/opencitations/api/issues/15
        output = self.execute_operation("/api/v1/metadata/omid:br/061903571196")
        expected_output = [
            {
                "id": "doi:10.36106/gjra/9300981 openalex:W4306682982 omid:br/061903571196",
                "title": "Lung Cavitation: An Unwanted Complication Of Covid-19 Lung Disease",
                "author": "A Dosi, Ravi [omid:ra/061909585847]; Shivhare, Shailendra [omid:ra/061909585848]; Agrawal, Ankur [omid:ra/061909585849]; Jaiswal, Neha [omid:ra/061909585850]; Patidar, Ravindra [omid:ra/061909585851]",
                "pub_date": "2022-09-15",
                "issue": "",
                "volume": "",
                "venue": "Global Journal For Research Analysis [omid:br/061903571793]",
                "type": "journal article",
                "page": "31-33",
                "publisher": "World Wide Journals [crossref:21849 omid:ra/0640115418]",
                "editor": ""
            }
        ]
        try:
            output_json = json.loads(output)
        except json.JSONDecodeError:
            self.fail("The output is not valid JSON")
        normalized_output = self.normalize_json(output_json)
        normalized_expected = self.normalize_json(expected_output)
        self.assertEqual(normalized_output, normalized_expected)
        self.assertIn("omid:", normalized_output[0]["venue"], "The venue field should contain an OMID")

    def test_metadata_retrieval_with_different_ids(self):
        # https://github.com/opencitations/api/issues/14
        
        # Test retrieval using OMID
        output_omid = self.execute_operation("/api/v1/metadata/omid:br/06603870331")
        json_omid = json.loads(output_omid)
        
        # Test retrieval using ISBN
        output_isbn = self.execute_operation("/api/v1/metadata/isbn:9789264960114")
        json_isbn = json.loads(output_isbn)
        
        # Test retrieval using DOI
        output_doi = self.execute_operation("/api/v1/metadata/doi:10.1787/b0e499cf-en")
        json_doi = json.loads(output_doi)
        
        # Normalize the results
        normalized_omid = self.normalize_json(json_omid)
        normalized_isbn = self.normalize_json(json_isbn)
        normalized_doi = self.normalize_json(json_doi)
        
        # Check that all results have the same basic structure
        self.assertEqual(len(normalized_omid), 1)
        self.assertEqual(len(normalized_isbn), 1)
        self.assertEqual(len(normalized_doi), 1)
        
        # Define the complete list of expected IDs
        expected_ids = [
            'doi:10.1787/b0e499cf-en',
            'isbn:9789264597587',
            'isbn:9789264759596',
            'isbn:9789264799318',
            'isbn:9789264960114',
            'openalex:W4221051054',
            'omid:br/06603870331'
        ]
        
        # Check that the OMID result contains all IDs
        omid_ids = normalized_omid[0]['id'].split()
        for expected_id in expected_ids:
            self.assertIn(expected_id, omid_ids)
        
        # Check that the ISBN result contains all IDs
        isbn_ids = normalized_isbn[0]['id'].split()
        for expected_id in expected_ids:
            self.assertIn(expected_id, isbn_ids)

        # Check that the DOI result contains all IDs
        doi_ids = normalized_doi[0]['id'].split()
        for expected_id in expected_ids:
            self.assertIn(expected_id, doi_ids)
        
        # Check that the number of IDs is correct
        self.assertEqual(len(omid_ids), len(expected_ids))
        self.assertEqual(len(isbn_ids), len(expected_ids))
        self.assertEqual(len(doi_ids), len(expected_ids))
        
        # Check that other metadata fields are the same across all results
        fields_to_check = ['title', 'author', 'pub_date', 'venue', 'publisher', 'type', 'issue', 'volume', 'page', 'editor']
        for field in fields_to_check:
            self.assertEqual(normalized_omid[0][field], normalized_isbn[0][field])
            self.assertEqual(normalized_omid[0][field], normalized_doi[0][field])

        # Check specific values
        self.assertEqual(normalized_omid[0]['title'], "OECD Economic Surveys: China 2022")
        self.assertEqual(normalized_omid[0]['author'], "Oecd [omid:ra/066010636485]")
        self.assertEqual(normalized_omid[0]['pub_date'], "2022-03-18")
        self.assertEqual(normalized_omid[0]['venue'], "OECD Economic Surveys: China [issn:2072-5027 openalex:S4210223649 omid:br/061402215286]")
        self.assertEqual(normalized_omid[0]['type'], "book")
        self.assertEqual(normalized_omid[0]['publisher'], "Organisation For Economic Co-Operation And Development (Oecd) [crossref:1963 omid:ra/0610116167]")

    def test_author_order_in_metadata(self):
        # https://github.com/opencitations/api/issues/13

        output = self.execute_operation("/api/v1/metadata/omid:br/0680773548")
        expected_output = [
            {
                "author": "Bilgin, Hülya [orcid:0000-0001-6639-5533 omid:ra/0622032021]; Bozkurt, Merlin [omid:ra/06802276621]; Yilmazlar, Selçuk [omid:ra/06802276622]; Korfali, Gülsen [omid:ra/06802276623]",
                "issue": "3",
                "editor": "",
                "pub_date": "2006-05",
                "title": "Sudden Asystole Without Any Alerting Signs During Cerebellopontine Angle Surgery",
                "volume": "18",
                "page": "243-244",
                "id": "doi:10.1016/j.jclinane.2005.12.014 openalex:W2127410217 pmid:16731339 omid:br/0680773548",
                "publisher": "Elsevier Bv [crossref:78 omid:ra/0610116009]",
                "type": "journal article",
                "venue": "Journal Of Clinical Anesthesia [issn:0952-8180 openalex:S155967237 omid:br/0621013884]"
            }
        ]

        try:
            output_json = json.loads(output)
        except json.JSONDecodeError:
            self.fail("The output is not valid JSON")

        normalized_output = self.normalize_json(output_json)
        normalized_expected = self.normalize_json(expected_output)

        self.assertEqual(normalized_output, normalized_expected)

        # Check specific author order
        authors = normalized_output[0]['author'].split('; ')
        expected_author_order = [
            "Bilgin, Hülya [orcid:0000-0001-6639-5533 omid:ra/0622032021]",
            "Bozkurt, Merlin [omid:ra/06802276621]",
            "Yilmazlar, Selçuk [omid:ra/06802276622]",
            "Korfali, Gülsen [omid:ra/06802276623]"
        ]
        self.assertEqual(authors, expected_author_order)

    def test_metadata_retrieval_with_parentheses_in_doi(self):
        # https://github.com/opencitations/api/issues/12

        test_dois = [
            "doi:10.1016/s0005-7894(77)80292-x",
            "doi:10.1016/s0002-9610(00)00404-9",
            "doi:10.1016/s0188-4409(00)00147-8",
            "doi:10.1002/1096-8644(200103)114:3<224::aid-ajpa1022>3.3.co;2-9",
            "doi:10.1002/(sici)1098-2760(19990605)21:5<330::aid-mop7>3.3.co;2-e"
        ]

        for doi in test_dois:
            output = self.execute_operation(f"/api/v1/metadata/{doi}")
            
            try:
                output_json = json.loads(output)
            except json.JSONDecodeError:
                self.fail(f"The output for {doi} is not valid JSON")

            # Check if the output is not empty
            self.assertNotEqual(len(output_json), 0, f"No metadata returned for {doi}")

            # Check if the 'id' field in the returned metadata contains the input DOI
            self.assertIn(doi, output_json[0]['id'], f"Returned metadata does not match input DOI for {doi}")


if __name__ == '__main__':
    unittest.main()