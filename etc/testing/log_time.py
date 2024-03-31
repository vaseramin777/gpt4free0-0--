from time import time


async def log_time_async(method: callable, **kwargs):
    # This function logs the time taken to execute an asynchronous function.
    # It takes a method (a callable object) and any number of keyword arguments
    # (kwargs) to be passed to the method.

    start = time()  # Record the start time before calling the method.
    result = await method(**kwargs)  # Call the method asynchronously.
    secs = f"{round(time() - start, 2)} secs"  # Calculate the time taken.
    return " ".join([result, secs]) if result else secs  # Return the result and time taken.


def log_time_yield(method: callable, **kwargs):
    # This function logs the time taken to execute a generator function.
    # It takes a method (a callable object) and any number of keyword arguments
    # (kwargs) to be passed to the method.

    start = time()  # Record the start time before calling the method.
    result = yield from method(**kwargs)  # Call the method and get the generator result.
    yield f" {round(time() - start, 2)} secs"  # Yield the time taken.


def log_time(method: callable, **kwargs):
    # This function logs the time taken to execute a synchronous function.
    # It takes a method (a callable object) and any number of keyword arguments
    # (kwargs) to be passed to the method.

    start = time()  # Record the start time before calling the method.
    result = method(**kwargs)  # Call the method synchronously.
    secs = f"{round(time() - start, 2)} secs"  # Calculate the time taken.
    return " ".join([result, secs]) if result else secs  # Return the result and time taken.
