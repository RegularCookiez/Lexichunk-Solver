import os
import re
import numpy as np
from itertools import product
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
all_possible_answers = []

for x in all_columns:
 
 all_possible_answers = []

 for y in x:

  #Clears the terminal and informs of you the solving progress.

  os.system('cls' if os.name == 'nt' else 'clear')
  print(f"Solving column {str(all_columns.index(x)+1)}...")
  print(f"Matching words to {y}...")


  #Creates a list of all possible regexes that can check for full words with missing chunks.
  #It checks for a word that has any amount of filler letters in any index of the word.

  possible_answers = []
  regex_needed = []
  for i in range(len(y)+1):
   regex_needed.append(f"^{y[:i]}.*{y[i:]}$")


  #Searches the dictionary and checks for any words that match the given words in the column.
  #Via string slicing, the chunk word is then deduced.

  for z in dictionary:
   for r in regex_needed:
    if re.search(r, z) and y != z:
     if -len(r)+r.index(".*")+3 != 0:
      removed_chunk = z[r.index(".*")-1:-len(r)+r.index(".*")+3]
     else:
      removed_chunk = z[r.index(".*")-1:]
     possible_answers.append(removed_chunk)


  #If this is the first word in the column, it sets all the list all_possible_answers to the possible chunks.
  #If not, it is addended to the list all_possible_answers and converted into a set which will only have chunks valid in every word in the column.

  if x.index(y) == 0:
   all_possible_answers = possible_answers
  else:
   all_possible_answers = list(set(all_possible_answers).intersection(set(possible_answers)))


 #When it is done solving for every column, it generates a list of every possible chunk in each column, with a slash for readability later on.

 if all_columns.index(x) != len(all_columns)-1:
  all_possible_answers = [f"{x}/" for x in all_possible_answers]
 potential_removed_groups.append(all_possible_answers)


#Now, the program clears itself again and attempts every chunk combination.

os.system('cls' if os.name == 'nt' else 'clear')
print("Checking all combinations of chunks...")


#It generates every possible combination of every potential chunk from each column, and checking it with the dictionary to see if it is a word.

all_combinations = list(product(*potential_removed_groups))

all_combinations = np.array(["".join(x) for x in all_combinations.copy()])

valid_solutions = []


#Chunks that combine to form real words are added to the valid_solutions list.

for x in all_combinations:
 if x.replace("/","") in dictionary:
  valid_solutions.append(x)


#perf_counter is used here to calculate the time taken for the search.
process_end = perf_counter()


#When the search is completed, a quick overview of the search results is shown.

os.system('cls' if os.name == 'nt' else 'clear')

print("Lexichunk Solved!\n")
for x in all_columns:
 print(f'Column {str(all_columns.index(x)+1)}: {" ".join(x)}')

print('\nAll Possible Chunks:')
for x in potential_removed_groups:
 unslashed_list = [y.replace("/","") for y in x]
 print(f'Column {potential_removed_groups.index(x)+1}: {", ".join(unslashed_list)}')

print(f'\nAll Solutions ({len(valid_solutions)})\n{", ".join(valid_solutions)}')

print(f"\nSearch completed in {round(process_end-process_start,2)}s.")
