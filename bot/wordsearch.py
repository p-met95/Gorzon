import numpy as np
from english_words import english_words_alpha_set
import string
import random
import copy


def wordcheck(word, word_coords, placed_words):
    p_words = ''.join(placed_words.keys())
    p_coords = sum(placed_words.values(), [])

    trutharray = []

    for letter, coord in zip(word, word_coords):

        if coord not in p_coords:
            trutharray.append(True)
        else:
            if p_words[p_coords.index(coord)] == letter:
                trutharray.append(True)
            else:
                trutharray.append(False)

    if sum(trutharray) == len(word):
        return True
    else:
        return False


class Wordgen:

    def __init__(self, maxlen):
        valid = [w for w in english_words_alpha_set if len(w) <= maxlen]

        self.word = random.choice(valid).upper()
        self.length = len(self.word)


class Grid:

    def __init__(self, dim, numw):

        self.dim = dim
        upalph = list(string.ascii_uppercase)
        randlet = [random.choice(upalph) for cell in range(dim * dim)]

        self.grid = np.reshape(np.array(randlet), (-1, dim))
        self.numw = numw
        self.words = [Wordgen(dim) for i in range(numw)]

    def listw(self):
        for i in self.words:
            return '\n'.join(i.word)

    def populate(self):

        self.allcoords = {}

        cmsg = 'Unable to converge, please try again with less words or a larger grid.'

        for word in self.words:

            self.rollback_g = copy.deepcopy(self.grid)
            bad_coord = []
            iters = 10000  # limit for number of tries before giving up

            for iteration in range(iters):

                while True:


                    cur_bc = copy.deepcopy(bad_coord)

                    # pick random direction to rotate word
                    direction = random.choice(['u', 'd', 'l', 'r', 'ul', 'ur', 'dl', 'dr'])
                    # pick random start point
                    ub, db, lb, rb = 0, self.dim - 1, 0, self.dim - 1

                    # alter bounds based on direction and length of word
                    if direction == 'r':
                        rb = rb - word.length + 1
                    elif direction == 'l':
                        lb = lb + word.length - 1
                    elif direction == 'd':
                        db = db - word.length + 1
                    elif direction == 'u':
                        ub = ub + word.length - 1
                    elif direction == 'ul':
                        ub = ub + word.length - 1
                        lb = lb + word.length - 1
                    elif direction == 'ur':
                        ub = ub + word.length - 1
                        rb = rb - word.length + 1
                    elif direction == 'dl':
                        db = db - word.length + 1
                        lb = lb + word.length - 1
                    elif direction == 'dr':
                        db = db - word.length + 1
                        rb = rb - word.length + 1

                    x = random.randint(lb, rb)
                    y = random.randint(ub, db)

                    attempt = [x, y, direction]

                    if len(cur_bc) == len(bad_coord):
                        raise StopIteration(cmsg)

                    # checks if it's already tried the coordinate combo and if it has make a new one
                    if attempt not in bad_coord:
                        break


                # grid[y][x]
                letters = list(word.word)
                wcoords = []

                if direction == 'r':
                    for i in range(word.length):
                        self.grid[y][x + i] = letters[i]
                        wcoords.append([y, x + i])

                elif direction == 'l':
                    for i in range(word.length):
                        self.grid[y][x - i] = letters[i]
                        wcoords.append([y, x - i])

                elif direction == 'd':
                    for i in range(word.length):
                        self.grid[y + i][x] = letters[i]
                        wcoords.append([y + i, x])

                elif direction == 'u':
                    for i in range(word.length):
                        self.grid[y - i][x] = letters[i]
                        wcoords.append([y - i, x])

                elif direction == 'ul':
                    for i in range(word.length):
                        self.grid[y - i][x - i] = letters[i]
                        wcoords.append([y - i, x - i])

                elif direction == 'ur':
                    for i in range(word.length):
                        self.grid[y - i][x + i] = letters[i]
                        wcoords.append([y - i, x + i])

                elif direction == 'dl':
                    for i in range(word.length):
                        self.grid[y + i][x - i] = letters[i]
                        wcoords.append([y + i, x - i])

                elif direction == 'dr':
                    for i in range(word.length):
                        self.grid[y + i][x + i] = letters[i]
                        wcoords.append([y + i, x + i])

                if wordcheck(word.word, wcoords, self.allcoords):
                    print(f'{word.word} succeeded on iteration {iteration + 1}.')
                    break

                if iteration == iters - 1:
                    raise StopIteration(cmsg)

                else:
                    print(f'{word.word} iteration {iteration + 1} failed, trying again.')
                    self.grid = copy.deepcopy(self.rollback_g)
                    bad_coord.append([x, y, direction])

            self.allcoords[word.word] = wcoords

    def prettyprint(self):
        return '\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in self.grid])


