import re
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    SYMBOL = auto()
    WHITESPACE = auto()
    PREPROCESSOR = auto()
    STRING = auto()
    CHAR = auto()
    COMMENT = auto()
    UNKNOWN = auto()
    ERROR = auto()

# Keywords based on the instruction
KEYWORDS = {
    "list", "queue", "deque", "priority_queue", "stack", "graph", "tree", "bst", "avl", "red_black_tree",
    "b_tree", "bplus_tree", "trie", "heap", "min_heap", "max_heap", "array", "hash_table", "linked_list",
    "singly_linked_list", "doubly_linked_list", "circular_linked_list", "skip_list",
    "LinearSearch", "BinarySearch", "TernarySearch", "InterpolationSearch", "ExponentialSearch",
    "BubbleSort", "SelectionSort", "InsertionSort", "MergeSort", "QuickSort", "HeapSort",
    "CountingSort", "RadixSort", "BucketSort", "BFS", "DFS", "Dijkstra", "BellmanFord", "FloydWarshall",
    "Kruskal", "Prim", "Kahn", "TopologicalSort", "Tarjan", "Kosaraju", "LCS", "Knapsack", 
    "MatrixChainMultiplication", "HuffmanCoding", "ActivitySelection",
    "if", "else", "switch", "case", "default", "while", "do", "for", "break", "continue", "return", "goto",
    "class", "struct", "public", "private", "protected", "virtual", "override", "static", "const", "new", "delete",
    "namespace", "using", "template", "operator", "friend", "inline", "typedef", "decltype", "constexpr", "this",
    "try", "catch", "throw", "explicit", "mutable", "final", "volatile", "show", "input"
}

# Preprocessor Directives
PREPROCESSOR_DIRECTIVES = {"#include", "#define", "#ifdef", "#ifndef", "#endif", "#undef", "#pragma", "#if", "#elif", "#else"}

# Symbols sorted by length to avoid partial matches
SYMBOLS = sorted({"(", ")", "{", "}", "[", "]", ";", ",", "=", "+", "-", "*", "/", "<", ">", "<=", ">=", "==", "!=", 
           "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", "%", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="}, key=len, reverse=True)

# Compiled regex patterns for efficiency
STRING_PATTERN = re.compile(r'"(\\.|[^"\\])*"')
CHAR_PATTERN = re.compile(r"'([^\\']|\\.)'")
NUMBER_PATTERN = re.compile(r'0x[0-9a-fA-F]+|0[0-7]+|\d+(\.\d+)?([eE][+-]?\d+)?')
WHITESPACE_PATTERN = re.compile(r'\s+')
IDENTIFIER_PATTERN = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')

TAB_WIDTH = 4  # Configurable tab width

# Helper function for updating position
def update_position(pos, lexeme, line, column):
    for char in lexeme:
        if char == '\n':
            line += 1
            column = 1
        elif char == '\t':
            column += TAB_WIDTH
        else:
            column += 1
    return pos + len(lexeme), line, column

# Tokenizer function
def tokenize(code):
    tokens = []
    pos = 0
    line, column = 1, 1
    nested_comment_depth = 0
    
    while pos < len(code):
        # Skip whitespace
        ws_match = WHITESPACE_PATTERN.match(code, pos)
        if ws_match:
            pos, line, column = update_position(pos, ws_match.group(0), line, column)
            continue
        
        # Match preprocessor directives
        if code[pos] == '#':
            end = code.find('\n', pos)
            lexeme = code[pos:end] if end != -1 else code[pos:]
            token_type = TokenType.PREPROCESSOR if lexeme.split()[0] in PREPROCESSOR_DIRECTIVES else TokenType.UNKNOWN
            tokens.append((token_type, lexeme, line, column))
            pos, line, column = update_position(pos, lexeme, line, column)
            continue
        
        # Match comments
        if code[pos:pos+2] == "/*":
            start_line = line
            start_column = column
            start_pos = pos  # Added missing variable
            nested_depth = 1
            pos += 2
            column += 2
            
            while pos < len(code) and nested_depth > 0:
                if code[pos:pos+2] == "/*":
                    nested_depth += 1
                    pos += 1
                    column += 1
                elif code[pos:pos+2] == "*/":
                    nested_depth -= 1
                    pos += 1
                    column += 1
                elif code[pos] == '\n':
                    line += 1
                    column = 1
                    pos += 1
                else:
                    column += 1
                    pos += 1
            
            if nested_depth > 0:
                tokens.append((TokenType.ERROR, "Unclosed comment", start_line, start_column))
            else:
                tokens.append((TokenType.COMMENT, code[start_pos:pos], start_line, start_column))
            continue
        
        # Match string literals and detect unclosed strings
        string_match = STRING_PATTERN.match(code, pos)
        if string_match:  # Fixed indentation
            lexeme = string_match.group(0)
            if lexeme[-1] != '"' or lexeme.count('"') < 2:
                tokens.append((TokenType.ERROR, "Unclosed string", line, column))
            else:
                tokens.append((TokenType.STRING, lexeme, line, column))
            pos, line, column = update_position(pos, lexeme, line, column)
            continue

        
        # Match character literals
        if code[pos] == "'":  # Fixed indentation
            end = pos + 1
            while end < len(code):
                if code[end] == "'" and (end == pos + 1 or code[end-1] != '\\'):
                    break
                end += 1
            else:
                tokens.append((TokenType.ERROR, "Unclosed character", line, column))
                pos += 1
                continue
            
            lexeme = code[pos:end+1]
            if CHAR_PATTERN.fullmatch(lexeme):
                tokens.append((TokenType.CHAR, lexeme, line, column))
            else:
                tokens.append((TokenType.ERROR, f"Invalid character: {lexeme}", line, column))
            pos, line, column = update_position(pos, lexeme, line, column)
            continue


        
        # Match numbers
        number_match = NUMBER_PATTERN.match(code, pos)
        if number_match:
            tokens.append((TokenType.NUMBER, number_match.group(0), line, column))
            pos, line, column = update_position(pos, number_match.group(0), line, column)
            continue
        
        # Match keywords and identifiers
        keyword_match = IDENTIFIER_PATTERN.match(code, pos)
        if keyword_match:
            lexeme = keyword_match.group(0)
            token_type = TokenType.KEYWORD if lexeme in KEYWORDS else TokenType.IDENTIFIER
            tokens.append((token_type, lexeme, line, column))
            pos, line, column = update_position(pos, lexeme, line, column)
            continue
        
        # Match symbols
        for symbol in SYMBOLS:
            if code.startswith(symbol, pos):
                tokens.append((TokenType.SYMBOL, symbol, line, column))
                pos, line, column = update_position(pos, symbol, line, column)
                break
        else:
            tokens.append((TokenType.ERROR, f"Unexpected character: {code[pos]}", line, column))
            pos += 1
    
    return tokens

# Interactive main function
if __name__ == "__main__":
    print("Welcome to the Lexer Tester!")
    print("Enter your code snippet below. Type 'exit' to quit.")
    
    while True:
        code_sample = input("\nEnter code:\n")
        if code_sample.lower() == "exit":
            print("Exiting lexer tester. Goodbye!")
            break
        
        tokens = tokenize(code_sample)
        print("\nTokens:")
        for token in tokens:
            print(token)
