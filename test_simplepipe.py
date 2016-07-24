import simplepipe
def test_simplepipe():
    def return_one():
        return 1

    p = simplepipe.Pipeline()
    p.add_task(return_one, inputs=[], outputs=['a'])
    output = p.run()
    assert(output == {'a': 1})

    data_in = {'a':1, 'b':2}
    data_out = {'a':1, 'b':2, 'c':3}
    def sum(a, b):
        return a+b

    p = simplepipe.Pipeline()
    p.add_task(sum, inputs=['a','b'], outputs=['c'])
    output = p.run(data_in)
    assert(output == data_out)
