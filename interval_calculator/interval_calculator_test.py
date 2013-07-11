
import unittest
from intervals_calculator import merge_intervals,\
    merge_sorted_intervals, calculate_duration_in_period, calculate_duration_datetime,\
    timedelta_to_secods, intersect_sorted_intervals, intersect_intervals,\
    intersect_one_with_many, substruct_one, substract_intervals,\
    has_intersection, substract_intervals_itree
from datetime import datetime, timedelta

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass
#        self.seq = range(10)
#        self.intervals = [(0,100),(0,50),(50,150)]


    def test_calculate_1(self):
        """single interval case"""
        input = [[0,100]]
        result = merge_intervals(input,False)
        self.assertEqual(input,result)

    def test_calculate_2(self):
        """two intervals - non overlapping""" 
        input = [[0,100],[200,300]]
        result = merge_intervals(input,False)
        self.assertEqual(input,result)

    def test_calculate_2_1(self):
        """many intervals - non overlapping""" 
        input = [[0,100],[200,300],[400,500],[600,700]]
        result = merge_intervals(input,False)
        self.assertEqual(input,result)


    def test_calculate_3(self):
        """two intervals - second right after first""" 
        input = [[0,100],[100,200]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,200]])


    def test_calculate_3_1(self):
        """many intervals - second right after first""" 
        input = [[0,100],[100,200],[200,300],[300,400],[400,500],[500,600]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,600]])

    def test_calculate_4(self):
        """two intervals - overlapping""" 
        input = [[0,100],[50,150]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,150]])


    def test_calculate_4_1(self):
        """two intervals - overlapping - one includes 100% of another""" 
        input = [[0,100],[50,70]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,100]])

    def test_calculate_4_2(self):
        """two intervals - overlapping - second includes 100% of another""" 
        input = [[0,70],[0,100]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,100]])
        

    def test_calculate_4_3(self):
        """many overlapping intervals""" 
        input = [[0,50],[45,80],[70,120],[100,150]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,150]])

    def test_calculate_4_4(self):
        """many intervals - some overlapping, some - not""" 
        input = [ [0,50],[45,80],[70,90], [100,150],[120,180], [190,210],[200,250]]
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,90],[100,180],[190,250]])


    """invalid cases"""
    
    def test_calculate_5(self):
        """intervals are out of order"""
        input = [ [100,150],[0,50]]
        #result = merge_intervals(input,False)        
        self.assertRaises(ValueError,merge_sorted_intervals,input,False)
        #self.assertEqual(result,[[0,90],[100,180],[190,250]])
        result = merge_intervals(input,False)
        self.assertEqual(result,[[0,50], [100,150]])
                
    
    
    """ calculate duration """
    
    def test_duration(self):
        """ calculate duration """
        input = [ [100,150],[0,50], [250,350], [200,300]]
        merged_sorted_interval = merge_intervals(input, False)
        #print input
        #print merged_sorted_interval
        duration = calculate_duration_in_period(merged_sorted_interval)
        #print duration
        self.assertEqual(duration,250)
        
        input = [ [10,40],[0,50], [500,600], [700,800]]
        merged_sorted_interval = merge_intervals(input, False)
        #print input
        #print merged_sorted_interval
        duration = calculate_duration_in_period(merged_sorted_interval)
        #print duration
        self.assertEqual(duration,250)
        
        
    def test_with_dates_1(self):
        """datetime support basic"""
        start = datetime(2010, 6, 15, 14, 21, 10, 190000)
        end = datetime(2010, 6, 15, 14, 21, 11, 190000)
        input = [[start,end]]
        
        result = merge_intervals(input, False)
        #print result
        self.assertEqual(input,result)
        

        
        
    def test_with_dates_2(self):
        """datetime support - many non overlapping intervals"""      
        start = datetime(2010, 6, 15, 14, 21, 10, 190000)
        end = datetime(2010, 6, 15, 14, 21, 11, 190000)
        input = [[start,end]]        
        start1 = datetime(2010, 6, 15, 14, 21, 12, 190000)
        end1 = datetime(2010, 6, 15, 14, 21, 13, 190000)
        
        input.append([start1,end1])        
        
        #print input
        result = merge_intervals(input, False)
        #print result
        self.assertEqual(input,result)
        

    def test_with_dates_3(self):
        """datetime support - overlapping intervals"""      
        start = datetime(2010, 6, 15, 14, 21, 01, 190000)
        end = datetime(2010, 6, 15, 14, 21, 10, 190000)
        input = [[start,end]]        
        start1 = datetime(2010, 6, 15, 14, 21, 5, 190000)
        end1 = datetime(2010, 6, 15, 14, 21, 13, 190000)
        
        expected_result = [[start,end1]]
        
        input.append([start1,end1])        
        
        #print input
        result = merge_intervals(input, False)
        #print result
        self.assertEqual(expected_result,result)
        
    def test_calculation_with_dates(self):        
        """datetime support - overlapping intervals"""      
        start = datetime(2010, 6, 15, 14, 21, 01, 190000)
        end = datetime(2010, 6, 15, 14, 21, 10, 190000)
        input = [[start,end]]        
        start1 = datetime(2010, 6, 15, 14, 21, 5, 190000)
        end1 = datetime(2010, 6, 15, 14, 21, 13, 190000)
        
        expected_result = [[start,end1]]
        
        input.append([start1,end1])
        
                
        
        #print input
        result = merge_intervals(input, False)
        #print result
        
        duration = calculate_duration_datetime(result)
        #print "datetime duration"
        #print duration
        
        expected_duration = timedelta(0, 12, 0)
        self.assertEqual(expected_duration,duration)
        
        #print timedelta_to_secods(expected_duration)
        
        self.assertEqual(12,timedelta_to_secods(expected_duration))
    def test_intersect_two(self):
        #case 1
        #i2 include i1
        i1 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]   
        
        i2 = [
              datetime(2011, 8, 15, 14, 21, 01, 190000),
              datetime(2011, 11, 1, 14, 21, 10, 190000)
              ]
        
        print "testing case 1"
        res = intersect_sorted_intervals(i1,i2,True)
        self.assertEqual(res,i1)

        #case 2
        #i1 include i2
        print "testing case 2"
        res = intersect_sorted_intervals(i2,i1,True)
        self.assertEqual(res,i1)
        
        #case 3
        i1 = [
              datetime(2011, 8, 15, 14, 21, 01, 190000),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]   
        
        i2 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 11, 1, 14, 21, 10, 190000)
              ]
        i3 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]
        print "testing case 3"
        res = intersect_sorted_intervals(i1,i2,True)
        self.assertEqual(res,i3)
        
        #case 4
        
        i1 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 11, 1, 14, 21, 10, 190000)
              ]

        i2 = [
              datetime(2011, 8, 15, 14, 21, 01, 190000),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]   
        
        i3 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]
        print "testing case 4"        
        res = intersect_sorted_intervals(i1,i2,True)
        self.assertEqual(res,i3)
        
        #case 5
        i1 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]
        i2 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]
        i3 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]
        print "testing case 5"        
        res = intersect_sorted_intervals(i1,i2,True)
        self.assertEqual(res,i3)

        #case 6
        i1 = [
              datetime(2011, 10, 1, 0, 0, 0, 0),
              datetime(2011, 10, 31, 23, 59, 59, 0)
              ]

        i2 = [
              datetime(2011, 12, 1, 0, 0, 0, 0),
              datetime(2011, 12, 31, 23, 59, 59, 0)
              ]

        
        print "testing case 6"        
        res = intersect_sorted_intervals(i1,i2,True)
        self.assertEqual(res,None)


        print "testing case 7"        
        res = intersect_sorted_intervals(i2,i1,True)
        self.assertEqual(res,None)
        
    def test_intersect_many(self):
        ivls = [[1,2],[3,4],[5,6]]
        r = intersect_intervals(ivls)
        print r
        self.assertEqual(r,None)

        ivls = [[1,10],[2,8],[3,7]]
        r = intersect_intervals(ivls)
        print r
        self.assertEqual(r,[3,7])

    def test_intersect_one_with_many(self):
        intervals = [[1,4],[6,8],[11,20]]
        cutoff_interval = [3,15]
        r = intersect_one_with_many(cutoff_interval,intervals)
        print r
        res = [[3,4],[6,8],[11,15]]
        self.assertEqual(res,r)
        
    def test_substract(self):
        
        print "case1"
        i1 = [1,10]
        i2 = [3,4]
        er = [[1,3],[4,10]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)


        print "case2"
        i1 = [5,10]
        i2 = [3,6]
        er = [[6,10]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)

        print "case3"
        i1 = [5,10]
        i2 = [7,13]
        er = [[5,7]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)



        print "case4"
        i1 = [5,10]
        i2 = [15,20]
        er = [[5,10]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)


        print "case5"
        i1 = [15,20]
        i2 = [5,10]
        er = [[15,20]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)


        print "case6"
        i1 = [15,20]
        i2 = [15,20]
        er = []
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)

        print "case7"
        i1 = [10,15]
        i2 = [5,20]
        er = []
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)


        print "case 8"
        i1 = [55,65]
        i2 = [60,65]
        er = [[55,60]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)

        print "case 9"
        i1 = [55,65]
        i2 = [55,60]
        er = [[60,65]]
        r = substruct_one(i1,i2,True)
        self.assertEqual(r,er)


        
    def test_substruct_intervals(self):
#        i1 = [[1,5],[8,19]]
#        i2 = [[2,3],[6,9],[11,13]]
        print "t1 "
        i1 = [[1,5],[8,19]]
        i2 = [[2,3]]        
        r = substract_intervals(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,19]]
        self.assertEqual(r,exp_res)


        print "t2 "
        i1 = [[1,5],[8,19],[21,25]]
        i2 = [[2,3]]        
        r = substract_intervals(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,19],[21,25]]
        self.assertEqual(r,exp_res)


        print "t3 "        
        i1 = [[1,5],[8,19]]
        i2 = [[2,3],[10,11]]        
        r = substract_intervals(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,10],[11,19]]
        #print exp_res
        self.assertEqual(r,exp_res)        
        
        


        print "t4 "        
        i1 = [[15,35],[40,65],[70,75],[90,100]]
        i2 = [[5,10],[20,25],[30,45],[50,55],[60,65],[80,85],[90,100]]        
        r = substract_intervals(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [ [15,20],[25,30],[45,50],[55,60],[70,75] ]
        #print exp_res
        self.assertEqual(r,exp_res)        

    def test_substruct_intervals_fast(self):
#        i1 = [[1,5],[8,19]]
#        i2 = [[2,3],[6,9],[11,13]]
        print "t1 "
        i1 = [[1,5],[8,19]]
        i2 = [[2,3]]
        r = substract_intervals_itree(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,19]]
        self.assertEqual(r,exp_res)


        print "t2 "
        i1 = [[1,5],[8,19],[21,25]]
        i2 = [[2,3]]
        r = substract_intervals_itree(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,19],[21,25]]
        self.assertEqual(r,exp_res)


        print "t3 "
        i1 = [[1,5],[8,19]]
        i2 = [[2,3],[10,11]]
        r = substract_intervals_itree(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [[1,2],[3,5],[8,10],[11,19]]
        #print exp_res
        self.assertEqual(r,exp_res)




        print "t4 "
        i1 = [[15,35],[40,65],[70,75],[90,100]]
        i2 = [[5,10],[20,25],[30,45],[50,55],[60,65],[80,85],[90,100]]
        r = substract_intervals_itree(i1,i2)
        #print r
        #exp_res = [[1,2],[4,5],[9,10],[13,19]]
        exp_res = [ [15,20],[25,30],[45,50],[55,60],[70,75] ]
        #print exp_res
        self.assertEqual(r,exp_res)



    def test_has_intersection(self):
        
        i1 = [55,65]
        i2 = [60,65]
        r = has_intersection(i1,i2)
        self.assertEqual(r,True)

        i1 = [55,65]
        i2 = [65,60]
        r = has_intersection(i1,i2)
        self.assertEqual(r,True)



if __name__ == '__main__':
    unittest.main()
