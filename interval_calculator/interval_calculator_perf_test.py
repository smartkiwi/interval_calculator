from random import randint, seed
import unittest
import time
from interval_calculator.intervals_calculator import merge_intervals, calculate_duration_in_period, intersect_sorted_intervals, substract_intervals, intersect_intervals, substract_intervals_itree




# the span of the generated intervals
SPAN = 14

# the size of the genome
scale = 4
SIZE = 5*10**scale

# the number of intervals
N = 10**scale

def generate(x):
    "Generates random interval over a size and span"
    lo = randint(0, SIZE)
    hi = lo + randint(1, SPAN)
    return [lo, hi]

# use this to force both examples to generate the same data
seed(10)



class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.__startTime = time.time()


    def _curr_duration(self):
        t = time.time() - self.__startTime
        print "%s: %.3f seconds" % (self.id(), t)

    def tearDown(self):
        self._curr_duration()



    def test_perf1(self):
        # generate 10 thousand random intervals
        seed(10)
        input = map(generate, xrange(N))
        self._curr_duration()
        #input = [ [0,50],[45,80],[70,90], [100,150],[120,180], [190,210],[200,250]]
        print len(input)
        result = merge_intervals(input,False)
        print len(result)
        self._curr_duration()
        duration = calculate_duration_in_period(result)
        print duration
        self._curr_duration()
    def test_perf2(self):
        # generate 10 thousand random intervals
        seed(10)
        input1 = map(generate, xrange(N))
        self._curr_duration()
        seed(2000)
        input2 = map(generate, xrange(N))
        self._curr_duration()

        print "input1 interval size: %s" % len(input1)
        print "input1 interval size: %s" % len(input2)
        result1 = merge_intervals(input1,False)
        print "merged sorted interval1 size: %s" % len(result1)
        self._curr_duration()
        duration = calculate_duration_in_period(result1)
        print "result 1 total duration: %s"  % duration
        result2 = merge_intervals(input2,False)
        print "merged sorted interval2 size: %s" % len(result2)
        self._curr_duration()
        duration = calculate_duration_in_period(result2)
        print "result 2 total duration: %s"  % duration
        self._curr_duration()
        substr_result = substract_intervals(input1,input2)
        print "substruct input1-input2: %s" % substr_result
        print "substruct duration %s" % calculate_duration_in_period(substr_result)



        self._curr_duration()
        #duration = calculate_duration_in_period(intersect)
        #print duration
        self._curr_duration()




    def test_perf2_fast(self):
        # generate 10 thousand random intervals
        seed(10)
        input1 = map(generate, xrange(N))
        self._curr_duration()
        seed(2000)
        input2 = map(generate, xrange(N))
        self._curr_duration()

        print "input1 interval size: %s" % len(input1)
        print "input1 interval size: %s" % len(input2)
        result1 = merge_intervals(input1,False)
        print "merged sorted interval1 size: %s" % len(result1)
        self._curr_duration()
        duration = calculate_duration_in_period(result1)
        print "result 1 total duration: %s"  % duration
        result2 = merge_intervals(input2,False)
        print "merged sorted interval2 size: %s" % len(result2)
        self._curr_duration()
        duration = calculate_duration_in_period(result2)
        print "result 2 total duration: %s"  % duration
        self._curr_duration()
        substr_result = substract_intervals_itree(input1,input2)
        print "substract_intervals_itree input1-input2: %s" % substr_result
        print "substract_intervals_itree duration %s" % calculate_duration_in_period(substr_result)



        self._curr_duration()
        #duration = calculate_duration_in_period(intersect)
        #print duration
        self._curr_duration()
