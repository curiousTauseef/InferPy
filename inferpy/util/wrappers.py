from functools import wraps
import inferpy as inf
import numpy as np

def tf_run_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if "tf_run" in kwargs:
            tf_run = kwargs.pop("tf_run")
        else:
            tf_run = inf.util.Runtime.tf_run_default


        if tf_run:
            output_tf = f(*args, **kwargs)
            if type(output_tf).__module__ == np.__name__:
                output_eval = np.array([])
                for t in output_tf:
                    output_eval.append(inf.util.Runtime.tf_sess.run(t))
            elif type(output_tf).__name__ == dict.__name__:
                output_eval = {}
                for k, v in output_tf.iteritems():
                    output_eval.update({k:inf.util.Runtime.tf_sess.run(v)})
            else:
                output_eval = inf.util.Runtime.tf_sess.run(f(*args, **kwargs))

            return output_eval
        return f(*args, **kwargs)
    return wrapper




def singleton(class_):
    class class_w(class_):
        _instance = None
        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w,
                                    class_).__new__(class_,
                                                    *args,
                                                    **kwargs)
                class_w._instance._sealed = False
            return class_w._instance
        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True
    class_w.__name__ = class_.__name__
    return class_w

