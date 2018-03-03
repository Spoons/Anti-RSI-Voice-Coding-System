from dragonfly import *

def combine_maps(*maps):
    """Merge the contents of multiple maps, giving precedence to later maps."""
    result = {}
    for map in maps:
        if map:
            result.update(map)
    return result

def join_maps(*maps):
    result = {}
    for map in maps:
        if map:
            result.update(map)
    return (result)

def create_rule(name, action_map, element_map, exported=False, context=None):
    """Creates a rule with the given name, binding the given element map to the
    action map.
    """
    return MappingRule(name,
                       action_map,
                       element_map_to_extras(element_map),
                       element_map_to_defaults(element_map),
                       exported,
                       context=context)


class JoinedRepetition(Repetition):
    """Like Repetition, except the results are joined with the given delimiter
    instead of returned as a list.
    """

    def __init__(self, delimiter, *args, **kwargs):
        Repetition.__init__(self, *args, **kwargs)
        self.delimiter = delimiter

    def value(self, node):
        return self.delimiter.join(Repetition.value(self, node))


