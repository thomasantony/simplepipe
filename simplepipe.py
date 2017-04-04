"""
Created on 24 July 2016
@author: Thomas Antony
"""
import copy
import inspect
import functools
import collections

__version__ = '0.0.4'

def validate_task(original_task):
    """
    Validates task and adds default values for missing options using the
    following steps.

    1. If there is no input list specified or if it is None, the input spec is
       assumed to be ['*'].

    2. If there are not outputs specified, or if the output spec is None or an
       empty list, the output spec is assumed to be ['*'].

    3. If the input or output spec is not iterable, they are converted into
       single element tuples. If they are any iterable, they are converted into
       tuples.

    4. The task['fn'] option must be callable.

    5. If number of outputs is more than one, task['fn'] must be a generator
       function.

    6. Generator functions are not supported for output spec of '*'.

    Returns new task with updated options
    """
    task = original_task._asdict()
    # Default values for inputs and outputs
    if 'inputs' not in task or task['inputs'] is None:
        task['inputs'] = ['*']

    # Outputs list cannot be empty
    if ('outputs' not in task or
       task['outputs'] is None or
       len(task['outputs']) == 0):
        task['outputs'] = ['*']

    # Convert to tuples (even for single values)
    if not hasattr(task['inputs'], '__iter__'):
        task['inputs'] = (task['inputs'],)
    else:
        task['inputs'] = tuple(task['inputs'])

    if not hasattr(task['outputs'], '__iter__'):
        task['outputs'] = (task['outputs'],)
    else:
        task['outputs'] = tuple(task['outputs'])

    if not callable(task['fn']):
        raise TypeError('Task function must be a callable object')

    if (len(task['outputs']) > 1 and
       not inspect.isgeneratorfunction(task['fn'])):
        raise TypeError('Multiple outputs are only supported with \
                        generator functions')

    if inspect.isgeneratorfunction(task['fn']):
        if task['outputs'][0] == '*':
            raise TypeError('Generator functions cannot be used for tasks with \
                             output specification "*"')
    return Task(**task)


def input_parser(key, data):
    """Used to pass in full workspace if an input is defined as '*'"""
    if key == '*':
        return copy.copy(data)
    else:
        return data[key]

def run_task(task, workspace):
    """
    Runs the task and updates the workspace with results.

    task : dict describing task

    Examples:
    {'task': task_func, 'inputs': ['a', 'b'], 'outputs': 'c'}
    {'task': task_func, 'inputs': '*', 'outputs': '*'}
    {'task': task_func, 'inputs': ['*','a'], 'outputs': 'b'}

    Returns a new workspace with results
    """
    data = copy.copy(workspace)

    task = validate_task(task)

    # Prepare input to task
    inputs = [input_parser(key, data) for key in task.inputs]

    if inspect.isgeneratorfunction(task.fn):
        # Multiple output task
        # Assuming number of outputs are equal to number of return values
        data.update(zip(task.outputs, task.fn(*inputs)))
    else:
        # Single output task
        results = task.fn(*inputs)
        if task.outputs[0] != '*':
            results = {task.outputs[0]: results}
        elif not isinstance(results, dict):
            raise TypeError('Result should be a dict for output type *')
        data.update(results)

    return data

Task = collections.namedtuple('Task', ['fn', 'inputs', 'outputs'])

class Workflow(object):
    def __init__(self, task_list=None, description='simplepipe Workflow'):
        if task_list is None:
            self.tasks = []
        else:
            self.tasks = task_list
        self.hooks = {}
        self.__doc__ = description

    def add_task(self, fn, inputs=None, outputs=None):
        """
        Adds a task to the workflow.

        Returns self to facilitate chaining method calls
        """
        # self.tasks.append({'task': task, 'inputs': inputs, 'outputs': outputs})
        self.tasks.append(Task(fn, inputs, outputs))
        return self

    def add_hook_point(self, name):
        """
        Creates a point in the workflow where hook functions can be added.

        Implemented as a special type of task that takes full workspace as its
        input and returns a modified workspace
        """

        self.tasks.append(Task(fn=functools.partial(self.run_hook, name),
                           inputs='*',
                           outputs='*'))
        return self

    def add_hook(self, name, function):
        """
        Adds a function to be called for hook of a given name.

        The function gets entire workspace as input and
        does not return anything.

        Example:
        def hook_fcn(workspace):
            pass
        """
        if not callable(function):
            return ValueError('Hook function should be callable')
        if name not in self.hooks:
            self.hooks[name] = []
        self.hooks[name].append(function)
        return self

    def run_hook(self, name, workspace):
        """Runs all hooks added under the give name."""
        if name not in self.hooks:
            raise KeyError('Hook '+name+' not found')

        data = copy.copy(workspace)
        for hook_listener in self.hooks[name]:
            # Hook functions may mutate the data and returns nothing
            hook_listener(data)
        return data

    def __call__(self, workspace={}):
        """
        Executes all the queued tasks in order and returns
        new workspace with results
        """
        result = workspace
        for task in self.tasks:
            result = run_task(task, result)
        return result

    def __repr__(self):
        return '<%s with %d tasks>' \
                % (self.__class__.__name__, len(self.tasks))
