#!/usr/bin/env python3

import argparse

_header = r"""<?xpacket begin='' id=''?>
<x:xmpmeta xmlns:x='adobe:ns:meta/'>
  <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>"""


_footer = r"""
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end='r'?>"""


def description_marked(public_domain=False):
    string = "False" if public_domain else "True"
    return r"""
    <rdf:Description rdf:about=''
                     xmlns:xapRights='http://ns.adobe.com/xap/1.0/rights/'>
      <xapRights:Marked>""" + string + r"""</xapRights:Marked>
    </rdf:Description>"""


def description_url(url):
    return r"""
    <rdf:Description rdf:about=''
                     xmlns:xapRights='http://ns.adobe.com/xap/1.0/rights/'>
      <xapRights:WebStatement rdf:resource='""" + url + r"""'/>
    </rdf:Description>"""


def description_terms(lang=["en"], default="en"):
    stringmap = {
        "en": "This work is licensed under a &lt;a rel=&#34;license&#34; "
              "href=&#34;http://creativecommons.org/licenses/by-sa/4.0/&#34;"
              "&gt;Creative Commons Attribution-ShareAlike 4.0 International "
              "License&lt;/a&gt;.",
        "de": "Dieses Werk ist lizenziert unter einer &lt;a rel=&#34;license"
              "&#34; href=&#34;http://creativecommons.org/licenses/by-sa/4.0/"
              "&#34;&gt;Creative Commons Namensnennung - Weitergabe unter "
              "gleichen Bedingungen 4.0 International Lizenz&lt;/a&gt;.",
    }

    string = r"""
    <rdf:Description rdf:about=''
                     xmlns:xapRights='http://ns.adobe.com/xap/1.0/rights/'>
      <xapRights:UsageTerms>
        <rdf:Alt>"""

    string += r"""
          <rdf:li xml:lang='x-default' >""" + stringmap[default] + \
              r"""</rdf:li>"""
    for l in lang:
        string += r"""
          <rdf:li xml:lang='""" + l + r"""' >""" + stringmap[l] + \
              r"""</rdf:li>"""

    string += r"""
        </rdf:Alt>
      </xapRights:UsageTerms>
    </rdf:Description>"""
    return string


def description_title(title):
    string = r"""
    <rdf:Description rdf:about=''
                     xmlns:dc='http://purl.org/dc/elements/1.1/'>
      <dc:title>
        <rdf:Alt>"""

    string += r"""
          <rdf:li xml:lang='x-default' >""" + title + r"""</rdf:li>"""
    string += r"""
          <rdf:li xml:lang='en' >""" + title + r"""</rdf:li>"""

    string += r"""
        </rdf:Alt>
      </dc:title>
    </rdf:Description>"""
    return string


def description_licence(licence_url="http://creativecommons.org/licenses/"
                        "by-sa/4.0/"):
    return r"""
    <rdf:Description rdf:about=''
                     xmlns:cc='http://creativecommons.org/ns#'>
      <cc:license rdf:resource='""" + licence_url + r"""'/>
    </rdf:Description>"""


def description_attribution(name):
    return r"""
    <rdf:Description rdf:about=''
                     xmlns:cc='http://creativecommons.org/ns#'>
      <cc:attributionName>""" + name + r"""</cc:attributionName>
    </rdf:Description>"""


def description_more_permissions(url):
    """Url under which one may ask for more rights"""
    return r"""
    <rdf:Description rdf:about=''
                     xmlns:cc='http://creativecommons.org/ns#'>
      <cc:morePermissions rdf:resource='""" + url + """'/>
    </rdf:Description>"""


def generate_xmp(title, author, url, extra_permissions=None):
    """
    title     Title of the work
    author    Author of the work
    url       Url which users of the work should reference
    extra_permissions    Url which users should contact to request
                         further permissions

    Returns the content of the appropriate xmp file
    """
    string = _header
    string += description_marked()
    string += description_url(url)
    string += description_terms()
    string += description_title(title)
    string += description_licence()
    string += description_attribution(author)
    if extra_permissions:
        string += description_more_permissions(extra_permissions)
    string += _footer

    return string


def main():
    parser = argparse.ArgumentParser(
        description="Builder for xmp metadata files for cc-by-sa licenced works"
    )
    parser.add_argument("--url", help="Url users of the work should reference",
                        required=True)
    parser.add_argument("--title", help="Title of the work", required=True)
    parser.add_argument("--author", help="Author of the work", required=True)
    parser.add_argument("--extra-permission", dest="extra_permissions",
                        help="Url where further permissions may be requested")

    parser.add_argument("output", help="Output xml file to write.",
                        metavar="output.xmp")

    args = parser.parse_args()
    with open(args.output, "w") as f:
        f.write(generate_xmp(args.title, args.author, args.url,
                             args.extra_permissions))


if __name__ == "__main__":
    main()
