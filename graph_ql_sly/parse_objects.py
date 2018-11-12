"""
contains definitions of the supplementary parse objects
"""

INDENT = '  '

class StringValue:
    """ StringValue """

    def __init__(self, string_characters):
        self.value = string_characters

    def __repr__(self):
        return f'StringValue("{self.value}")'

    def __str__(self):
        return f'"{self.value}"'


class Document:
    """ Document """

    def __init__(self, definition):
        self.definitions = [definition]


class Definition:
    """ Definition """

    def __init__(self, definition, offset=''):
        self.definition = definition
        self.offset = offset

    def __repr__(self):
        return f'Definition(\n{INDENT}{self.offset}{self.definition!r}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        self.definition.set_offset(offset + f'{INDENT}')


class ExecutableDefinition:
    """ ExecutableDefinition """

    def __init__(self, definition, offset=''):
        self.definition = definition
        self.offset = offset

    def __repr__(self):
        return f'ExecutableDefinition(\n{INDENT}{self.offset}{self.definition!r}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        self.definition.set_offset(offset + f'{INDENT}')


class OperationDefinition:
    """ OperationDefinition """

    def __init__(self, selection_set, operation_type='query', name=None,
                 variable_definitions=None, directives=None, offset=''):
        self.selection_set = selection_set
        self.operation_type = operation_type
        self.name = name
        self.variable_definitions = variable_definitions
        self.directives = directives
        self.offset = offset

    def __repr__(self):
        return f'OperationDefinition(\n' + \
            self.offset + f'{INDENT}operation_type={self.operation_type!r}, \n' +\
            self.offset + f'{INDENT}name={self.name!r}, \n' + \
            self.offset + f'{INDENT}selection_set={self.selection_set!r}\n' + \
            self.offset + ')'

    def set_offset(self, offset=''):
        self.offset = offset
        self.selection_set.set_offset(offset + f'{INDENT}')


class SelectionSet:
    """ SelectionSet """

    def __init__(self, selection, offset=''):
        self.selections = [selection]
        self.offset = offset

    def __repr__(self):
        selections_repr = f',\n{self.offset}{INDENT}'.join(i.__repr__() for i in self.selections)
        return f'SelectionSet(\n{self.offset}{INDENT}{selections_repr}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        for selection in self.selections:
            selection.set_offset(offset + f'{INDENT}')


class Selection:
    """ Selection """

    def __init__(self, field, offset=''):
        self.field = field
        self.offset = offset

    def __repr__(self):
        return f'Selection(\n{self.offset}{INDENT}{self.field!r}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        self.field.set_offset(offset + f'{INDENT}')


class Field:
    """ Field """

    def __init__(self, name, alias=None, arguments=None, directives=None,
                 selection_set=None, offset=''):
        self.name = name
        self.alias = alias
        self.arguments = arguments
        self.directives = directives
        self.selection_set = selection_set
        self.offset = offset

    def __repr__(self):
        return f'Field(\n' + \
            self.offset + f'{INDENT}name={self.name!r}, \n' +\
            self.offset + f'{INDENT}arguments={self.arguments!r}, \n' + \
            self.offset + f'{INDENT}selection_set={self.selection_set!r}\n' + \
            self.offset + ')'

    def set_offset(self, offset=''):
        self.offset = offset
        if self.arguments:
            self.arguments.set_offset(offset + f'{INDENT}')
        if self.selection_set:
            self.selection_set.set_offset(offset + f'{INDENT}')


class Arguments:
    """ Arguments """

    def __init__(self, argument, offset=''):
        self.arguments = [argument]
        self.offset = ''

    def __repr__(self):
        argument_repr = f',\n{self.offset}{INDENT}'.join(i.__repr__() for i in self.arguments)
        return f'Arguments(\n{self.offset}{INDENT}{argument_repr}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        if self.arguments:
            for argument in self.arguments:
                argument.set_offset(offset + f'{INDENT}')


class Argument:
    """ Argument """

    def __init__(self, name, value, offset=''):
        self.name = name
        self.value = value
        self.offset = ''

    def __repr__(self):
        return f'Argument(\n{self.offset}{INDENT}name={self.name},\n{self.offset}{INDENT}value={self.value}\n{self.offset})'

    def set_offset(self, offset=''):
        self.offset = offset
        try:
            self.value.set_offset(offset + f'{INDENT}')
        except AttributeError:
            pass


class Value:
    """ Value """

    def __init__(self, value, offset=''):
        self.value = value.value
        self.offset = offset

    def __repr__(self):
        return self.offset + f'Value("{self.value}")'

    def __str__(self):
        return f'"{self.value}"'

    def set_offset(self, offset=''):
        self.offset = offset
        try:
            self.value.set_offset(offset + f'{INDENT}')
        except AttributeError:
            pass


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
