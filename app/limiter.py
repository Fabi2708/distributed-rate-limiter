import time

class TokenBucket:
    
    def __init__ (self,capacity,timestamp):
        self.capacity = capacity
        self.refill_rate = 10/60
        self.token_count = capacity
        self.timestamp = timestamp

    def refill(self):
        current_time = time.perf_counter()
        elapsed_time = current_time - self.timestamp
        tokens_to_add = elapsed_time * self.refill_rate
        self.token_count = min(self.token_count + tokens_to_add,self.capacity)
        self.timestamp = current_time

    def consume(self):
        self.refill()
        if(self.token_count >= 1):
            self.token_count -= 1
            return True
        else:
            return False
        

    