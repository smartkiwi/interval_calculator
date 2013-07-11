__author__ = 'vvlad'
import time
from random import randint, seed

# if you can install bx python then uncomment the line below
#
# from bx.intervals.operations.quicksect import IntervalNode

# otherwise just download the quickset module as shown above
# and place it in next to your program
#
from quicksect import IntervalNode

# the span of the generated intervals
SPAN = 10

# the size of the genome
scale = 5
SIZE = 5*10** scale

# the number of intervals
N = 10** scale

def generate(x):
    "Generates random interval over a size and span"
    lo = randint(10000, SIZE)
    hi = lo + randint(1, SPAN)
    return (lo, hi)

def find(start, end, tree):
    "Returns a list with the overlapping intervals"
    out = []
    tree.intersect( start, end, lambda x: out.append(x) )
    return [ (x.start, x.end) for x in out ]

# use this to force both examples to generate the same data
seed(10)

starttime = time.clock()
# generate 10 thousand random intervals
data = map(generate, xrange(N))
print "%f generating %s intervals" % (time.clock() - starttime, N)

# generate the intervals to query over
seed(1231231)
starttime = time.clock()
query = map(generate, xrange(N))
print "%f generating %s query intervals" % (time.clock() - starttime, N)

# start the root at the first element
start, end = data[0]
tree = IntervalNode( start, end )

starttime = time.clock()
# build an interval tree from the rest of the data
for start, end in data[1:]:
    tree = tree.insert( start, end )
print "%f building tree with %s intervals" % (time.clock() - starttime, N)

starttime = time.clock()
for start, end in query:
    overlap = find(start, end , tree)
    #print '(%s, %s) -> %s' % (start, end, overlap)

print "%f query" % (time.clock() - starttime)