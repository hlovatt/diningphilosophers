from asyncio import sleep, TaskGroup, wait_for, Lock, run
from dataclasses import dataclass
from random import random
from typing import Final

@dataclass
class Philosopher:
    name: str
    left_chopstick: Lock
    right_chopstick: Lock

    def __post_init__(self):
        self.dined = False

    async def _eat(self):
        # This locks up, because all waiting on right chopstick due to reaction time delay.
        # async with self.right_chopstick:
        #     print(f'{self.name} is eating.')
        #     await sleep(random())
        #     self.dined = True
        try:
            # To prevent lock up, only wait for a short time for right chopstick.
            await wait_for(self.right_chopstick.acquire(), random() / 13)
            print(f'{self.name} is eating.')
            await sleep(random())  # Eating time.
            self.dined = True
            self.right_chopstick.release()
        except TimeoutError:
            ...  # Times out when right chopstick not available.

    async def trying_to_eat(self):
        while not self.dined:
            print(f'{self.name} is trying to eat.')
            async with self.left_chopstick:
                await sleep(1 / 13)  # Reaction time causes a lock-up with simplistic code!
                await self._eat()
            print(f'{self.name} is thinking.')
            await sleep(random())  # Thinking time.

async def main():
    # philosopher_names: Final = ['Socrates', 'Plato', 'Aristotle', 'Pandrosion', 'Hypatia']
    philosopher_names: Final = ['Pandrosion', 'Hypatia']
    num_philosophers: Final = len(philosopher_names)
    chopsticks: Final = [Lock() for _ in range(num_philosophers)]
    print('All trying to eat.')
    async with TaskGroup() as tg:
        for i, name in enumerate(philosopher_names):
            philosopher = Philosopher(name, chopsticks[i], chopsticks[(i + 1) % num_philosophers])
            tg.create_task(philosopher.trying_to_eat())
    print('All dined and all thought.')

run(main())
