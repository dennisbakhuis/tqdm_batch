# tqdm_batch
Batch processing using joblib including tqdm progress bars

Add batch processing to joblib, including tqdm progress bars.

## Install
```bash
pip install tqdm_batch
```

## Usage
Process a list of `items` using a `function`.

```python
from tqdm_batch import batch_process
import random
import time

def batch_process_function(row, some_var):
    time.sleep(0.01)
    return row + random.randint(0, some_var)

N = 1_000
items = range(N)

result = batch_process(
    items,
    batch_process_function,
    some_var=42,
    n_workers=6,
    sep_progress=True,
)
```

![Multi batch processing with progress bars](assets/multiprocessing_parallel3.png?raw=true "Multi batch processing with progress bars")
