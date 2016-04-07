import swf2svg
import unittest
import xml.etree.ElementTree


class TestMain(unittest.TestCase):
    def setUp(self):
        self.svg_xml = None
        self.output_file = None

    def tearDown(self):
        xml.etree.ElementTree.ElementTree(self.svg_xml).write(self.output_file, encoding="UTF-8", xml_declaration=False, method="xml")

    def test_candy(self):
        input_file = 'swf/candy.swf'
        self.output_file = 'svg/candy.svg'
        self.svg_xml = swf2svg.to_svg(input_file)

    def test_body(self):
        input_file = 'swf/body.swf'
        self.output_file = 'svg/body.svg'
        self.svg_xml = swf2svg.to_svg(input_file)
