# Introduction to Simple Stream Processor in python

This is a simple project to illustrate the high level concepts behind modern stream processors like apache flink in an easy and digestible way.

Key concepts covered here are functions operators, data flow graphs, operator chaining and windowing.

The project is simple enough and self contained in single files to explore and study and add more sophisticated components for learning and experimentation.

## Execution

```python
python stream.py 
```

The simplest design just showing function operators stitched together, input is still an infinite sequential numbers stream.

```python
python stream_tumbling_window.py 
```

The prior code extended to support basic tumbling window.

```python
python stream_sliding_window.py
```

The base implementation with a sliding window with size and a slide distance.

