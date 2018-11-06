# pylint: disable=W0108, R0914, W0703, C0111, E0601

"""
Parser code.  Given a valid graphql string, it spits out a parse tree.
"""

from sly import Lexer #, Parser


class GraphQLLexer(Lexer):
    # token names
    tokens = {
        NAME,
        INTEGER_PART,
        FRACTIONAL_PART,
        EXPONENT_PART,
        ZERO_VALUE,
        BLOCKSTRING_DELIMITER,
        STRING_DELIMITER
    }
    literals = {'!', '$', '(', ')', '...', ':', '=',
                '@', '[', ']', '{', '|', '}'}
    ignore = ',\ufeff\u0009\u0020'
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

# class GraphQLParser(Parser):
#     tokens = GraphQLLexer.tokens
