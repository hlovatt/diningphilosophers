===================
Dining Philosophers
===================

Python solution to `The Dining Philosophers Problem
<https://en.wikipedia.org/wiki/Dining_philosophers_problem>`_
using ``asyncio`` only.
The solution technique used is the obvious one of
only ``await`` on the left and right chopsticks for
a short time before giving up and going back to thinking
for a random amount of time.

I'm classing this solution as 'obvious' since it is common
to try and grab a resource and if you can't wait a random
amount of time before retrying, e.g. collisions on
half-duplex networks like early ethernet implementations
use this technique (`CSMA/CD
<https://en.wikipedia.org/wiki/Carrier-sense_multiple_access_with_collision_detection>`_).

To demonstrate the lock-up of simple code,
that doesn't time out, the problem is
framed so that all the philosophers try and eat at the start,
but have a 'reaction-time' delay between picking up the left
chopstick and after the delay the right chopstick.
This ensures that at the start each philosopher picks up
their left chopstick but can't pick up their right chopstick,
because the next philosopher already has it.

Simplistic code that fails is given, but is commented out.
