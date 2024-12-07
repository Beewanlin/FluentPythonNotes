======
Tombola test
======

Every concrete subclass of Tombola should pass these tests.

>>> balls = list(range(3))
>>> globe = ConcreteTombola(balls)
>>> globe.loaded()
True

>>> globe.inspect()
(0, 1, 2)

Pick and collect balls:
>>> picks = []
>>> picks.append(globe.pick())
