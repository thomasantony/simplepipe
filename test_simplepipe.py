import pytest
import simplepipe


@pytest.fixture
def sum_fn():
    return lambda a, b: a+b

@pytest.fixture
def doubler_fn():
    return lambda a: 2*a

@pytest.fixture
def return_one_fn():
    def return_one():
        return 1

    return return_one


@pytest.fixture
def two_output_fn():
    # Test function with multiple outputs
    def two_outputs():
        yield 1
        yield 2

    return two_outputs

@pytest.fixture
def mixed_input_fn():
    def mixed_inputs(workspace, a):
        return workspace['x'] * a
    return mixed_inputs


def test_validate_task(return_one_fn, two_output_fn):
    """Test the validate_task() function"""
    # When task is not callable
    with pytest.raises(TypeError):
        simplepipe.validate_task(simplepipe.Task(fn = 'foobar',
                                  inputs = [],
                                  outputs = ['a']))

    # Multiple outputs require generator function
    with pytest.raises(TypeError):
        simplepipe.validate_task(simplepipe.Task(fn = return_one_fn,
                                  inputs = [],
                                  outputs = ['a', 'b']))

    # '*' output does not work with generator functions
    with pytest.raises(TypeError):
        simplepipe.validate_task(simplepipe.Task(fn = two_output_fn,
                                  inputs = [],
                                  outputs = ['*']), {})


def test_run_task(return_one_fn, two_output_fn, mixed_input_fn, doubler_fn):
    """Test the run_task() function"""

    # Test run task with one output
    output = simplepipe.run_task(simplepipe.Task(fn=return_one_fn,
                                  inputs =[],
                                  outputs =['a']), {})
    assert output == {'a': 1}

    # Fails when task with '*' output doesn't return dict
    with pytest.raises(TypeError):
        simplepipe.run_task(simplepipe.Task(fn = return_one_fn,
                             inputs = [],
                             outputs = ['*']), {})
    # Task with two outputs
    task_five = simplepipe.Task(fn = two_output_fn,
                 inputs = [],
                 outputs = ['a', 'b'])
    output = simplepipe.run_task(task_five, {})
    assert output == {'a': 1, 'b': 2}

    # Task with mixed inputs (workspace + normal)
    task_six = simplepipe.Task(fn = mixed_input_fn,
                                inputs=['*', 'a'],
                                outputs='b')
    output = simplepipe.run_task(task_six, {'x': 2, 'a': 3})
    assert output == {'x': 2, 'a': 3, 'b': 6}

    task_seven = simplepipe.Task(fn=doubler_fn,
                                inputs='first',
                                outputs='second')
    output = simplepipe.run_task(task_seven, {'first':1})
    assert output == {'first':1, 'second':2}


def test_workflow(sum_fn, return_one_fn, two_output_fn):
    """Test the Workflow class"""
    p = simplepipe.Workflow()
    data_in = {'first': 1, 'second': 2}
    data_out = {'first': 1, 'second': 2, 'c': 3}
    p.add_task(sum_fn, inputs =['first', 'second'], outputs =['c'])
    assert(p(data_in) == data_out)

    # Test composition of workflows
    p2 = simplepipe.Workflow()
    p2.add_task(p)
    p2.add_task(return_one_fn, inputs =[], outputs =['d'])
    data_out2 = {'first': 1, 'second': 2, 'c': 3, 'd': 1}
    assert(p2(data_in) == data_out2)

    # Test protection against mutation
    def bad_mutator_fn(workspace):
        workspace['a'] = 'just_messing_with_a'
        return {'e': 'foobar'}

    wf3 = simplepipe.Workflow()
    wf3.add_task(fn=bad_mutator_fn)
    assert wf3({'a': 1, 'b': 2}) == {'a': 1, 'b': 2, 'e': 'foobar'}


def test_hooks(sum_fn):
    """Test hooks in workflow"""
    def after_sum_1(data):
        data['c'] = 10

    def after_sum_2(data):
        data['e'] = 100

    p = simplepipe.Workflow()
    data_in = {'a': 1, 'b': 2}
    data_out = {'a': 1, 'b': 2, 'c': 3}
    p.add_task(sum_fn, inputs =['a', 'b'], outputs =['c']) \
     .add_hook_point('after_sum') \
     .add_task(lambda c: 2*c, inputs =['c'], outputs =['d'])

    p.add_hook('after_sum', after_sum_1)
    p.add_hook('after_sum', after_sum_2)
    output = p(data_in)

    assert(output == {'a': 1, 'b': 2, 'c': 10, 'd': 20, 'e': 100})
