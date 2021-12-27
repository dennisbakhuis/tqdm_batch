from typing import Union, List
from multiprocessing import Queue

from tqdm.auto import tqdm


def progress_bar(
    totals: Union[int, List[int]],
    queue : Queue,
) -> None:
    """
    Progress bar Thread

    A separate thread to manage the progress of all
    workers. When totals is a integer value a
    single progress bar is created and all updates
    in the queue update this single bar. To have
    a progress bar for each worker, totals should
    be a list with totals for each worker.

    Parameters:
    -----------
    totals : Union[int, List[int]]
      Totals for the single bar or for each worker,
      depending if it is a List of int or a single
      int.
    queue : multiprocessing.Queue
      Queue to receive progress updates. progress_bar
      expects an 'update' string to update a single
      bar or a string with the pid of the worker
      (i.e. f'update{pid}'). When finished, send a
      'done' to terminate the Thread.
    """
    if isinstance(totals, list):
        splitted = True
        pbars = [
            tqdm(
                desc=f'Worker {pid + 1}',
                total=total,
                position=pid,
            )
            for pid, total in enumerate(totals)
        ]
    else:
        splitted = False
        pbars = [
            tqdm(total=totals)
        ]

    while True:
        try:
            message = queue.get()
            if message.startswith('update'):
                if splitted:
                    pid = int(message[6:])
                    pbars[pid].update(1)
                else:
                    pbars[0].update(1)
            elif message == 'done':
                break
        except:
            pass
    for pbar in pbars:
        pbar.close()
