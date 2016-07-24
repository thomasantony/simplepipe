"""
Created on 24 July 2016
@author: Thomas Antony
"""
import copy
import functools

class Workflow:
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
        self.tasks.append({'hook': name})
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

    def run_hook(self, name, data_in):
        if name not in self.hooks:
            raise KeyError('Hook '+name+' not found')

        data = copy.deepcopy(data_in)
        for hook_fn in self.hooks[name]:
            # Hook functions may mutate the data and returns nothing
            hook_fn(data)
        return data

    def __call__(self, data_in={}):
        data = copy.deepcopy(data_in)
        for task in self.tasks:
            if 'hook' in task:
                result = self.run_hook(task['hook'], data)
                data.update(result)
            else:
                inputs = [data[key] for key in task['inputs']]
                results = task['task'](*inputs)
                if not hasattr(results, '__iter__') or isinstance(results, str):
                    results = [results]
                if len(results) != len(task['outputs']):
                    raise RuntimeError('Number of return values does not match number of outputs')

                data.update(zip(task['outputs'],results))
        return data

    def __len__(self):
        """
        Returns number of tasks in workflow
        """
        return len(self.tasks)
