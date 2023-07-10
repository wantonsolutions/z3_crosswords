from z3 import Solver, Int, Or, And, Distinct, sat
from tqdm import tqdm
import words as words

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




n = 5
word_list = words.get_english_words_dict_of_length(n)
print(word_list)

ROWS="ABCDEFGHI"
COLUMN="123456789"
ROWS=ROWS[0:n]
COLUMN=COLUMN[0:n]
positions = [r+c for r in ROWS for c in COLUMN]
print(positions)


problems_in = ['A1', 'A2', 'B1', 'B2']
problems = {pos: Int(pos) for pos in positions}

ltn, ntl = letters_number_map()

s = Solver()

#I need to add a constraint that prevents the same word from being used twice
for row in ROWS:
    print(row)
    ors = []
    for word in tqdm(word_list):
        ors.append(And([problems[row+col] == ltn[word[int(col)-1]] for col in COLUMN]))
    s.add(Or(ors))


for col in COLUMN:
    print(col)
    ors = []
    for word in tqdm(word_list):
        ors.append(And([problems[row+col] == ltn[word[int(ltn[row.lower()])]] for row in ROWS]))
    s.add(Or(ors))


    # s.add(Or(ands))
# print(solving)
res = s.check()
while (res == sat):
    m = s.model()
    # print(m)

    values = {pos: m.evaluate(s).as_string() for pos, s in problems.items()}
    # print(values)
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