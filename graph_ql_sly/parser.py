# pylint: disable=W0108, R0914, W0703, C0111, E0601

"""
Lexer and Parser code.  Given a valid graphql string, it spits out a parse tree.
"""

import codecs
from sly import Lexer, Parser
from .parse_objects import *

ESCAPE_DECODER = codecs.getdecoder("unicode_escape")


def decode_escape(escaped_value):
    """ translates escaped characters into their character values """
    return ESCAPE_DECODER(escaped_value)[0]


class GraphQLLexer(Lexer):
    # token names
    tokens = {
        NAME,
        INTEGER_PART,
        FRACTIONAL_PART,
        EXPONENT_PART,
        ZERO_VALUE,
        BLOCKSTRING_DELIMITER,
        STRING_DELIMITER,
        QUERY,
        TRUE,
        FALSE,
        NULL,
    }
    literals = {'!', '$', '(', ')', '...', ':', '=',
                '@', '[', ']', '{', '|', '}'}
    ignore = ',\ufeff\u0009\u0020\n'
    ignore_comment = r'\#.*\n'

    ZERO_VALUE = r'[-]?0'
    INTEGER_PART = r'[-]?[0-9]+'
    FRACTIONAL_PART = r'[.][0-9]+'
    EXPONENT_PART = r'[eE][+-]?[0-9]+'

    @_(r'[\"]{3}')
    def BLOCKSTRING_DELIMITER(self, t):
        self.push_state(GraphQLLexerBlockString)
        return t

    @_(r'[\"]{1}')
    def STRING_DELIMITER(self, t):
        self.push_state(GraphQLLexerString)
        return t

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['query'] = QUERY
    NAME['true'] = TRUE
    NAME['false'] = FALSE
    NAME['null'] = NULL


class GraphQLLexerBlockString(Lexer):
    tokens = {
        BLOCKSTRING_DELIMITER,
        ESCAPED_CHAR,
        QUOTE_CHAR,
        STRING_SOURCE
    }
    #literals = {'\\'}

    @_(r'[\"]{3}')
    def BLOCKSTRING_DELIMITER(self, t):
        self.pop_state()
        return t

    ESCAPED_CHAR = r'[\\]["\\/bfnrt]'
    QUOTE_CHAR = r'[\"]+'
    STRING_SOURCE = r'[\u0009\u000A\u000D\u0020-\u0021\u0023-\u005b\u005d-\uFFFF]+'


class GraphQLLexerString(Lexer):
    tokens = {
        STRING_DELIMITER,
        ESCAPED_CHAR,
        STRING_SOURCE
    }
    # literals = {'\\'}

    @_(r'[\"]{1}')
    def STRING_DELIMITER(self, t):
        self.pop_state()
        return t

    ESCAPED_CHAR = r'[\\]["\\/bfnrt]'
    STRING_SOURCE = r'[\u0009\u000A\u000D\u0020-\u0021\u0023-\u005b\u005d-\uFFFF]+'


class GraphQLParser(Parser):
    tokens = GraphQLLexer.tokens | \
        GraphQLLexerString.tokens | \
        GraphQLLexerBlockString.tokens

    # value stuff

    @_(
        'float_value',
        'int_value',
        'string_value',
        'boolean_value',
        'null_value',
        'list_value',
        'object_value',
    )
    def value(self, p):
        return Value(p[0])

    # lists

    @_('list_start "]"')
    def list_value(self, p):
        return p.list_start

    @_('"[" "]"')
    def list_value(self, p):
        return ListValue()

    @_('list_start value')
    def list_start(self, p):
        p.list_start.value.append(p.value.value)
        return p.list_start

    @_('"[" value')
    def list_start(self, p):
        return ListValue(p.value.value)

    # objects

    @_('object_start }')
    def object_value(self, p):
        return p.object_start

    @_('"{" "}"')
    def object_value(self, p):
        return ObjectValue()

    @_('object_start NAME ":" value')
    def object_start(self, p):
        p.object_start.value[p.NAME] = p.value.value
        return p.object_start

    @_('"{" NAME ":" value')
    def object_start(self, p):
        return ObjectValue(ObjectField(p.NAME, p.value.value))

    # nulls

    @_("NULL")
    def null_value(self, p):
        return NullValue()

    # floats

    @_("INTEGER_PART FRACTIONAL_PART EXPONENT_PART")
    def float_value(self, p):
        return FloatValue(integer_part=p.INTEGER_PART,
                          fractional_part=p.FRACTIONAL_PART,
                          exponent_part=p.EXPONENT_PART)

    @_("INTEGER_PART FRACTIONAL_PART")
    def float_value(self, p):
        return FloatValue(integer_part=p.INTEGER_PART,
                          fractional_part=p.FRACTIONAL_PART)

    @_("INTEGER_PART EXPONENT_PART")
    def float_value(self, p):
        return FloatValue(integer_part=p.INTEGER_PART,
                          fractional_part=p.EXPONENT_PART)

    # ints

    @_("INTEGER_PART")
    def int_value(self, p):
        return IntValue(integer_part=p.INTEGER_PART)

    # bools

    @_("TRUE", "FALSE")
    def boolean_value(self, p):
        return BooleanValue(boolean_value=p[0])

    # string stuff

    @_('STRING_DELIMITER string_character STRING_DELIMITER')
    def string_value(self, p):
        return StringValue(p.string_character)

    @_('STRING_DELIMITER empty STRING_DELIMITER')
    def string_value(self, p):
        return StringValue('')

    @_('')
    def empty(self, p):
        return ''

    @_('STRING_SOURCE string_character')
    def string_character(self, p):
        return p.STRING_SOURCE + p.string_character

    @_('ESCAPED_CHAR string_character')
    def string_character(self, p):
        return decode_escape(p.ESCAPED_CHAR) + p.string_character

    @_('STRING_SOURCE')
    def string_character(self, p):
        return (p.STRING_SOURCE)

    @_('ESCAPED_CHAR')
    def string_character(self, p):
        return decode_escape(p.ESCAPED_CHAR)
