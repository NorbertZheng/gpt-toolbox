#!/usr/bin/env python3
"""
Created on 17:08, Mar. 21st, 2023

@author: Norbert Zheng
"""
import os
import logging
import datetime
# local dep
if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

__all__ = [
    "Paths",
]

class Paths:
    """
    `Paths` object of current training process.
    """

    def __init__(self, base):
        """
        Creates directories for storing data during a model training run.

        Args:
            base: The base path of current project.

        Returns:
            None
        """
        ## Initialize parameters.
        self.base = base
        ## Initialize variables.
        # Get current `date` for saving folder, and initialize current
        # `run` to create a new run folder within the current date.
        date, run = datetime.datetime.today().strftime("%Y-%m-%d"), 0
        # Find the current `run`: the first run that doesn't exist yet.
        while True:
            # Construct new paths.
            self.run = os.path.join(self.base, "summaries", date, str(run))
            self.papers = os.path.join(self.run, "papers")
            # Update current `run`.
            run += 1
            # Once paths doesn't exist yet, create new folders.
            if not os.path.exists(self.run) and not os.path.exists(self.papers):
                os.makedirs(self.run); os.makedirs(self.papers); break
        # Initialize logger.
        self.logger = self._init_logger(self.run, "summaries")

    """
    init funcs
    """
    # def _init_logger func
    def _init_logger(self, path, name):
        """
        Create logger, output during training can be stored to file in a consistent way, which is saved in `run`.

        Args:
            path: The directory path of logger.
            name: The file name of logger.

        Returns:
            logger: Created logger object.
        """
        # Create new logger.
        logger = logging.getLogger(name); logger.setLevel(logging.INFO)
        # Remove any existing handlers so you don't output to old files, or to
        # new files twice - important when resuming training exsiting model.
        logger.handlers = []
        # Create a file handler, and create a logging format.
        handler = logging.FileHandler(os.path.join(path, name+".log")); handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s: %(message)s"); handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Return the logger object.
        return logger

if __name__ == "__main__":
    # Initialize the base path of current project.
    base = os.path.join(os.getcwd(), os.pardir)
    # Instantiate `Paths` object.
    paths_inst = Paths(base)

