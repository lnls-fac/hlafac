
import elements


def element_list():
    q1 = elements.Quadrupole(name='Q1', k=0.3)
    d1 = elements.Drift(name='D1', length=2.5)

    return [q1, d1]
