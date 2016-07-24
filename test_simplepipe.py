import simplepipe
def sum(a, b):
    return a+b



def test_simplepipe():
    def return_one():
        return 1

    p = simplepipe.Workflow()
    p.add_task(return_one, inputs=[], outputs=['a'])
    output = p()
    assert(output == {'a': 1})


    p = simplepipe.Workflow()
    data_in = {'a':1, 'b':2}
    data_out = {'a':1, 'b':2, 'c':3}
    p.add_task(sum, inputs=['a','b'], outputs=['c'])
    output = p(data_in)
    assert(output == data_out)

def test_hooks():
    p = simplepipe.Workflow()
    data_in = {'a':1, 'b':2}
    data_out = {'a':1, 'b':2, 'c':3}
    p.add_task(sum, inputs=['a','b'], outputs=['c'])
    p.add_hook_event('after_sum')

    def after_sum_1(data):
        data['c'] = 10

    p.add_task(lambda x: 2*x, inputs=['c'], outputs=['d'])

    p.add_hook('after_sum', after_sum_1)
    output = p(data_in)
    assert(output == {'a': 1, 'b': 2, 'c': 10, 'd': 20})
