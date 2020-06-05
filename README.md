# repro-catalogue
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
[![Build Status](https://travis-ci.com/alan-turing-institute/repro-catalogue.svg?branch=master)](https://travis-ci.com/alan-turing-institute/repro-catalogue)
[![PyPI version](https://badge.fury.io/py/repro-catalogue.svg)](https://badge.fury.io/py/repro-catalogue)
[![Documentation Status](https://readthedocs.org/projects/pip/badge/)](https://repro-catalogue.readthedocs.io/en/latest/)

A command line tool to catalogue versions of data, code and results to support reproducibility of research projects.


## Contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Contributing](#contributing)
* [Contributors](#contributors)

## Introduction

Research projects are frequently updated - new data are added, and the code undergoes regular changes. Under these circumstances, it's easy to store results, yet lose track of the context in which they were produced.

The `catalogue` tool aids reproducibility by saving **hash values** of the input data and the results, along with the **git commit hash** of the code used to generate those results. The `catalogue` command line interface then allows the user to easily compare the hash values from different occasions on which the analysis was run so that changes to the input data, code and results can be identified and the impact on reproducibility can be understood.


## Installation

The package is available on PyPI and requires Python 3 to use:

```{bash}
pip install repro-catalogue
```

See [https://repro-catalogue.readthedocs.io/en](https://repro-catalogue.readthedocs.io/en) for full documentation on how to install and use the tool.


## Contributing

🚧 This repository is always a work in progress and everyone is encouraged to help us build something that is useful to the many. 🚧

Everyone is asked to follow our [code of conduct](CODE_OF_CONDUCT.md) and to checkout our [contributing guidelines](CONTRIBUTING.md) for more information on how to get started.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/LouiseABowler"><img src="https://avatars1.githubusercontent.com/u/25640708?v=4" width="100px;" alt=""/><br /><sub><b>Louise Bowler</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=LouiseABowler" title="Documentation">📖</a> <a href="#ideas-LouiseABowler" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3ALouiseABowler" title="Reviewed Pull Requests">👀</a> <a href="#projectManagement-LouiseABowler" title="Project Management">📆</a> <a href="#design-LouiseABowler" title="Design">🎨</a> <a href="#maintenance-LouiseABowler" title="Maintenance">🚧</a> <a href="#infra-LouiseABowler" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="http://isla.st"><img src="https://avatars2.githubusercontent.com/u/23707851?v=4" width="100px;" alt=""/><br /><sub><b>Isla</b></sub></a><br /><a href="#design-Islast" title="Design">🎨</a> <a href="#ideas-Islast" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=Islast" title="Documentation">📖</a></td>
    <td align="center"><a href="https://whitakerlab.github.io"><img src="https://avatars1.githubusercontent.com/u/3626306?v=4" width="100px;" alt=""/><br /><sub><b>Kirstie Whitaker</b></sub></a><br /><a href="#design-KirstieJane" title="Design">🎨</a> <a href="#ideas-KirstieJane" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-KirstieJane" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://sgibson91.github.io/"><img src="https://avatars2.githubusercontent.com/u/44771837?v=4" width="100px;" alt=""/><br /><sub><b>Sarah Gibson</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=sgibson91" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Asgibson91" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/kevinxufs"><img src="https://avatars2.githubusercontent.com/u/48526846?v=4" width="100px;" alt=""/><br /><sub><b>kevinxufs</b></sub></a><br /><a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Akevinxufs" title="Reviewed Pull Requests">👀</a> <a href="#userTesting-kevinxufs" title="User Testing">📓</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=kevinxufs" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/edaub"><img src="https://avatars0.githubusercontent.com/u/45598892?v=4" width="100px;" alt=""/><br /><sub><b>Eric Daub</b></sub></a><br /><a href="#design-edaub" title="Design">🎨</a> <a href="#ideas-edaub" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=edaub" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=edaub" title="Documentation">📖</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Aedaub" title="Reviewed Pull Requests">👀</a> <a href="#maintenance-edaub" title="Maintenance">🚧</a> <a href="#projectManagement-edaub" title="Project Management">📆</a></td>
    <td align="center"><a href="https://github.com/radka-j"><img src="https://avatars2.githubusercontent.com/u/29207091?v=4" width="100px;" alt=""/><br /><sub><b>Radka Jersakova</b></sub></a><br /><a href="#design-radka-j" title="Design">🎨</a> <a href="#ideas-radka-j" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=radka-j" title="Code">💻</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/pulls?q=is%3Apr+reviewed-by%3Aradka-j" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/alan-turing-institute/repro-catalogue/commits?author=radka-j" title="Documentation">📖</a> <a href="#maintenance-radka-j" title="Maintenance">🚧</a> <a href="#projectManagement-radka-j" title="Project Management">📆</a> <a href="#infra-radka-j" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
