import threading
import time
from queue import Queue

# Simple stream processor with a sliding window with size and a slide distance
class Stream:
    def __init__(self, name):
        self.name = name
        self.sources = []
        self.sinks = []
        self.tasks = []
        self.queue = Queue()
    
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
    
    def window(self, size, slide=1):
        self.tasks.append(('window', (size, slide)))
        return self
    
    def start(self):
        for source in self.sources:
            threading.Thread(target=self.run_source, args=(source,)).start()
        while True:
            item = self.queue.get()
            for task in self.tasks:
                op, func = task
                if op == 'map':
                    item = func(item)
                elif op == 'filter':
                    if not func(item):
                        break
                elif op == 'window':
                    size, slide = func
                    window = [item] + [self.queue.get() for i in range(size - 1)]
                    for i in range(size, slide):
                        window.pop(0)
                        window.append(self.queue.get())
                    item = window
                elif op == 'reduce':
                    item = func(item)
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

# window sum
def sum_window(window):
    return sum(window)

# std out : sink
def print_item(item):
    print(item)

stream = Stream('numbers')
stream.source(numbers).map(multiply_by_2).filter(is_even).window(5, 4).reduce(sum_window).sink(print_item)
stream.start()