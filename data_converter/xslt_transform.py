import os
from lxml import etree as ET


def xslt_transform(xml_filename):
    xsl_path = os.path.join("data_converter", "products_transform.xsl")
    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_path)
    transform = ET.XSLT(xslt)
    result = transform(dom)
    result.write_output("products.html")
