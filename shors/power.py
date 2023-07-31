import fastPow
import math

# If N is power of b returns b. Otherwise, returns -1
def power(N):
    # checks whether N is the ith power of a number between l and u
    def isPower(l, u, i, N):
        # ensure upper lower than lower 
        if (l > u):
            return -1
        # first check for middle of l and u
        mid = (l + u) / 2
        ans = fastPow.fastPower(mid, i, N)
        if (ans == N):
            return mid
        # if ith power of mid underestimates can increment lower bound
        elif (ans < N):
            return isPower(mid+1, u, i, N)
        # else if ith power of mid overestimates can decrement upper bound
        else:
            return isPower(l, mid-1, i, N)
    # exponent of power bounded above by s
    s = int(math.floor(math.log(N, 2))) + 1
    # base of power bounded above by r
    r = int(math.floor(math.sqrt(N))) + 1
    # test all possible exponents
    for i in range(2, s):
        ans = isPower(2, r, i, N)
        if ans != -1:
            return ans
    return -1