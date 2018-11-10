"""
contains definitions of the supplementary parse objects
"""


class StringValue:
    """ StringValue """

    def __init__(self, string_characters):
        self.value = string_characters

    def __repr__(self):
        return f'StringValue("{self.string_characters}")'

    def __str__(self):
        return f'"{self.string_characters}"'


class Definition:
    """ Definition """

    def __init__(self, definition):
        self.definition = definition


class ExecutableDefinition:
    """ ExecutableDefinition """

    def __init__(self, definition):
        self.definition = definition


class OperationDefinition:
    """ OperationDefinition """

    def __init__(self, selection_set, operation_type='query', name=None,
                 variable_definitions=None, directives=None):
        self.selection_set = selection_set
        self.operation_type = operation_type
        self.name = name
        self.variable_definitions = variable_definitions
        self.directives = directives


class SelectionSet:
    """ SelectionSet """

    def __init__(self, selections):
        self.selections = selections


class Selection:
    """ Selection """

    def __init__(self, field):
        self.field = field


class Field:
    """ Field """

    def __init__(self, name, alias=None, arguments=None, directives=None,
                 selection_set=None):
        self.name = name
        self.alias = alias
        self.arguments = arguments
        self.directives = directives
        self.selection_set = selection_set


class Arguments:
    """ Arguments """

    def __init__(self, argument):
        self.arguments = [argument]


class Argument:
    """ Argument """

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Value:
    """ Value """

    def __init__(self, value):
        self.value = value.value

    def __repr__(self):
        return f'Value("{self.value}")'

    def __str__(self):
        return f'"{self.value}"'


class IntValue:
    """ IntValue """

    def __init__(self, integer_part):
        self.value = int(integer_part)


class FloatValue:
    """ FloatValue """

    def __init__(self, integer_part, fractional_part='', exponent_part=''):
        self.value = float(f'{integer_part+fractional_part+exponent_part}')


class BooleanValue:
    """ BooleanValue """

    def __init__(self, boolean_value):
        self.value = boolean_value == 'true'


class NullValue:
    """ NullValue """

    def __init__(self):
        self.value = None


class ListValue:
    """ ListValue """

    def __init__(self, value=None):
        self.value = [] if value is None else [value]


class ObjectValue:
    """ ObjectValue """

    def __init__(self, object_field=None):
        self.value = {} if object_field is None else \
            {object_field.name: object_field.value}


class ObjectField:
    """ ObjectField """

    def __init__(self, name, value):
        self.name = name
        self.value = value
