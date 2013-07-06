__author__ = 'vvlad'
class IntervalTree:
    def __init__(self, h, left, right):
        self.h = h
        self.left = left
        self.right = right

def merge(A, B, op, l=-float("inf"), u=float("inf")):
    if l > u:
        return None
    if not isinstance(A, IntervalTree):
        if isinstance(B, IntervalTree):
            opT = op
            A, B, op = B, A, (lambda x, y : opT(y,x))
        else:
            return op(A, B)
    left = merge(A.left, B, op, l, min(A.h, u))
    right = merge(A.right, B, op, max(A.h, l), u)
    if left is None:
        return right
    elif right is None or left == right:
        return left
    return IntervalTree(A.h, left, right)

def to_range_list(T, l=-float("inf"), u=float("inf")):
    if isinstance(T, IntervalTree):
        return to_range_list(T.left, l, T.h) + to_range_list(T.right, T.h, u)
    return [(l, u-1)] if T else []

def range_list_to_tree(L):
    return reduce(lambda x, y : merge(x, y, lambda a, b: a or b),
        [ IntervalTree(R[0], False, IntervalTree(R[1]+1, True, False)) for R in L ])


if __name__=='__main__':
    r1 = range_list_to_tree([ (1, 1000), (1100, 1200) ])
    r2 = range_list_to_tree([ (30, 50), (60, 200), (1150, 1300) ])


    r1_ = range_list_to_tree([ (1, 1000) ])
    r2_ = range_list_to_tree([ (100, 1000), (1,1100) ])

    print "r1: %s" % to_range_list(r1)
    print "r2: %s" % to_range_list(r2)

    diff = merge(r1, r2, lambda a, b : a and not b)
    print "diff: %s" % to_range_list(diff)


    #Intersection
    intersection_result = merge(r1, r2, lambda a, b : a and b)
    print "Intersection: %s" % to_range_list(intersection_result)

    #Union
    union_result = merge(r1, r2, lambda a, b : a or b)
    print "Union: %s" % to_range_list(union_result)

    #Xor
    xor_result = merge(r1, r2, lambda a, b : a != b)
    print "Xor: %s" % to_range_list(xor_result)