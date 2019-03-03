from yattag import Doc, indent
from collections import namedtuple
from xml.etree import ElementTree

Product = namedtuple("Product", ["image", "description", "price"])


def get_product_list_from_xml(filename):
    tree = ElementTree.parse(filename)
    products = tree.getroot()

    products_list = []

    for product in products:
        product_image = product.find("image").text
        product_description = product.find("description").text
        product_price = product.find("price").text
        products_list.append(
            Product(
                image=product_image,
                description=product_description,
                price=product_price,
            )
        )

    return products_list


def xml_data_to_html(input_filename, output_filename):
    product_list = get_product_list_from_xml(input_filename)

    columns_headers = ["Image", "Description", "Price"]

    doc, tag, text, line = Doc().ttl()
    doc.asis(
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
        '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
    )

    with tag("html"):
        with tag("head"):
            doc.asis('<meta charset="utf-8">')
            doc.asis(
                '<link rel="stylesheet"'
                ' href="https://maxcdn.bootstrapcdn.com/bootstrap'
                '/4.0.0/css/bootstrap.min.css" '
                'integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy'
                '4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" '
                'crossorigin="anonymous">'
            )

        with tag("body"):

            with tag("h1", align="center", klass="display-3"):
                text("Products")

            with tag(
                "table", style="width: 90%", klass="table table-hover mx-auto"
            ):
                with tag("thead"):
                    with tag("tr"):
                        for header in columns_headers:
                            with tag("th", scope="col", align="center"):
                                text(header)

                with tag("tbody"):
                    for product in product_list:
                        with tag("tr", klass="product"):
                            with tag("td"):
                                with tag(
                                    "a", href=product.image, target="_blank"
                                ):
                                    doc.stag(
                                        "img",
                                        src=product.image,
                                        klass="rounded float-left",
                                        height="200",
                                        width="200",
                                        alt=product.description,
                                    )
                            with tag(
                                "td", align="center", klass="align-middle"
                            ):
                                with tag("p", klass="lead"):
                                    text(product.description)
                            with tag(
                                "td", align="center", klass="align-middle"
                            ):
                                with tag("p", klass="lead"):
                                    text(product.price)

    with open(output_filename, "w") as html_file:
        html_file.write(indent(doc.getvalue()))

    return indent(doc.getvalue())
