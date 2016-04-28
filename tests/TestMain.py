import swf2svg
import unittest


class TestMain(unittest.TestCase):
    def test_candy(self):
        input_file = 'swf/candy.swf'
        output_svg = 'svg/candy.svg'
        output_json = 'json/candy.json'
        swf2svg.write_file(input_file, output_svg, output_json, True)

    def test_body(self):
        input_file = 'swf/body.swf'
        output_svg = 'svg/body.svg'
        output_json = 'json/body.json'
        swf2svg.write_file(input_file, output_svg, output_json, True)

    def test_angel_failure(self):
        input_file = 'swf/angel_failure_android.swf'
        output_svg = 'svg/angel_failure_android.svg'
        output_json = 'json/angel_failure_android.json'
        swf2svg.write_file(input_file, output_svg, output_json, True)

    def test_sky(self):
        input_file = 'swf/skyMc_0156.swf'
        output_svg = 'svg/skyMc_0156.svg'
        output_json = 'json/skyMc_0156.json'
        swf2svg.write_file(input_file, output_svg, output_json, True)

