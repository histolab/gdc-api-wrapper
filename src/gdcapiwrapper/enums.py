# encoding: utf-8

from enum import Enum


class FORMAT_TYPE(Enum):
    """Enumerated values representing the various types of file format."""

    # ---member definitions---
    CSV = "CSV"
    HTML = "HTML"
    JSON = "JSON"
    XML = "XML"

    # ---allowed formats for TCIA apis---
    TCIA_ALLOWED_FORMATS = frozenset((CSV, HTML, JSON, XML))
