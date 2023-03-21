#!/usr/bin/env python3
"""
Created on 21:09, Mar. 20th, 2023

@author: Norbert Zheng
"""
import re, os
import json, arxiv
import shutil, datetime
import numpy as np
# local dep
if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.pardir)
import utils

__all__ = [
    "Arxiv",
]

class Arxiv:
    """
    The Arxiv downloader used to download the latest papers on arxiv.
    """

    def __init__(self, query, filter_keys):
        """
        Initialize `Arxiv` object to prepare current download process.

        Args:
            query: str - The query string, e.g. "ti: xx, au: xx, all: xx".
            filter_keys: list - The list of keys to filter searched papers.

        Returns:
            None
        """
        # Initialize parameters
        self.query = query
        self.filter_keys = filter_keys
        # Initialize variables.
        self.results = self._init_search()

    """
    init funcs
    """
    # def _init_search func
    def _init_search(self, max_results=30, sort_by="Relevance", sort_order="Descending"):
        """
        Get search results, then use `filter_keys` to remove items.

        Args:
            max_results: int - The number of maximum results during search.
            sort_by: str - The sort rule used during search, could be one of [Relevance,LastUpdatedDate].
            sort_order: str - The sort order used during search, could be one of [Ascending,Descending].

        Returns:
            results: list - The list of filterred `arxiv.arxiv.Result`s.
        """
        # Initialize search, then get all `results`.
        search = arxiv.Search(query=self.query, max_results=max_results,
            sort_by=getattr(arxiv.SortCriterion, sort_by), sort_order=getattr(arxiv.SortOrder, sort_order))
        results = [result_i for result_i in search.results()]
        # Log information about the initial search process.
        print((
            "INFO: Get {:d} articles after searching arxiv with query ({}), sorted by {} with {} order."
        ).format(len(results), self.query, sort_by.lower(), sort_order.lower()))
        # Filter `results` according to `filter_keys`.
        filter_results = []
        for result_i in results:
            # Get the abstraction part of current result item.
            abstraction_i = result_i.summary.replace("-\n", "-").replace("\n", " ")
            # Check whether all filter keys are in abstraction.
            filter_pass_i = np.array([filter_key_i.lower() in abstraction_i.lower()\
                for filter_key_i in self.filter_keys], dtype=np.bool_).all()
            if filter_pass_i: filter_results.append(result_i)
        # Log information about the filterred results.
        print((
            "INFO: Get {:d} articles after filterring arxiv with filter keys ({}), sorted by {} with {} order."
        ).format(len(filter_results), self.filter_keys, sort_by.lower(), sort_order.lower()))
        # Return the final `results`.
        return filter_results

    """
    download funcs
    """
    # def download func
    def download(self, path_papers):
        """
        Download search results to local path according to base path.

        Args:
            path_papers: str - The path to download papers.

        Returns:
            downloads: list - The list of successfully downloaded items, each contains [path,title,url,authors,abstraction].
        """
        # Make sure `path_papers` exists.
        assert os.path.exists(path_papers)
        # Store the current query configuration into the run path.
        # TODO: Write additional information (e.g. max_results, sort_by, sort_order) into json file.
        config = {"query":self.query,"filter_keys":self.filter_keys,}
        with open(os.path.join(path_papers, "config.json"), "w") as f: json.dump(config, f)
        # Initialize `downloads` as empty list.
        downloads = []
        # Start downloading papers to the run path.
        for result_i in self.results:
            try:
                # Initialize `fname_i` as `author_i/year_i/title_i.pdf`.
                fname_i = result_i.authors[0].name.split(" ")[-1].lower() +\
                    result_i.updated.strftime("%Y") + result_i.title.split(" ")[0].lower()
                # Remove unwanted characters from `fname_i`, e.g. `/ \ : * ? " < > |`.
                rm_characters = "[\/\\\:\*\?\"\<\>\|]"; fname_i = re.sub(rm_characters, "-", fname_i)
                # Refine `fname_i`, then add `.pdf` postfix.
                fname_i = fname_i.strip("-"); fname_i += ".pdf"
                # Download pdf with quote retry.
                self._download_pdf(result_i, path_papers, fname_i)
                # Successfully downloaded the specified pdf.
                path_i = os.path.join(path_papers, fname_i); assert os.path.exists(path_i)
                downloads.append(utils.DotDict({"path":path_i,"title":result_i.title,"url":result_i.entry_id,
                    "authors":[author_i.name for author_i in result_i.authors],
                    "abstraction":result_i.summary.replace("-\n", "-").replace("\n", " "),}))
            except Exception as e:
                print("INFO: When downloading {}, get the following error: {}".format(result_i.title, e))
        # Return the final `downloads`.
        return downloads

    # def _download_pdf func
    @utils.decorator.request_retry
    def _download_pdf(self, result, path_papers, fname):
        """
        Download the specified result to local path.

        Args:
            result: object - The specified search `arxiv.arxiv.Result`.
            path_papers: str - The path to download papers.
            fname: str - The file name to save the pdf.

        Returns:
            None
        """
        # Download the specified result to local path.
        result.download_pdf(path_papers, filename=fname)

if __name__ == "__main__":
    # Initialize the base path of current project.
    base = os.path.join(os.getcwd(), os.pardir)
    # Instantiate `Paths` object.
    paths_inst = utils.Paths(base)

    # Initialize the input arguments of `Arxiv`.
    query = "all: Decoding speech from non-invasive brain recordings"
    filter_keys = ["brain", "MEG", "decoding"]
    # Instantiate `Arxiv` object.
    arxiv_inst = Arxiv(query, filter_keys)
    # Download filterred arxiv results.
    downloads = arxiv_inst.download(paths_inst.papers)

