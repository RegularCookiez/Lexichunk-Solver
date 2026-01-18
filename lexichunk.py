import os
import re
import numpy as np
from time import perf_counter

#The dictionary is unpacked from the dictionary.txt file and loaded into a NumPy array.

dictionary = np.loadtxt("dictionary.txt", dtype=str)


#The program asks the user for the number of columns and the words in each column.

column_numbers = int(input("How many columns are there?\n"))

os.system('cls' if os.name == 'nt' else 'clear')

all_columns = []
for i in range(column_numbers):
 shortened_words = input(f"What are the shortened words in Column {i+1}?\n").split()
 all_columns.append(shortened_words)
 os.system('cls' if os.name == 'nt' else 'clear')


#The search process starts here.

process_start = perf_counter()

potential_removed_groups = []
all_possible_answers = set()

for index, x in enumerate(all_columns, start=1):
 
 all_possible_answers = set()

 for idx, y in enumerate(x):

  #Clears the terminal and informs of you the solving progress.

  os.system('cls' if os.name == 'nt' else 'clear')
  print(f"Solving column {str(index)}...\nMatching words to {y}...")


  #Iterates through the word to find all possible splits where a chunk could be.
  #Then, goes through the entire dictionary finds a chunk that fits in that split.
  #It adds any valid chunk into possible_answers.

  possible_answers = set()
  for i in range(len(y)+1):
   chunk_start = y[:i]
   chunk_end = y[i:]
   end_len = len(y)-i

   for z in dictionary:
    if y != z and z.startswith(chunk_start) and z.endswith(chunk_end):
     if end_len != 0:
      removed_chunk = z[i:len(z)-end_len]
     else:
      removed_chunk = z[i:]
     possible_answers.add(removed_chunk)


  #If this is the first word in the column, it sets the set all_possible_answers to the set of possible chunks.
  #If not, all_possible_answers is taken as the intersection between itself and possible_answers.

  if idx == 0:
   all_possible_answers = possible_answers
  else:
   all_possible_answers &= possible_answers


 #When it is done solving for every column, it generates a list of every possible chunk in each column.

 potential_removed_groups.append(all_possible_answers)


#Now, the program clears itself again and attempts every chunk combination.

os.system('cls' if os.name == 'nt' else 'clear')
print("Checking all combinations of chunks...")


#It constructs a regex query to check for chunk combinations, and compiles it.

pattern = re.compile("^" + "".join(f"({'|'.join(x)})" for x in potential_removed_groups) + "$")


#It then finds words matching that pattern, and uses groups() to demarcate chunks with slashes, adding it to valid_solutions.

valid_solutions = []
for w in dictionary:
 match = pattern.match(w)
 if match:
  chunks = match.groups()
  slashed_word = "/".join(chunks)
  valid_solutions.append(slashed_word)


#perf_counter is used here to calculate the time taken for the search.

process_end = perf_counter()


#When the search is completed, a quick overview of the search results is shown.

os.system('cls' if os.name == 'nt' else 'clear')

print("Lexichunk Solved!\n")
for index, x in enumerate(all_columns, start=1):
 print(f'Column {index}: {" ".join(x)}')

print('\nAll Possible Chunks:')
for index, x in enumerate(potential_removed_groups, start=1):
 unslashed_list = [y.replace("/","") for y in x]
 print(f'Column {index}: {", ".join(unslashed_list)}')

print(f'\nAll Solutions ({len(valid_solutions)})\n{", ".join(valid_solutions)}')
print(f"\nSearch completed in {round(process_end-process_start,2)}s.")
