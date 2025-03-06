# Coeus Lexer Documentation

## Overview
The Coeus Lexer is responsible for **tokenizing** Coeus source code into distinct tokens, which are then processed by the parser and compiler. It efficiently identifies **keywords, identifiers, numbers, symbols, preprocessor directives, strings, characters, and comments**, ensuring correct lexical analysis.

## Features
- **Recognizes and tokenizes all Coeus keywords, operators, and structures.**
- **Handles nested comments and escape sequences in strings and characters.**
- **Detects and reports errors** such as unclosed strings, comments, and invalid tokens.
- **Maintains line and column positions** to improve error reporting.
- **Optimized regular expressions** for fast tokenization.
- **Interactive mode available for testing.**

## Token Types
Tokens are categorized using the `TokenType` enum:

```python
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
```

## Recognized Tokens
| **Token Type** | **Description** |
|--------------|-----------------|
| **Keywords** | Built-in data structures, control flow statements, and algorithms. |
| **Identifiers** | Variable and function names. |
| **Numbers** | Integer and floating-point numbers. |
| **Symbols** | Operators and delimiters. |
| **Preprocessor Directives** | `#include`, `#define`, etc. |
| **Strings** | Enclosed in `" "`, supporting escape sequences. |
| **Characters** | Enclosed in `' '`, supporting escape sequences. |
| **Comments** | Single-line (`//`) and multi-line (`/* ... */`). |
| **Whitespace** | Tabs, spaces, and newlines. |
| **Errors** | Unrecognized characters or improperly closed constructs. |

## Tokenization Process
### Step 1: Preprocessing
- Ignore **whitespace** unless inside a string or comment.
- Detect and handle **preprocessor directives**.

### Step 2: Token Matching Order
1. **Whitespace** (skipped)
2. **Preprocessor directives**
3. **Multi-line comments (`/* ... */`)**
4. **Single-line comments (`// ...`)**
5. **String literals (`" ... "`)**
6. **Character literals (`' ... '`)**
7. **Numbers**
8. **Identifiers (keywords checked first)**
9. **Symbols**
10. **Error detection for unknown tokens**

### Step 3: Position Tracking
- Maintains **line and column numbers** to improve debugging.
- Handles **tabs with configurable width (default: 4 spaces)**.

## Example Usage
### Input Code
```coeus
list<int> myList;
myList.insert(10);
// Comment Example
if (myList.find(10)) {
    show "Found";
}
```

### Tokenized Output
```plaintext
(TokenType.KEYWORD, 'list', 1, 1)
(TokenType.SYMBOL, '<', 1, 5)
(TokenType.KEYWORD, 'int', 1, 6)
(TokenType.SYMBOL, '>', 1, 9)
(TokenType.IDENTIFIER, 'myList', 1, 11)
(TokenType.SYMBOL, ';', 1, 17)
(TokenType.IDENTIFIER, 'myList', 2, 1)
(TokenType.SYMBOL, '.', 2, 7)
(TokenType.IDENTIFIER, 'insert', 2, 8)
(TokenType.SYMBOL, '(', 2, 14)
(TokenType.NUMBER, '10', 2, 15)
(TokenType.SYMBOL, ')', 2, 17)
(TokenType.SYMBOL, ';', 2, 18)
(TokenType.COMMENT, '// Comment Example', 4, 1)
(TokenType.KEYWORD, 'if', 5, 1)
(TokenType.SYMBOL, '(', 5, 4)
(TokenType.IDENTIFIER, 'myList', 5, 5)
(TokenType.SYMBOL, '.', 5, 11)
(TokenType.IDENTIFIER, 'find', 5, 12)
(TokenType.SYMBOL, '(', 5, 16)
(TokenType.NUMBER, '10', 5, 17)
(TokenType.SYMBOL, ')', 5, 19)
(TokenType.SYMBOL, ')', 5, 20)
(TokenType.SYMBOL, '{', 5, 22)
(TokenType.KEYWORD, 'show', 6, 5)
(TokenType.STRING, '"Found"', 6, 10)
(TokenType.SYMBOL, ';', 6, 17)
(TokenType.SYMBOL, '}', 7, 1)
```

## Running the Lexer
### 1. Interactive Mode
Run the lexer to test tokenization interactively:
```sh
python src/lexer.py
```
- Enter Coeus code and see tokenized output.
- Type `exit` to quit.

### 2. Running Tests
Ensure lexer functionality by running unit tests:
```sh
pytest tests/lexer_test.py
```

## What I'm Planning to add:
- Improve **error recovery** for incomplete syntax.
- Implement **symbol table integration** for better identifier tracking.
- Add **support for user-defined types**.
- Expand **error messaging** for clearer debugging.

