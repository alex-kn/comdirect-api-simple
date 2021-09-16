# Contributing

Welcome. This project aims to be a simple python wrapper for the REST API for private consumers of the German Comdirect bank (https://developer.comdirect.de). Contribution are welcome, be it in the form of pull requests or new issues.

## Getting started

To get started simply fork and clone the repository, followed by a quick `pip install -r requirements.txt` to install the needed dependencies in your environment.

Then start a python session in your terminal and dig in (see [Usage](https://github.com/alex-kn/comdirect-api-simple#usage)). Alternatively, use a Jupyter notebook as a playground to execute different requests repeatedly and compare the responses.

## Submitting Changes

Guidelines for Pull Requests:

* PRs should contain a list of changes in the description.
* Changes should be tested against the API. Unfortunately Comdirect doesn't provide a test server so the real API has to be used.
* Code should be formatted using [Black](https://black.readthedocs.io/)
