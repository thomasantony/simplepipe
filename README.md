# Overview

**simplepipe** is a simple composable, functional pipelining library for Python. It was built to facilitate the composition of small tasks, defined as pure functions, in order to perform a complex operation. It supports single and multi-output tasks (via generator functions). **simplepipe** also allows creation of hooks that can modify the behavior of the workflow after it has been created.

[![Build Status](https://travis-ci.org/thomasantony/simplepipe.svg?branch=master)](https://travis-ci.org/thomasantony/simplepipe)
[![PyPI version](https://badge.fury.io/py/simplepipe.svg)](https://badge.fury.io/py/simplepipe)
# Installation

The following command will install the package in your python environment from PyPI.

    pip install simplepipe

If you want install from the source code instead, run

    python setup.py install

# Examples
**simplepipe** allows you to define a list of tasks executed in a sequence that
uses data in a workspace and returns a new, updated workspace. Each task can be
python function, generator function or another Workflow object. The original workspace is unaffected. Method calls to `add_task`, `add_hook`, and `add_hook_point` can be chained.


## Full-workspace tasks and composed workflows

This is the default mode for tasks if no input or output spec is given.
These functions must return a dict with result that will be used to update the workspace.
Workflow objects can themselves be used as full-workspace tasks. These functions should return
a dict that will be used with the 'update()' method on the workspace dict.

simplepipe makes sure that the input workspace dict is protected from mutations
from these tasks and only updates the workspace with the returned value

```python
import simplepipe

def do_stuff_with_workspace(workspace):
    workspace['c'] = workspace['b']*2
    return workspace

wf = simplepipe.Workflow()
data_in = {'a': 1, 'b': 2}
wf.add_task(do_stuff_with_workspace)  # '*' is default mode
output = wf(data_in)
print(output) # Prints {'a': 1, 'b': 2, 'c': 4}

wf2 = simplepipe.Workflow()
wf2.add_task(wf)  # Add another workflow as a task
wf2.add_task(fn= lambda c: 5*c, inputs='c', outputs='d')
output = wf(data_in)
print(output) # Prints {'a': 1, 'b': 2, 'c': 4, 'd': 20}

# Protection against mutator functions
def bad_mutator_fn(workspace):
    workspace['a'] = 'just_messing_with_a'
    return {'e': 'foobar'}

wf3 = simplepipe.Workflow()
wf3.add_task(fn=bad_mutator_fn)
output = wf(data_in)
print(output) # Prints {'a': 1, 'b': 2, 'e': 'foobar'}
```

## Single output functions

```python
import simplepipe

def sum(a, b):
    return a+b

def twice(x):
    return 2*x

wf = simplepipe.Workflow()
data_in = {'a': 1, 'b': 2}
wf.add_task(sum, inputs=['a', 'b'], outputs=['c']) \
  .add_task(twice, inputs=['c'], outputs=['d'])
output = wf(data_in)
print(output) # Prints {'a': 1, 'b': 2, 'c': 3, 'd': 6}
```

## Multi-output functions

Functions returning multiple values must use the `yield` keyword to return them
separately, one at a time.

```python
import simplepipe

def sum_and_product(a, b):
    yield a+b
    yield a*b

wf = simplepipe.Workflow()
data_in = {'a': 1, 'b': 2}
wf.add_task(sum_and_product, inputs=['a', 'b'], outputs=['c', 'd'])
output = wf(data_in)
print(output) # Prints {'a': 1, 'b': 2, 'c': 3, 'd': 2}
```

## Hooks
**simplepipe** also supports hooks that allow customization of the workflow after it has been created. Hook points are defined using the `add_hook_point` method. Any number of hook functions can be bound to the hook points in the work flow. Multiple hooks added at the same hook point will be executed in the order that they were added.

*Note: Hook functions are not pure functions and are supposed to mutate the output workspace. They do not return anything.*

```python
import simplepipe

def sum(a, b):
    return a+b

def twice(x):
    return 2*x

def do_after_sum(workspace):
    workspace['c'] = workspace['c']*10

def do_after_twice(workspace):
    workspace['e'] = 31337


wf = simplepipe.Workflow()
data_in = {'a': 1, 'b': 2}
wf.add_task(sum, inputs=['a', 'b'], outputs=['c'])
wf.add_hook_point('after_sum')
wf.add_task(twice, inputs=['c'], outputs=['d'])
wf.add_hook_point('after_twice')

# Hook functions can be inserted any time before the workflow is executed
wf.add_hook('after_sum', do_after_sum)
wf.add_hook('after_twice', do_after_twice)

output = wf(data_in)
print(output)
# {'a': 1, 'b': 2, 'c': 30, 'd': 60, 'e': 31337}
```

#About the Author
[Thomas Antony's LinkedIn Profile](https://www.linkedin.com/in/thomasantony)
