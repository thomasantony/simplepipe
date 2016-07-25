# Overview

**simplepipe** is a simple functional pipelining library for Python. It was facilitate
the composition of small tasks, defined as pure functions to accomplish a complex objective.

# Installation

The following command will install the package in your python environment.

    python setup.py install

Submission to PyPI is in progress.

# Examples
**simplepipe** allows you to define a list of functions executed in a sequence that
uses data in a workspace and returns a new, updated workspace. The original workspace is unaffected.

## Single output functions

    import simplepipe

    def sum(a, b):
        return a+b

    def twice(x):
        return 2*x

    wf = simplepipe.Workflow()
    data_in = {'a': 1, 'b': 2}
    wf.add_task(sum, inputs=['a', 'b'], outputs=['c'])
    wf.add_task(twice, inputs=['c'], outputs=['d'])
    output = wf(data_in)
    print(output) # Prints {'a': 1, 'b': 2, 'c': 3, 'd': 6}

## Multi-output functions

Functions returning multiple values must use the `yield` keyword to return them
separately, one at a time.


    import simplepipe

    def sum_and_product(a, b):
        yield a+b
        yield a*b

    wf = simplepipe.Workflow()
    data_in = {'a': 1, 'b': 2}
    wf.add_task(sum_and_product, inputs=['a', 'b'], outputs=['c','d'])
    output = wf(data_in)
    print(output) # Prints {'a': 1, 'b': 2, 'c': 3, 'd': 2}

## Hooks
**simplepipe** also supports hooks that allow customization of the workflow.
Multiple hooks can be added under the same name and the hooked functions will
executed in the order that they were added wherver the hook event was specified.


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
    wf.add_hook_event('after_sum')
    wf.add_task(twice, inputs=['c'], outputs=['d'])
    wf.add_hook_event('after_twice')

    # Hook functions can be inserted any time before the workflow is executed
    wf.add_hook('after_sum', do_after_sum)
    wf.add_hook('after_twice', do_after_twice)

    output = wf(data_in)
    print(output)
    # {'a': 1, 'b': 2, 'c': 30, 'd': 60, 'e': 31337}

*Note: Hook functions are not pure functions and are supposed to mutate the output workspace. They do not return anything.*
