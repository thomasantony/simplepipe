"""
Created on 24 July 2016
@author: Thomas Antony
"""
import copy
import functools

class Workflow(object):
    def __init__(self, task_list=[]):
        self.tasks = task_list
        self.hooks = {}

    def add_task(self, task, inputs=[], outputs=[]):
        self.tasks.append({'task':task, 'inputs':inputs, 'outputs':outputs})
        return self

    def add_hook_event(self, name):
        """
        Creates a point in the workflow where hook functions can be added
        """
        self.tasks.append({'task': functools.partial(self.run_hook, name),
                            'inputs': '*',
                            'outputs': '*'})
        return self

    def add_hook(self, name, function):
        """
        Adds a function to be called for hook of a given name

        The function gets entire workspace as input and does not return anything
        """
        if not callable(function):
            return ValueError('Hook function should be callable')
        if name not in self.hooks:
            self.hooks[name] = []
        self.hooks[name].append(function)

    def run_hook(self, name, workspace):
        """
        Runs all hooks added under the give name
        """
        if name not in self.hooks:
            raise KeyError('Hook '+name+' not found')

        data = copy.deepcopy(workspace)
        for hook_fn in self.hooks[name]:
            # Hook functions may mutate the data and returns nothing
            hook_fn(data)
        return data

    def __call__(self, workspace={}):
        data = copy.deepcopy(workspace)
        for task in self.tasks:
            # Input is full workspace for input type '*'
            if task['inputs'] == '*' or task['inputs']==['*']:
                inputs = [data]
            else:
                inputs = [data[key] for key in task['inputs']]

            results = task['task'](*inputs)

            if len(task['outputs']) == 1:
                results = [results]

            if len(results) != len(task['outputs']):
                raise RuntimeError('Number of return values does not match number of outputs')

            if task['outputs'] == '*' or task['outputs'] == ['*']:
                try:
                    data.update(results[0])
                except TypeError as e:
                    raise TypeError('Result should be a dict for output type *')
            else:
                data.update(zip(task['outputs'],results))
        return data

    def __repr__(self):
        return '<%s with %d tasks>' % (self.__class__.__name__, len(self.tasks))
