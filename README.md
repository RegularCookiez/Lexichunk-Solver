# Lexichunk-Solver

Lexichunk is a word game where you have a deduce a final word by piecing together word chunks that are taken out of lists of words.

Each column of words has a specific group of letters taken away anywhere in the word. Those group of letters will be used as part the chunk word. Find the chunk word based on the removed groups of letters, from left to right.

![My Image](lexichunk_example.jpg)

To use the Python solver, simply enter the number of columns, then enter the words removed of their chunks separated by spaces.
The program will use a custom dictionary to solve for them, and output potential solutions below, separating each chunk with a slash.
