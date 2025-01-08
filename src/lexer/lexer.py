import re

class Lxr:  # Lexer
    def __init__(self):
        self.tok_spec = [  # specs for tokens
            # DS keywords
            ('KW', r'\b(list|stack|queue|deque|set|map|tree|graph|heap|class|struct|interface|enum)\b'),

            # Ops
            ('OP', r'\b(push|pop|insert|delete|remove|search|sort|reverse|traverse|clear|new|delete|get|from)\b'),

            # DTS (Data Types)
            ('DTS', r'\b(int|float|string|char|bool|long|short|double|unsigned|signed|void|auto)\b'),

            # Access specifiers
            ('ACCESS', r'\b(public|private|protected)\b'),

            # Control keywords
            ('CTRL', r'\b(if|else|for|while|do|switch|case|break|continue|return|default|goto)\b'),

            # Preprocessor directives (simplified)
            ('PREPROC', r'\b(def|get)\b'),

            # Arithmetic operators
            ('ARITH_OP', r'[+\-*/%]'),

            # Logical operators
            ('LOGIC_OP', r'(\&\&|\|\||!)'),

            # Comparison operators
            ('COMP_OP', r'(==|!=|<|>|<=|>=)'),

            # Assignment operators
            ('ASS_OP', r'(=|\+=|\-=|\*=|/=|%=)'),

            # Funcs (simplified funcs)
            ('FUNC', r'\b(show|take|give|stop|call)\b'),

            # Syms (Symbols)
            ('SYM', r'[{}<>\\[\](),;.]'),

            # Idents (variable names)
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # Nums
            ('NUM', r'\b\d+\b'),

            # Skip spaces/tabs
            ('SKIP', r'[ \t]+'),

            # Newline
            ('NL', r'\n'),
        ]

    def tknz(self, code):  # Tokenize input code
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.tok_spec)
        get_tkn = re.compile(tok_regex).finditer

        tkns = []  # Hold tokens
        for match in get_tkn(code):
            kind = match.lastgroup
            value = match.group()
            if kind == 'SKIP':
                continue  # skip spaces
            else:
                tkns.append((kind, value))
        return tkns

if __name__ == "__main__":
    lxr = Lxr()  
    
    print("Enter Coeus code (end input with Ctrl+Z on Windows or Ctrl+D on Unix):")
    try:
        # Take multiline input from user
        code = """
""".join(iter(input, ""))
        
        tkns = lxr.tknz(code)  # tokenize dat

        for tkn in tkns:
            print(tkn)  # Show all tokens
    except RuntimeError as e:
        print(f"Error: {e}")
