# simplepipe

**simplepipe** is a simple functional pipelining library for Python. I wrote this to facilitate
writing of neat code to perform complex tasks. It could be that I have reinvented
the wheel somehow, but I couldn't find any library that did what I wanted.

**simplepipe** allows you to define a list of functions executed in a sequence that
uses data in a workspace and returns an updated workspace.

Functions returning multiple values must use the `yield` keyword to return them
separately, one at a time.

Example:

    import simplepipe

    def sum(a, b):
        return a+b

    def twice(x):
        return 2*x

    queue = simplepipe.Workflow()
    data_in = {'a': 1, 'b': 2}
    queue.add_task(sum, inputs=['a', 'b'], outputs=['c'])
    queue.add_task(twice, inputs=['c'], outputs=['d'])
    output = queue(data_in)
    print(output) # Prints {'a': 1, 'b': 2, 'c': 3, 'd': 6}

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


    queue = simplepipe.Workflow()
    data_in = {'a': 1, 'b': 2}
    queue.add_task(sum, inputs=['a', 'b'], outputs=['c'])
    queue.add_hook_event('after_sum')
    queue.add_task(twice, inputs=['c'], outputs=['d'])
    queue.add_hook_event('after_twice')

    # Hook functions can be inserted any time before the workflow is executed
    queue.add_hook('after_sum', do_after_sum)
    queue.add_hook('after_twice', do_after_twice)

    output = queue(data_in)
    print(output)
    # {'a': 1, 'b': 2, 'c': 30, 'd': 60, 'e': 31337}

*Note: Hook functions are not pure functions and are supposed to mutate the workspace.*
