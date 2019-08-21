

def is_tag_match(elem, suffix):
    """ returns true if namespaced tag name matches suffix without the namespace
    tag name will be {namespaceblahblahblah}suffix
    """
    suffixLen = len(suffix)
    return elem.tag[-suffixLen:] == suffix

def get_attr_val(elem, suffix):
    """ gets the attribute value given by suffix from the element
    uses the namespace from the element tag """
    namespace = elem.tag.split('}')[0] + '}'
    return elem.get(namespace + suffix)