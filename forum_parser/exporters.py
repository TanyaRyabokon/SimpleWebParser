from scrapy.exporters import XmlItemExporter


class ArticlesXmlItemExporter(XmlItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
        self.item_element = kwargs.pop("item_element", "page")
        self.root_element = kwargs.pop("root_element", "data")

    def make_fragment(self, item_name, item_value):
        self._beautify_indent(depth=2)
        self.xg.startElement("fragment", {"type": item_name})
        self._beautify_newline()
        self._beautify_indent(depth=3)
        self._xg_characters(str(item_value))
        self._beautify_newline()
        self._beautify_indent(depth=2)
        self.xg.endElement("fragment")
        self._beautify_newline(new_item=True)

    def export_item(self, item):
        self._beautify_indent(depth=1)
        self.xg.startElement(self.item_element, {"url": item["url"]})
        self._beautify_newline()
        for name, values in self._get_serialized_fields(
            item, default_value=""
        ):
            if isinstance(values, list):
                for value in values:
                    self.make_fragment(name, value)
            else:
                self.make_fragment(name, values)
        self._beautify_indent(depth=1)
        self.xg.endElement(self.item_element)
        self._beautify_newline(new_item=True)
