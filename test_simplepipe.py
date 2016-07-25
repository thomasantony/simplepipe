import pytest
import simplepipe

@pytest.fixture
def sum_func():
    def sum(a, b):
        return a+b
    return sum

def test_run_task():
    """Test the run_task() function"""
    def return_one():
        return 1

    # Test run task
    task_one = {'task':return_one, 'inputs':[], 'outputs':['a']}
    output = simplepipe.run_task(task_one, {})
    assert(output == {'a': 1})

def test_workflow(sum_func):
    """Test the Workflow class"""
    p = simplepipe.Workflow()
    data_in = {'a':1, 'b':2}
    data_out = {'a':1, 'b':2, 'c':3}
    p.add_task(sum_func, inputs=['a','b'], outputs=['c'])
    output = p(data_in)
    assert(output == data_out)

def test_hooks(sum_func):
    """Test hooks in workflow"""
    def after_sum_1(data):
        data['c'] = 10

    def after_sum_2(data):
        data['e'] = 100

    p = simplepipe.Workflow()
    data_in = {'a':1, 'b':2}
    data_out = {'a':1, 'b':2, 'c':3}
    p.add_task(sum_func, inputs=['a','b'], outputs=['c'])
    p.add_hook_event('after_sum')
    p.add_task(lambda c: 2*c, inputs=['c'], outputs=['d'])

    p.add_hook('after_sum', after_sum_1)
    p.add_hook('after_sum', after_sum_2)
    output = p(data_in)

    assert(output == {'a': 1, 'b': 2, 'c': 10, 'd': 20, 'e': 100})
