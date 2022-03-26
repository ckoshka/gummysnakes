# gummysnakes

```python
from gummysnakes import coerce

@coerce
class Seed:
    pass

@coerce
class OrangeTree:
    pass

@coerce
def grow_seed(s: Seed) -> OrangeTree:
    print("This might take a while...")
    return OrangeTree()

@coerce
class Orange:
    pass

@coerce
def pick_oranges(t: OrangeTree) -> List[Orange]:
    print("Picking some oranges for you...")
    return [Orange()]

@coerce
class OrangeJuice:
    pass

@coerce
def make_orange_juice(os: List[Orange]) -> OrangeJuice:
    print("Making orange juice!")
    return OrangeJuice()

gimme_an_orange = Seed() >> OrangeJuice

print(f"Here is your orange juice: {gimme_an_orange}")
```

Result:

```
This might take a while...
Picking some oranges for you...
Making orange juice!
Here is your orange juice: OrangeJuice({})
```

```python
import time
import random
def fail_at_something():
    result = 1 / 0

def fail_again():
    raise Exception("Wuh woh, someone did a fucky wucky!")

def make_pizza_dough():
    return "Dough"

def add_salami(pizza_base: str):
    return pizza_base + " with salami"

def add_cheese(pizza_base: str):
    print(pizza_base + " and cheese!")

def gimme_a_random_number(num: int):
    print(random.randint(0, num))

Overloader.do_all()
    
(((fail_at_something | fail_again) | make_pizza_dough >> add_salami >> add_cheese) & gimme_a_random_number[1000] * 3)()
```

Result:

```
Dough with salami and cheese!
817
301
349
```
