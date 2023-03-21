#!/usr/bin/env python3
"""
Created on 19:12, Mar. 21st, 2023

@author: Norbert Zheng
"""
import tenacity
import functools
# local dep
if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

__all__ = [
    "request_retry",
]

# def request_retry func
def request_retry(func):
    """
    A decorator that provides a mechanism to repeat requests in response to exceeding a temporary quote limit.

    Args:
        func: func - The pointer of function.

    Returns:
        _wrapper: func - The wrapper of function.
    """
    # Get the wrapper of func.
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        return tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
            stop=tenacity.stop_after_attempt(5), reraise=True)(func)(*args, **kwargs)
    # Return the final `_wrapper`.
    return _wrapper

if __name__ == "__main__":
    print("decorator: Hello World!")

