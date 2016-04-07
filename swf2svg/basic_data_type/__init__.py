import swf2svg.basic_data_type.Rectangle
import swf2svg.basic_data_type.CXForm
import swf2svg.basic_data_type.Matrix
import swf2svg.basic_data_type.Color


def read_rect(bit_reader):
    return Rectangle.read_rect(bit_reader)


def read_matrix(buffer):
    return Matrix.MatrixRecord(buffer)


def read_cx_form(buffer):
    return CXForm.CXFormRecord(buffer)


def read_cx_form_with_alpha(buffer):
    return CXForm.CXFormWithAlphaRecord(buffer)


def read_color(red, green, blue, alpha):
    if alpha is None:
        return Color.RGBColorRecord(red, green, blue)
    else:
        return Color.RGBAColorRecord(red, green, blue, alpha)
