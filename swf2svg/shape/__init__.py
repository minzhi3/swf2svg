import swf2svg.shape.Gradient
import swf2svg.shape.FillStyle
import swf2svg.shape.LineStyle
import swf2svg.shape.ShapeRecord


def read_gradient(buffer, shape_generation):
    return Gradient.Gradient(buffer, shape_generation)


def read_fill_style_array(buffer, shape_generation):
    return FillStyle.FillStyleArray(buffer, shape_generation)


def read_line_style_array(buffer, shape_generation):
    return LineStyle.LineStyleArray(buffer, shape_generation)

