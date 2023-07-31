import time
from Factoring import myShor


if __name__ == '__main__':
    total_time = 0
    for i in range(1,5):
        start_time = time.perf_counter()
        extractor = myShor(8,3) 
        print(extractor.order_finding(5,87))
        finish_time = time.perf_counter()
        print(f"Program with 3 threads and 8 bits of precision finished in {finish_time-start_time} seconds")
        total_time += finish_time-start_time
    average_time = total_time/4
    print(f"Program with 3 threads and 8 bits of prsecision finished in average {average_time} seconds")
            
