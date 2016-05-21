# Simple interpreter

An interpreter of a simple artificial programming language written in Python 3.

Here you'll find a brief description of the language and the implementation.

## Simple language

This software is an interpreter of a relatively simple programming language
designed by me.

### Data types

Simple language supports integer numbers, floating-point numbers and the
Boolean data type.

Literal integer numbers are comprised of a sequence of digits.
Please note that negative integer number literals are not supported just yet.

Floating-point number literals follow a bit more complicated format, with
scientific notation support and stuff.
At the moment negative floating-point numbers literals are not supported
either.

The Boolean data type has two literal values: `True` and `False`.

### Variables

Named memory locations are called variables.
Numbers can be stored in memory by assigning them to variables using the
assignment operator `:=`.
A variable can be used anywhere a number can be used.

    x := 1;
    answer_to_everything := 42;
    y := x;

### Arithmetic expressions

Numbers can be computed from complex arithmetic expressions.
Simple language supports addition, subtraction, multiplication, and division
with grouping using parentheses.
An arithmetic expression can be used anywhere a number can be used.

    microseconds := 1000000 * seconds;

### Input/output

Simple language provides basic output facilities using the `print` statement.

    print 60 * 3.14 / 180;
    print days_per_year * 24;

Only `print`ing numbers is supported at the moment.

### Control flow

Simple language supports conditional control flow using the `if` operator.
When executed, the `if` operator executes its body statement if it's condition
evaluates to the true Boolean value.

    never_printed := 0;
    if (False)
        print never_printed;

Boolean values can be computed from complex logical expressions.
Simple language supports conjunction (`&&`) and disjunction (`||`) of logical
expressions, as well as comparing them using the equality (`==`) and inequality
(`!=`) operators.
Arguably not the most useful feature at the moment, but I am working on it.
A logical expression can be used anywhere a Boolean value can be used.

    if (True && False == False)
        days := 366;

Please note that the conditional operators `&&` and `||` have the same
precedence right now.

### Compound statement

A compound statement (or a block) is a sequence of statements grouped together
inside a pair of curly braces (`{` and `}`).
When executed, a block executes its statements sequentially.
A block can be used anywhere a statement can be used.

    if (True) {
        days := 366;
        hours := days * 24;
        minutes := hours * 60;
        seconds := minutes * 60;
    }

### Language grammar

The language grammar written in the Extended Backus&#x2012;Naur Form (EBNF) (as
described in [the corresponding Wikipedia article]
(https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_Form))
is as follows:

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

## Interpreter design

This implementation follows the conventional interpreter design principles
(more or less).

### Lexer

The *lexer* represents the contents of a source file as a sequence of *tokens*.
Token examples include identifiers (like `x` and `foo`), literal values (either
numeric like `42` and `3.14` or Boolean like `True`), parentheses (`(` and
`)`), arithmetic operation signs (`+`, `*`), etc.
The lexer is implemented in `src/lexer.py`.

### Parser

The *parser* builds a program tree according to the rules described in the
language grammar.
Each tree node processes its children accordingly.
For example, a node representing addition of two numbers must have exactly
two children.
When executed, this node evaluates its children and adds the two values.

       +
      / \
     /   \
    1     2

Each of the children in the example above might in turn be represented by a
complex subtree.
For example the right-side operand of the addition might be a result of
multiplicating two numbers.

        +
       / \
      /   \
     /     \
    1       *
           / \
          /   \
         2     3

The `if` statement also has two children (its condition and body), but executes
its body only after making sure the condition evaluates to the true Boolean
value.

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

The parser is implemented in `src/parser.py`.

## Usage

To use this software, you need to be able to run Python 3 scripts.

To execute a script written in Simple language, pass the path to the script
to `src/parser.py`.

You can also pass the path to a script to `src/lexer.py` to examine the tokens
the script gets separated into.

## License

This project, including all of the files and their contents, is licensed under
terms of the MIT License.
See [LICENSE.txt] for details.

[LICENSE.txt]: LICENSE.txt
