import swf2svg
import unittest
import xml.dom.minidom
import xml.etree.ElementTree
import json


class TestMain(unittest.TestCase):
    def setUp(self):
        self.svg_xml = None
        self.output_file = None
        self.json = None
        self.js_file = None

    def tearDown(self):
        svg = xml.etree.ElementTree.tostring(self.svg_xml, encoding='utf8', method='xml')
        xml_string = xml.dom.minidom.parseString(svg)
        pretty_xml = xml_string.toprettyxml()
        text_file = open(self.output_file, "w")
        text_file.write(pretty_xml)
        text_file.close()

        js_file = open(self.js_file, 'w')
        js_file.write('var svgInfo = ')
        json.dump(self.json, js_file)
        js_file.close()

    def test_candy(self):
        input_file = 'swf/candy.swf'
        self.output_file = 'svg/candy.svg'
        self.js_file = 'js/candy.js'
        self.svg_xml, self.js = swf2svg.to_svg(input_file)

    def test_body(self):
        input_file = 'swf/body.swf'
        self.output_file = 'svg/body.svg'
        self.js_file = 'js/body.js'
        self.svg_xml, self.js = swf2svg.to_svg(input_file)

    def test_body2(self):
        input_file = 'swf/angelbody_petit_eto_0001.swf'
        self.output_file = 'svg/body2.svg'
        self.js_file = 'js/body2.js'
        self.svg_xml, self.json = swf2svg.to_svg(input_file=input_file, svg_path='swf2svg/tests/svg/body2.svg')

    def test_sky(self):
        input_file = 'swf/skyMc_0156.swf'
        self.output_file = 'svg/skyMc_0156.svg'
        self.js_file = 'svg/skyMc_0156.js'
        self.svg_xml, self.js = swf2svg.to_svg(input_file=input_file)
