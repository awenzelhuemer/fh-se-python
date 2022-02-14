from functools import wraps, update_wrapper

def my_dec(func):
    
    # @wraps(func)
    def my_dec_wrapper(x):
        '''Hello this is my decorator'''
        print("Before execution.")
        print(func(x))
        print("After execution")
    return update_wrapper(my_dec_wrapper, func) 

@my_dec
def test(s):
    '''Hello this is my original function'''
    return s

test(25)
help(test)
