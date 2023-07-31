import qsharp

import miller_rabin
import fractions
import power
import fastPow
import fraction
import gcd

import multiprocessing
import time
import random

from shors import PhaseEstimation

class myShor():
    def __init__(self, precision, thread_num):
        self.Precision = precision
        self.Thread_Num = thread_num

    # Order-finding algorithm
    def order_finding(self, x, n):

        def phase_estimation(x, n):
            # simulate quantum phase-estimation 
            tmp = int(PhaseEstimation.simulate(x=x, N=n, precision=self.Precision))
            # Convert integer into float corresponding to approximation of s/r
            theta = float(tmp) / (2**self.Precision)
            return theta

        # repeat order finding 
        for _ in range(2):
            theta = phase_estimation(x, n)
            if theta == 0:
                print("========\nOrder Finding for: x={}, N={}\nGet theta: {}\nNo r estimated\n".format(
                    x, n, theta))
                continue

            r = fraction.denominator(theta, n)
            print("========\nOrder Finding for: x={}, N={}\nGet theta: {}\nEstimate r: {}\n".format(
                x, n, theta, r))
            for i in r:
                m = fastPow.fastPower(x, i, n)
                if m == 1:
                    return i
        return -1
    
    def shor(self, n):
        # check whether n even
        if (n % 2 == 0):
            return (2, n // 2)
        else:
        # check whether n is prime
            if miller_rabin.miller_rabin(n):
                return (1, n)
            else:
                # check whether n can be written as simple power and if so return base 
                tmp = power.power(n)
                if tmp != -1:
                    return (tmp, n // tmp)
                while True:
                    # Three random numbers between 3 and n-1 to run multiple threads of order finding algorithm on 
                    xlist = random.sample(range(3, n - 1), self.Thread_Num)
                    # check whether any of the xs already divide n with euclid's algorithm
                    for x in xlist:
                        g = gcd.gcd(x,n)
                        if (g != 1):
                            return (g, n // g)

                    # repeat order_finding until non-trivial factor of n is obtained
                    print("======== Order Finding Started ========")
                    # set up multithread process for computing orders of each x in xlist
                    pool = multiprocessing.Pool(self.Thread_Num)
                    start_time = time.perf_counter()
                    processes = [pool.apply_async(self.order_finding, args=(x,n)) for x in xlist]
                    results = [p.get() for p in processes]
                    for r, x in zip(results, xlist):
                        # check that correct order obtained
                        if r == -1:
                            continue
                        # check that order even
                        if (r % 2 == 0):
                            s = fastPow.fastPower(x, r // 2, n)
                            # check that x^{r/2} is non-trivial solution to a^2 == 1 mod N
                            if (s != 1 and s != n-1):
                                g1 = gcd.gcd(s+1, n)
                                g2 = gcd.gcd(s-1, n)
                                # return the respective factor of n
                                if (g1 != 1):
                                    return (g1, n // g1)
                                elif (g2 != 1):
                                    return (g2, n // g2)