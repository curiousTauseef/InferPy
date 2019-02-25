from contextlib import contextmanager
from inferpy import exceptions
from inferpy.util import tf_graph


# This dict store the active (if active is True) context parameters of prob model builder,
# the model built as the initial model, and the builder vars that are being built now (model expanded?)
_properties = dict(
    active=False,
    build_graph=False,
    graph=None,
    builder_vars=None,
    builder_params=None
)


def is_active():
    # is the prob model builder context active?
    return _properties['active']


def is_building_graph():
    # is the prob model builder context active?
    return _properties['build_graph']


def register_variable(rv):
    # TODO: if not active, raise custom exception
    # rv is a Random Variable from inferpy
    if rv.name in _properties['builder_vars'] or rv.name in _properties['builder_params']:
        raise exceptions.NotUniqueRandomVariableName(
            'Random Variable names must be unique among Random Variables and Parameters. \
                Detected twice: {}'.format(rv.name))
    _properties['builder_vars'][rv.name] = rv


def register_parameter(p):
    # TODO: if not active, raise custom exception
    # p is a Parameter from inferpy
    if p.name in _properties['builder_params'] or p.name in _properties['builder_vars']:
        raise exceptions.NotUniqueParameterName(
            'Parameter names must be unique among Parameters and Random Variables. Detected twice: {}'.format(p.name))
    _properties['builder_params'][p.name] = p


def get_builder_variable(name):
    # TODO: if not active, raise custom exception
    # return the variable or parameter if exists. Otherwise, return None
    return _properties['builder_vars'].get(
        name,
        _properties['builder_params'].get(name, None)
        )


def get_var_parameters():
    # return {k: p.var for k, p in _properties['builder_params'].items()}
    return _properties['builder_params']


def get_graph():
    # TODO: if not active, raise custom exception
    # return the graph of dependencies of the prob model that is being built
    return _properties['graph']


def update_graph(rv_name):
    # TODO: if not active, raise custom exception
    # return the graph of dependencies of the prob model that is being built
    # create a new graph using the actual tf computational graph, and clean it using the actual
    # builder vars and the random var name which is being built
    if _properties['build_graph']:
        _properties['graph'] = tf_graph.get_graph(
            set(_properties['builder_vars']).union(
                set([rv_name])).union(
                    set(_properties['builder_params'])
                ))


@contextmanager
def builder(graph):
    # prob model builder context. Allows to get access to RVs as they are built (at the same time ed.tape registers vars)
    # We only allow to use one context level
    assert not _properties['active']
    _properties['active'] = True
    _properties['build_graph'] = graph is None
    if _properties['build_graph']:
        _properties['graph'] = tf_graph.get_empty_graph()
    else:
        _properties['graph'] = graph
    _properties['builder_vars'] = dict()
    _properties['builder_params'] = dict()
    try:
        yield
    finally:
        _properties['active'] = False
        _properties['build_graph'] = False
        _properties['graph'] = None
        _properties['builder_vars'] = None
        _properties['builder_params'] = None