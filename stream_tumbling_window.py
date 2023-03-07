import threading
import time
from queue import Queue

# Simple stream processor with a fixed size tumbling window
class Stream:
    def __init__(self, name, window_size):
        self.name = name
        self.sources = []
        self.sinks = []
        self.tasks = []
        self.queue = Queue()
        self.window_size = window_size
    
    def source(self, func):
        self.sources.append(func)
        return self
    
    def map(self, func):
        self.tasks.append(('map', func))
        return self
    
    def filter(self, func):
        self.tasks.append(('filter', func))
        return self
    
    def reduce(self, func):
        self.tasks.append(('reduce', func))
        return self
    
    def sink(self, func):
        self.sinks.append(func)
        return self
    
    def start(self):
        for source in self.sources:
            threading.Thread(target=self.run_source, args=(source,)).start()
        window_items = []
        while True:
            item = self.queue.get()
            for task in self.tasks:
                op, func = task
                if op == 'map':
                    item = func(item)
                elif op == 'filter':
                    if not func(item):
                        break
                elif op == 'reduce':
                    window_items.append(item)
                    if len(window_items) == self.window_size:
                        item = func(window_items)
                        window_items = []
                    else:
                        break
            else:
                for sink in self.sinks:
                    sink(item)
    
    def run_source(self, source):
        for item in source():
            self.queue.put(item)

# infinite time delayed sequential number stream : source
def numbers():
    index = 0
    while True:
        time.sleep(0.1)
        yield index
        index += 1

# pure function operator
def multiply_by_2(x):
    return x * 2

# filter operator
def is_even(x):
    return x % 2 == 0

# tuple reduce
def reduce_sum(items):
    return sum(items)

# std out : sink
def print_item(item):
    print(item)

stream = Stream('numbers', 3)
stream.source(numbers).map(multiply_by_2).filter(is_even).reduce(reduce_sum).sink(print_item)
stream.start()
