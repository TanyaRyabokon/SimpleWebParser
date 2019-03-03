ESCAPE_LITERALS = ["\r", "\n", "\t", "\xa0"]


def clean_article_text(text):
    for literal in ESCAPE_LITERALS:
        text = text.replace(literal, "")
    return text


def get_custom_settings(filename, xml_exporter):
    return {
        "FEED_URI": filename,
        "FEED_EXPORTERS": {"xml": xml_exporter},
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "xml",
        "FEED_EXPORT_INDENT": 4,
        "LOG_ENABLED": False,
    }
