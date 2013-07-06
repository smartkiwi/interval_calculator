from interval_calculator.unused.interval_tree import range_list_to_tree, to_range_list, merge

__author__ = 'vvlad'

from random import randint, seed

import time

__author__ = 'vvlad'




# the span of the generated intervals
SPAN = 14

# the size of the genome
scale = 2
SIZE = 5*10**scale

# the number of intervals
N = 10**scale

def generate(x):
    "Generates random interval over a size and span"
    lo = randint(0, SIZE)
    hi = lo + randint(1, SPAN)
    return (lo, hi)

# use this to force both examples to generate the same data
seed(10)


startTime = time.time()

r1 = range_list_to_tree(map(generate, xrange(N)))
t = time.time() - startTime
print "%.3f seconds" % (t)

r2 = range_list_to_tree(map(generate, xrange(N)))
t = time.time() - startTime
print "%.3f seconds" % (t)


#print "r1: %s" % to_range_list(r1)
#print "r2: %s" % to_range_list(r2)

diff = merge(r1, r2, lambda a, b : a and not b)
t = time.time() - startTime
print "%.3f seconds" % (t)

print "diff: %s" % to_range_list(diff)

