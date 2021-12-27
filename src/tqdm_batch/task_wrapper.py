def task_wrapper(pid, function, batch, queue, *args, **kwargs):
    """
    Wrapper to add progress bar update
    """
    result = []
    for example in batch:
        result.append(function(example, *args, **kwargs))
        queue.put(f'update{pid}')
    return result
