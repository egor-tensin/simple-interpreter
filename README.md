# Simple interpreter

An interpreter of a simple (deficient, really) programming language.

Here you'll find a brief description of the language and the implementation.

## The language

### Data types

Integer numbers, floating-point numbers and boolean values are supported.

Literal integer numbers are represented as sequences of digits.
Negative integer number literals are not supported.

Floating-point number literals follow a bit more complicated format with
scientific notation support.
Negative floating-point numbers literals are not supported.

Boolean values are represented as either `True` or `False`.

### Variables

Variables are named memory regions.
Numbers can be stored in memory by assigning them to variables using the
assignment operator `:=`.
A variable can be used anywhere a number can be used.

    x := 1;
    answer_to_everything := 42;
    y := x;

### Arithmetic expressions

Numbers can be computed from complex arithmetic expressions.
Addition, subtraction, multiplication, and division with grouping using
parentheses are supported.
An arithmetic expression can be used anywhere a number can be used.

    microseconds := 1000000 * seconds;

### Input/output

Basic output facilities are provided by the `print` statement.

    print 60 * 3.14 / 180;
    print days_per_year * 24;

Only numbers can be `print`ed.

### Logical expressions

Boolean values can be computed from complex logical expressions.
The language supports the conjunction (`&&`) and disjunction (`||`) operators,
as well as comparing two Boolean values using the equality (`==`) and
inequality (`!=`) operators.
A logical expression can be used anywhere a Boolean value can be used.

    if (True && False == False)
        days := 366;

Please note that operators `&&` and `||` have the same precedence.

### Control flow

Control flow is supported using the conditional `if` statement.
When executed, an `if` statement executes its body if its condition evaluates
to `True`.

    never_printed := 0;
    if (False)
        print never_printed;

### Compound statements

A compound statement (or a block) is a sequence of statements grouped together
inside a pair of curly braces (`{` and `}`).
When executed, a block executes the sequence of statements sequentially.
A block can be used anywhere a statement can be used.

    if (True) {
        days := 366;
        hours := days * 24;
        minutes := hours * 60;
        seconds := minutes * 60;
    }

### Language grammar

The language grammar in the [Extended Backus-Naur Form] (EBNF) is as follows:

    program = { statement } ;

    statement = empty_statement
              | block
              | assignment
              | print_statement
              | if_statement ;

    empty_statement = ";" ;

    block = "{" , { statement } , "}" ;

    assignment = identifier , ":=" , arithmetic_expression , ";" ;

    print_statement = "print" , arithmetic_expression , ";" ;

    arithmetic_expression = arithmetic_term , { "+" , arithmetic_term
                                              | "-" , arithmetic_term } ;
    arithmetic_term = arithmetic_factor , { "*" , arithmetic_factor
                                          | "/" , arithmetic_factor } ;
    arithmetic_factor = identifier
                      | number
                      | "(" , arithmetic_expression , ")" ;

    number = integer_number | floating_point_number ;

    integer_number = digit , { digit } ;
    digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

    (* Valid floating-point number literals: "1e1", "1e+1", "1e-1", ".1", "1.".
       Invalid floating-point number literals: "1e", ".e1". *)
    floating_point_number = integer_number , exponent
                          | integer_number , "." , { digit } , [ exponent ] ;
                          | { digit } , "." , integer_number , [ exponent ] ;
    exponent = ( "e" | "E" ) , [ "+" | "-" ] , integer_number ;

    identifier = ( LETTER | "_" ) , { LETTER | digit | "_" } ;
    (* LETTER is a symbol Python considers a letter under the current locale
       like "a", "b", "c", "X", "Y", "Z", etc. *)

    if_statement = "if" , "(" , logical_expression , ")" , statement ;

    logical_expression = logical_term , { "&&" , logical_term
                                        | "||" , logical_term } ;
    logical_term = logical_factor , [ "==" , logical_factor
                                    | "!=" , logical_factor ] ;
    logical_factor = "True"
                   | "False"
                   | "(" , logical_expression , ")" ;

[Extended Backus-Naur Form]: https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form

## Design

### Lexer

The *lexer* represents the contents of a source file as a sequence of *tokens*.
Token examples include identifiers (like `x` and `foo`), literal values (either
numeric like `42` and `3.14` or Boolean like `True`), parentheses (`(` and
`)`), arithmetic operation signs (`+`, `*`), etc.

The lexer is implemented in "src/lexer.py".

### Parser

The *parser* builds a program tree according to the rules described in the
language grammar.
Each tree node, when executed, processes its children accordingly.
For example, a node representing addition of two numbers must have exactly
two children.
When executed, such a node evaluates its children and adds the two values.

       +
      / \
     /   \
    1     2

Each of the children in the example above might in turn be represented by a
complex subtree.
For example, the right-side operand of an addition might be a multiplication of
two numbers.

        +
       / \
      /   \
     /     \
    1       *
           / \
          /   \
         2     3

An `if` statement must also have two children (its condition and body), but
executes its body only after making sure the condition evaluates to `True`.

                    if
                   /  \
            -------    -------
           /                  \
          &&                  :=
         /  \                /  \
        /    \              /    \
       /      \           days   366
      /        \
    True     False

The parser is implemented in "src/parser.py".

## Prerequisites

* Python 3

## Usage

To execute a script, pass the path to a file to "src/parser.py".

You can also pass the path to a script to "src/lexer.py" to examine the tokens
the script gets separated into.

## License

This project, including all of the files and their contents, is licensed under
terms of the MIT License.
See [LICENSE.txt] for details.

[LICENSE.txt]: LICENSE.txt
