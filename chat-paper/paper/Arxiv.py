#!/usr/bin/env python3
"""
Created on 20:02, Mar. 21st, 2023

@author: Norbert Zheng
"""
import io, os, fitz
from PIL import Image
# local dep
if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

__all__ = [
    "Arxiv",
]

class Arxiv:
    """
    The Arxiv paper parser used to parse the raw pdf of arxiv paper.
    """

    def __init__(self, config):
        """
        Initialize `Arxiv` object, then directly start current parse process.

        Args:
            config: DotDict - The configuration of the specified pdf, contains [path,title,url,authors,abstraction].
                path: str - The path of the specified paper (must be provided!).
                title: str - The title of the specified paper (must be provided!).
                url: str - The arxiv link of the specified paper.
                authors: list - The authors list of the specified paper.
                abstraction: str - The abstraction of the specified paper (must be provided!).

        Returns:
            None
        """
        # Initialize parameters.
        self.path = config.path; self.title = config.title
        self.url = config.url; self.authors = config.authors
        self.abstraction = config.abstraction
        # Parse text of current pdf.
        self.parse_text()

    """
    parse funcs
    """
    # def parse_text func
    def parse_text(self):
        """
        Parse the raw text of paper.

        Args:
            None

        Returns:
            None
        """
        # Open pdf document to start current parse process.
        self.pdf = fitz.open(self.path_paper)
        # Get the content of each section.
        self.sections = self._parse_sections()

    # def _parse_sections func
    def _parse_sections(self):
        """
        Get the content of each section.

        Args:
            None

        Returns:
            sections: DotDict - The content of each section.
        """

    # def _parse_sections_page func
    def _parse_sections_page(self):
        """
        Get the start page index of each section.

        Args:
            None

        Returns:
            sections_page: DotDict - The start page index of each section.
        """
        # Initialize `section_names` & `sections_page`.
        section_names = [
            # Abstract part.
            "Abstract",
            # Introduction part.
            "Introduction", "Related Work", "Background", "Preliminary", "Problem Formulation",
            # Method part.
            "Methods", "Methodology", "Method", "Approach", "Approaches",
            # Experiment part.
            "Materials and Methods", "Experiment Settings", "Experiment", "Experimental Results",
            "Evaluation", "Experiments", "Results", "Findings", "Data Analysis",
            # Discussion part.
            "Discussion", "Results and Discussion", "Conclusion",
            # Reference part.
            "References",
        ]; sections_page = DotDict()
        

if __name__ == "__main__":
    # local dep
    import utils, downloader

    """
    # Initialize the base path of current project.
    base = os.path.join(os.getcwd(), os.pardir)
    # Instantiate `Paths` object.
    paths_inst = utils.Paths(base)
    # Initialize the input arguments of `downloader.Arxiv`.
    query = "all: Decoding speech from non-invasive brain recordings"
    filter_keys = ["brain", "MEG", "decoding"]
    # Instantiate `downloader.Arxiv` object.
    downloader_inst = downloader.Arxiv(query, filter_keys)
    # Download filterred arxiv results.
    downloads = downloader_inst.download(paths_inst.papers)

    # Instantiate `paper.Arxiv` object.
    paper_inst = Arxiv(downloads[0])
    """
    paper_inst = Arxiv(utils.DotDict({'path': "./demo.pdf", 'title': 'Decoding speech from non-invasive brain recordings', 'url': 'http://arxiv.org/abs/2208.12266v1', 'authors': ['Alexandre Défossez', 'Charlotte Caucheteux', 'Jérémy Rapin', 'Ori Kabeli', 'Jean-Rémi King'], 'abstraction': 'Decoding language from brain activity is a long-awaited goal in both healthcare and neuroscience. Major milestones have recently been reached thanks to intracranial devices: subject-specific pipelines trained on invasive brain responses to basic language tasks now start to efficiently decode interpretable features (e.g. letters, words, spectrograms). However, scaling this approach to natural speech and non-invasive brain recordings remains a major challenge. Here, we propose a single end-to-end architecture trained with contrastive learning across a large cohort of individuals to predict self-supervised representations of natural speech. We evaluate our model on four public datasets, encompassing 169 volunteers recorded with magneto- or electro-encephalography (M/EEG), while they listened to natural speech. The results show that our model can identify, from 3s of MEG signals, the corresponding speech segment with up to 72.5% top-10 accuracy out of 1,594 distinct segments (and 44% top-1 accuracy), and up to 19.1% out of 2,604 segments for EEG recordings -- hence allowing the decoding of phrases absent from the training set. Model comparison and ablation analyses show that these performances directly benefit from our original design choices, namely the use of (i) a contrastive objective, (ii) pretrained representations of speech and (iii) a common convolutional architecture simultaneously trained across several participants. Together, these results delineate a promising path to decode natural language processing in real time from non-invasive recordings of brain activity.'}))

