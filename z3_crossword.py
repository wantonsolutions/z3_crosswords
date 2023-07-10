from z3 import Solver, Int, Or, And, Distinct, sat
from tqdm import tqdm
import words as words
import random

usage = "Usage: python3 z3_crossword.py <n> where n is the size of the crossword between 1 and 9"

def letters_number_map():
    alpha = "abcdefghijklmnopqrstuvwxyz"
    ltn = dict()
    ntl = dict()
    i=0
    for letter in alpha:
        ltn[letter] = i
        ntl[i] = letter
        i+=1
    return ltn, ntl

def set_up_problem(n):
    ROWS="ABCDEFGHI"
    COLUMN="123456789"
    ROWS=ROWS[0:n]
    COLUMN=COLUMN[0:n]
    positions = [r+c for r in ROWS for c in COLUMN]
    problems = {pos: Int(pos) for pos in positions}
    return problems, ROWS, COLUMN

def set_up_solver(n):
    word_list = words.get_english_words_dict_of_length(n)
    random.shuffle(word_list)
    ltn, ntl = letters_number_map()
    problems, ROWS, COLUMN = set_up_problem(n)
    s = Solver()

    #I need to add a constraint that prevents the same word from being used twice
    for row in ROWS:
        ors = []
        for word in tqdm(word_list):
            ors.append(And([problems[row+col] == ltn[word[int(col)-1]] for col in COLUMN]))
        s.add(Or(ors))


    for col in COLUMN:
        ors = []
        for word in tqdm(word_list):
            ors.append(And([problems[row+col] == ltn[word[int(ltn[row.lower()])]] for row in ROWS]))
        s.add(Or(ors))
    return s

def solve_continuously(s, n):
    problems, ROWS, COLUMN = set_up_problem(n)
    ltn, ntl = letters_number_map()
    res = s.check()
    while (res == sat):
        m = s.model()

        values = {pos: m.evaluate(s).as_string() for pos, s in problems.items()}
        i = 0
        rows = n
        for v in values :
            print(ntl[int(values[v])], end="")
            i+=1
            if i == rows:
                print()
                i=0
        print()

        block = []
        for var in m:
            block.append(var() != m[var])
        s.add(Or(block))
        res = s.check()

def get_n_from_user():
    import sys
    if len(sys.argv) != 2:
        print(usage)
        exit()
    try:
        n = int(sys.argv[1])
    except:
        print(usage)
        exit()
    
    if n < 1 or n > 9:
        print(usage)
        exit()

    return n


n = get_n_from_user()
s = set_up_solver(n)
solve_continuously(s, n)
