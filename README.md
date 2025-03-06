# Coeus Compiler

## Overview

Coeus is a **custom programming language compiler** that natively supports **data structures and algorithms** as first-class constructs. The lexer is a core component responsible for **tokenizing source code** into meaningful tokens for parsing and compilation.

## Features

- **Innate support for Data Structures & Algorithms** (e.g., linked lists, trees, heaps, graphs, sorting/searching algorithms).
- **Custom Lexer** that efficiently tokenizes Coeus source code.
- **Optimized Token Matching** with regex-based lexing.
- **Preserves Line/Column Positions** for improved error handling.

## Repository Structure

```
/coeus-compiler
│── README.md        # General project overview
│── docs/
│   ├── lexer.md     # Detailed lexer documentation
│── src/
│   ├── lexer.py     # Lexer implementation
│── tests/
│   ├── lexer_test.py # Unit tests for lexer
```

## Getting Started

### **1. Clone the Repository**
### **2. Running the Lexer**

You can test the lexer interactively:

```sh
python src/lexer.py
```

Enter Coeus code and see tokenized output. Type `exit` to quit.

### **3. Running Tests**

Ensure lexer functionality by running unit tests:

```sh
pytest tests/lexer_test.py
```

## Documentation

For a detailed breakdown of the lexer’s implementation, check [**docs/lexer.md**](docs/lexer.md).

## Contributing

- Fork the repository.
- Create a feature branch (`feature-branch-name`).
- Commit your changes with descriptive messages.
- Open a pull request.

## License

This project is licensed under the MIT License.

