import unittest

from lxml import etree
from parliament_data.utils import validate_xml_schema
from parliament_data.download import get_blocks
from parliament_data.segmentation import create_tei, create_parlaclarin, infer_metadata

class Test(unittest.TestCase):

    # Official example parla-clarin 
    def test_official_example(self):
        schema_path = "schemas/parla-clarin.xsd"
        parlaclarin_path = "data/parla-clarin/official-example.xml"
        
        valid = validate_xml_schema(parlaclarin_path, schema_path)
        self.assertEqual(valid, True)

    # Parla-clarin generated from example OCR XML
    def test_generated_example(self):
        schema_path = "schemas/parla-clarin.xsd"
        package_id = "prot-198990--93"
        fname = "prot_198990__93-031.xml"
        
        # Package argument can be None since the file is already saved on disk
        content_blocks = get_blocks(fname, None, package_id)
        metadata = infer_metadata(fname)
        
        tei = create_tei(content_blocks, metadata)
        parla_clarin_str = create_parlaclarin(tei, metadata)
        
        parlaclarin_path = "data/parla-clarin/generated-example.xml"
        f = open(parlaclarin_path, "w")
        f.write(parla_clarin_str)
        f.close()
        
        valid = validate_xml_schema(parlaclarin_path, schema_path)
        self.assertEqual(valid, True)


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
