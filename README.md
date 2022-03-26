# gummysnakes

```python
from gummysnakes import coerce
@coerce
class Food:
    def __init__(self, foodname: str) -> 'Food':
        self.foodname = foodname

@coerce
def str_to_food(s: str) -> Food:
    return Food(s)

@coerce
def food_to_review(f: Food) -> 'Review':
    return f"I ate {f.foodname} and it was delicious"

@coerce
def review_to_metareview(r: 'Review') -> 'MetaReview':
    return f"{r}? What a horrible review."

result = Food("oranges") >> 'MetaReview'
print(result)
```
