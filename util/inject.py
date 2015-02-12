__author__ = 'grainier'
import re

with open ("raw_html.txt", "r") as myfile:
    data = myfile.read()

data = unicode(data, 'utf8')

# should find a way to get this
referer = 'http://example.com/abc.php?d=3424'

# strip get parameters
try:
    referer = referer[:referer.index('?')]
    pass
except ValueError:
    pass

# md5 the referer
o_ref = referer

# verification (is this necessary?)
o_ver = 'fsdhjkhfsjkd34ewr4'

href_pattern = ur'href=\"([^"]+)\"'
alt_href = ur'href="\1?o_ref=%s&o_ver=%s"' % (o_ref, o_ver)

# TODO : Remove possible duplication of '?'
# TODO : How to hash referer, how to cross reference for the original url using hash (2way)
# TODO : Verification number generation method
# TODO : How to get response destination from Client Profile

man_data = re.sub(href_pattern, alt_href, data)

print(man_data)