"""
Created on 24 July 2016
@author: Thomas Antony
"""
import copy

class Pipeline:
    def __init__(self, task_list=[]):
        self.tasks = task_list

    def add_task(self, task, inputs=[], outputs=[]):
        self.tasks.append({'task':task, 'inputs':inputs, 'outputs':outputs})

    def run(self, data_in={}):
        data = copy.deepcopy(data_in)
        for task in self.tasks:
            inputs = [data_in[key] for key in task['inputs']]
            results = task['task'](*inputs)
            if not hasattr(results, '__iter__') or isinstance(results, str):
                results = [results]
            if len(results) != len(task['outputs']):
                raise RuntimeError('Number of return values does not match number of outputs')

            data.update(zip(task['outputs'],results))
        return data
