'''

@author: Volodymyr Vladymyrov smartkiwi@gmail.com

Time Intervals calculation library:
    contains methods for merging overlapping intervals and calculating their duration
    intervals are defined as a list of list:
        
        [[10,100],[110,150]]
        
        or 
        
        [
            [datetime.datetime(2010, 6, 15, 14, 21, 1, 190000), datetime.datetime(2010, 6, 15, 14, 21, 10, 190000)],
            [datetime.datetime(2010, 6, 15, 14, 21, 5, 190000), datetime.datetime(2010, 6, 15, 14, 21, 13, 190000)]
        ]
        
        
usage:
1) first step merged_intervals = merge_intervals( [[],[],[]] )
2) calculation duration: duration = calculate_duration_datetime(merged_intervals)

Example:
input =  [
            [datetime.datetime(2010, 6, 15, 14, 21, 1, 190000), datetime.datetime(2010, 6, 15, 14, 21, 10, 190000)],
            [datetime.datetime(2010, 6, 15, 14, 21, 5, 190000), datetime.datetime(2010, 6, 15, 14, 21, 13, 190000)]
        ]
merged_intervals = merge_intervals( input )
duration = calculate_duration_datetime(merged_intervals)
duration
timedelta(0, 12, 0)

timedelta_to_secods(duration)
12.0

      
'''
from datetime import timedelta



def timedelta_to_secods(d):
    """converts timedelta into seconds
    @param d: datetime.timedelta
    @return: float - seconds 
    """
    return d.days * 60 * 60 * 24 + d.seconds + d.microseconds / 1e6

def merge_intervals(intervals,debug=False):
    '''returns merged intervals
        sorts input intervals and uses merge_sorted_intervals method
        
    @param set of intervals: list of lists with intervals i.e. [(start1,end1),(start2,end2)] . Input intervals should be sorted by increasing start
    @return set of merged intervals: list of lists with intervals i.e. [(start1,end1),(start2,end2)]
    '''
    def get_start(item):
        '''
        internal method to extract start for every interval
        @param item: list with two elements
        @return: item[0] 
        '''
        return item[0]
    
    sorted_intervals=sorted(intervals,key=get_start)
    return merge_sorted_intervals(sorted_intervals,debug)



def merge_sorted_intervals(intervals,debug=False):
    '''returns merged intervals
    raises ValueError if input intervals are out of order - i.e. start1 > start2
    @param set of intervals: list of lists with intervals i.e. [(start1,end1),(start2,end2)] . Input intervals should be sorted by increasing start
    @return set of merged intervals: list of lists with intervals i.e. [(start1,end1),(start2,end2)]
    '''
    
    
    if len(intervals)<2:
        """case 0 - only one interval """
        if debug:
            print "case 0 - only one input interval - return it as is"
        return intervals
    
        
    out_intervals = []
    latest_end = None
    previous_interval=None
    
    for interval in intervals:
        """check for intervals to be in order"""
        
        if debug:
            print "previous %s , current %s" % (previous_interval,interval)
        if previous_interval is not None and interval[0]<previous_interval[0]:
            raise ValueError,"input intervals should be in ascending order of the start values"
        
        

        """define aliases for better readability"""
        i_start = interval[0]
        i_end = interval[1]
        if len(out_intervals)>0:
            last_out_interval = out_intervals[len(out_intervals)-1]
            latest_end = last_out_interval[1]  
        else:
            last_out_interval = None

        if debug:
            if last_out_interval is not None:
                print "previous interval: (%s,%s), probing interval (%s,%s)" % (last_out_interval[0],last_out_interval[1],interval[0],interval[1])
            else:
                print "first interval - probing interval (%s,%s)" % (interval[0],interval[1])



        if previous_interval is None or latest_end<i_end and latest_end<i_start:
            """case 2 - one or many non overlapping intervals"""
            if debug:
                print "\tcase 1: add new out interval (%s,%s)" % (i_start,i_end)
            out_intervals.append(interval)
            latest_end = i_end            
        elif latest_end>=i_start and latest_end<=i_end and last_out_interval is not None:
            """case 2 - next interval starts in the middle or right after last 1.end>=2.start"""
            if debug:
                print "\tcase 2: extending last out interval (%s,%s) with (%s,%s)" % (last_out_interval[0],last_out_interval[1],i_start,i_end)
            last_out_interval[1] = i_end
        else:
            if debug:
                print "do nothing"
        
        previous_interval = interval
            
            
    return out_intervals

def intersect_sorted_intervals(i1,i2,debug=False):
    out_interval = [None,None]
    if i1[0]>i2[0] and i1[1]<i2[1]:
        if debug: print "case 1"
        out_interval[0] = i1[0]
        out_interval[1] = i1[1]
    
    if i1[0]<i2[0] and i1[1]>i2[1]:
        if debug: print "case 2"
        out_interval[0] = i2[0]
        out_interval[1] = i2[1]
    if i1[0]<i2[0] and i1[1]<i2[1] and i2[0]<i1[1]:
        if debug: print "case 3"
        out_interval[0] = i2[0]
        out_interval[1] = i1[1]            

    if i1[0]>i2[0] and i1[1]>i2[1] and i1[0]<i2[1]:
        if debug: print "case 4"
        out_interval[0] = i1[0]
        out_interval[1] = i2[1]        

    if i1[0]==i2[0] and i1[1]==i2[1]:
        if debug: print "case 5"
        out_interval[0] = i1[0]
        out_interval[1] = i2[1]
    
    if out_interval[0] is None and out_interval[1] is None:
        if debug: print "case >5"
        return None        
                
    return out_interval
    
def intersect_intervals(intervals,debug=False):
    c = 0
    firsti = None
    for ivl in intervals:
        if c==0:
            firsti = ivl
        else:
            firsti = intersect_sorted_intervals(firsti,ivl)
        c+=1
        if firsti is None:
            return None        
    return firsti


def has_intersection(i1,i2,debug=False):

    if i2[0]>=i1[0] and i2[1]<=i1[1]:
        if debug: print "case 1"
        return True
    if i2[0]<i1[0] and i2[1]<i1[1] and i2[1]>i1[0]:
        if debug: print "case 2"
        return True

    if i1[0]<i2[0] and i2[0]<i1[1] and i2[1]>i1[1]:
        if debug: print "case 3"
        return True

    if i1[0]<=i2[0] and i2[0]>=i1[1]:
        if debug: print "case 4"
        #return False

    if i1[0]>i2[1] and i1[1]>i2[1]:
        if debug: print "case 5"
        #return False


    if i1[0]==i2[0] and i1[1]==i2[1]:
        if debug: print "case 6"
        return True

    if i1[0]>i2[0] and i1[1]<i2[1]:
        if debug: print "case 7"
        return True
    

    return False

def intersect_one_with_many(interval,intervals):
    res = []
    for i in intervals:
        r = intersect_sorted_intervals(interval, i)
        if r is not None:
            res.append(r)
    return res

def substract_intervals(i1s,i2s,debug=False):
    
    i1sorted = merge_intervals(i1s)
    i2sorted = merge_intervals(i2s)


    for i2 in i2sorted:
        res = []    
        for i1 in i1sorted:
            if has_intersection(i1, i2, debug):
                r = substruct_one(i1, i2, debug)
                res.extend(r)
            else:
                res.append(i1)
        i1sorted = merge_intervals(res)
        if debug: print str(i2)+" res`:"+str(res)                
            
    if debug: print "i1:"+str(i1s)
    if debug: print "i2:"+str(i2s)
    if debug: print "res:"+str(i1sorted)        
    return merge_intervals(i1sorted, debug)


def substruct_one(i1,i2,debug=False):
    re = []
    if i2[0]>i1[0] and i2[1]<i1[1]:
        if debug: print "case 1"
        re.append([i1[0],i2[0]])
        re.append([i2[1],i1[1]])
        return re
    if i2[0]<i1[0] and i2[1]<i1[1] and i2[1]>i1[0]:
        if debug: print "case 2"
        re.append([i2[1],i1[1]])
        return re

    if i2[0]<=i1[0] and i2[1]<i1[1] and i2[1]>i1[0]:
        if debug: print "case 2`"
        re.append([i2[1],i1[1]])
        return re
    
    

    if i1[0]<i2[0] and i2[0]<i1[1] and i2[1]>i1[1]:
        if debug: print "case 3"
        re.append([i1[0],i2[0]])
        return re


    if i1[0]<i2[0] and i2[0]<i1[1] and i2[1]>=i1[1]:
        if debug: print "case 3`"
        re.append([i1[0],i2[0]])
        return re
    
    

    if i1[0]<i2[0] and i2[0]>i1[1]:
        if debug: print "case 4"
        re.append(i1)
        return re

    if i1[0]>i2[1] and i1[1]>i2[1]:
        if debug: print "case 5"
        re.append(i1)
        return re    


        


    return re


def calculate_duration_in_period(intervals):
    """method to calculate duration of merged intervals
        please note if intervals are overlapping this function will return incorrect result - use merge_intervals method first
        raises ValueError if end time is earlier then start time
    @param intervals: list of lists - !nonoverlapping intervals
    @return duration
    """
    duration = 0
    for interval in intervals:
        if interval[1] < interval[0]:
            raise ValueError, "End of the interval is earlier then start: (%s,%s)" % (interval[0],interval[1])
        dur1 = interval[1] - interval[0]
        duration=duration+dur1
        
    return duration

def calculate_duration_datetime(intervals):
    """method to calculate duration of merged intervals
        please note if intervals are overlapping this function will return incorrect result - use merge_intervals method first
        raises ValueError if end time is earlier then start time
    @param intervals: list of lists - !nonoverlapping intervals (start and end are datetime)
    @return duration in timedelta
    """
    duration = timedelta(0)
    for interval in intervals:
        if interval[1] < interval[0]:
            raise ValueError, "End of the interval is earlier then start: (%s,%s)" % (interval[0],interval[1])
        dur1 = interval[1] - interval[0]
        duration=duration+dur1
        
    return duration


def iterate_over_interval(start,end):
        current_day = start
        while current_day <= end:
            yield current_day
            current_day += timedelta(days=1)
    


    
    