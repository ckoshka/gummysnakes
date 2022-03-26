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

```bash
This might take a while...
Picking some oranges for you...
Making orange juice!
Here is your orange juice: OrangeJuice({})
```
