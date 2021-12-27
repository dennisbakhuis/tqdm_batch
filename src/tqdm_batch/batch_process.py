from typing import List, Dict, Union, Callable
from  math import ceil
from threading import Thread
from multiprocessing import Manager

from joblib import Parallel, delayed

from .progress_bar import progress_bar
from .task_wrapper import task_wrapper


def batch_process(
    items: list,
    function: Callable,
    n_workers: int=8,
    sep_progress: bool=False,
    *args,
    **kwargs,
    ) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Batch process a list of items

    The <items> will be divided into n_workers batches which process
    the list individually using joblib. When done, all results are
    collected and returned as a list.

    Parameters:
    -----------
    items : list
      List of items to batch process. This list will be divided in
      n_workers batches and processed by the function.
    function : Callable
      Function used to process each row. Format needs to be:
      callable(item, *args, **kwargs).
    n_workers : int (Default: 8)
      Number of processes to start (processes). Generally there is
      an optimum between 1 <= n_workeres <= total_cpus as there is
      an overhead for creating separate processes.
    sep_progress : bool (Default: False)
      Show a separate progress bar for each worker.
    *args, **kwargs : -
      (named) arguments to pass to batch process function.

    Returns:
    --------
    input_items : List [ Dict [ str, Union [ str, List [ str ]]]]
      List of processed input_items with collected id, words,
      tokens, and labels.
    """
    # Divide data in batches
    batch_size = ceil(len(items) / n_workers)
    batches = [
        items[ix:ix+batch_size]
        for ix in range(0, len(items), batch_size)
    ]

    # Check single or multiple progress bars
    if sep_progress:
        totals = [len(batch) for batch in batches]
    else:
        totals = len(items)

    # Start progress bar in separate thread
    manager = Manager()
    queue = manager.Queue()
    try:
        progproc = Thread(target=progress_bar, args=(totals, queue))
        progproc.start()

        # Parallel process the batches
        result = Parallel(n_jobs=n_workers)(
            delayed(task_wrapper)
            (pid, function, batch, queue, *args, **kwargs)
            for pid, batch in enumerate(batches)
        )

    finally:
        # Stop the progress bar thread
        queue.put('done')
        progproc.join()

    # Flatten result
    flattened = [item for sublist in result for item in sublist]

    return flattened
