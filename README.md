# efsa-tools <img src="https://raw.githubusercontent.com/openefsa/efsa_tools/main/media/logo.png" height="140" align="right">

[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-brightgreen.svg)](https://lifecycle.r-lib.org/articles/stages.html#stable) [![codecov](https://codecov.io/gh/openefsa/efsa_tools/branch/main/graph/badge.svg?token=0YQIJKISMA)](https://codecov.io/gh/openefsa/efsa_tools)

## Overview

The **efsa-tools** package brings together all the functions developed for
EFSA's ad hoc data collections, providing tools for dataset operations as well
as utilities designed to preserve data history.

The package is intended for researchers, analysts, and practitioners who
require convenient programmatic access to data collection utilities.

During installation, the following packages developed by EFSA are also
installed:
- **eppoPynder** - [Website](https://openefsa.github.io/eppoPynder/) | [PyPI](https://pypi.org/project/eppoPynder/).
- **pystiller** - [Website](https://openefsa.github.io/pystiller/) | [PyPI](https://pypi.org/project/pystiller/).

These packages are not required to use **efsa-tools**, but are included for
convenience and can be imported and used directly in the code if needed:

```python
import eppopynder
# and/or
import pystiller
```

## Installation

### From PyPI

```
pip install efsa-tools
```

### Development version

To install the latest development version:

```
pip install git+https://github.com/openefsa/efsa_tools.git
```

## Usage

Once installed, load the package as usual:

```python
from efsa_tools import *
```

Basic usage examples and full documentation are available in the package
[guide](https://openefsa.github.io/efsa_tools/guide/).

## Authors and maintainers

- **Lorenzo Copelli** (author, [ORCID](https://orcid.org/0009-0002-4305-065X)).
- **Luca Belmonte** (author, maintainer, [ORCID](https://orcid.org/0000-0002-7977-9170)).

## Links

- **Source code**: [GitHub - openefsa/efsa_tools](https://github.com/openefsa/efsa_tools).
- **Bug tracker**: [Issues on GitHub](https://github.com/openefsa/efsa_tools/issues).
