# CPY Language Compiler to RISC-V Assembly

## Contributors

* Anastasios-Orestis Stefas (4916)
* Amalia-Georgia Mouselimi (5074)
* University of Ioannina - Department of Computer Science and Engineering

---

## Project Description

This project is a fully functional compiler for the **cpy programming language**, developed for the *Compilers course (February 2024)*.

The compiler is written in **Python** and generates **RISC-V assembly** as the final output.

The *cpy* language is a specialized programming language that supports:

* Nested functions and Pascal-style scoping rules
* Parameter passing and recursive calls
* Integer data types (range -32767 to 32767)
* Global variable access using the `global` keyword

---

## Features & Implementation

The compiler was developed in four distinct phases:

* **Lexical Analysis**
  Tokenizes the source code using a custom lexical analyzer

* **Syntax Analysis**
  Implements a Recursive Descent Parser based on the EBNF grammar

* **Intermediate Code**
  Generates quads (quadruplets) and handles temporary variables

* **Symbol Table & Final Code**
  Manages scopes and entities to produce executable RISC-V assembly code

---

## File Structure

* `cpy_code.py`: The main compiler implementation
* `cpy_report.pdf`: Detailed technical documentation of the project
* `cpyGrammar.txt`: The formal EBNF grammar of the cpy language
* `test1.cpy`, `test2.cpy`, `symbol_test.cpy`: Test programs for validation
* `ProgramLanguageCPY.pdf`: The original language specification

---

## How to Run

To compile a cpy source file, use the following command:

```bash
python cpy_code.py your_file.cpy
```

The compiler will generate:

* A `.int` file containing the intermediate code (quads)
* A `.symb` file containing the Symbol Table
* A `.asm` file containing the final RISC-V Assembly code
