from random import randint, seed

import time

__author__ = 'vvlad'


from interval_calculator.unused.interval import Interval, IntervalSet
r1 = IntervalSet([Interval(1, 1000), Interval(1100, 1200)])
r2 = IntervalSet([Interval(30, 50), Interval(60, 200), Interval(1150, 1300)])
print(r1 - r2)


# the span of the generated intervals
SPAN = 14

# the size of the genome
scale = 3
SIZE = 5*10**scale

# the number of intervals
N = 10**scale

def generate(x):
    "Generates random interval over a size and span"
    lo = randint(0, SIZE)
    hi = lo + randint(1, SPAN)
    return Interval(lo, hi)

# use this to force both examples to generate the same data
seed(10)

input1 = IntervalSet(map(generate, xrange(N)))
print len(input1)
print input1

seed(100123)
input2 = IntervalSet(map(generate, xrange(N)))
print len(input2)
print input2

startTime = time.time()

result = input1 - input2

t = time.time() - startTime
print "%.3f seconds" % (t)


print len(result)
print result