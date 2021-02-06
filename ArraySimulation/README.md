# README

## Author/Maintainer

The author and maintainer of this utility is Matthew Yu (2020).

---

## Install

Installation requirements can be found in `requirements.txt` and can be
installed using `pip3 install -r requirements.txt`. Python 3 is required.

---

## Usage

To use this application, run `python3 PVSim.py` in the root directory of
`ArraySimulation`. The UI should be fairly straightforward.

---

## Testing

Tests are stored for each class in `ArraySimulation/tests/`. These can be run
from the root folder `ArraySimulation/` with the command `pytest .`

All tests are by default `ON`. Some tests may be marked as `additional`; these
may take significant time to process due to their time complexity or processing
requirements. To not run these, use the command `pytest . -m "not additional"`.

---

## Development

After making changes, please run the [black formatter](https://github.com/psf/black) with the command
`python -m black {source_file_or_directory}`.

---

## TODO

The list below are some files that require a refactor in some sort of way.

- PVSource/PVSource.py
  - [ ] Implementation of quick multi-module calculation.
    - This can be either with a fake but similar model (see Afnan's work) or a
      more realistic calculation, probably using Lagragian. Focus is getting the
      model up with MPPT algorithms testing on it.
  - [ ] After the prior point is completed, tests should be updated to reflect this.
- MPPT/MPPTAlgorithms
  - Golden.py
    - [ ] Tests should be written for this file.
  - Ternary.py
    - [ ] Tests should be written for this file.
  - Bisection.py
    - [ ] This needs to be crosschecked with the current simulator, as discrepancies
      between implementation and design document have been found.
    - [ ] Tests should be written for this file.
  - PandO.py
    - [ ] Tests should be written for this file.
  - IC.py
    - [ ] Tests should be written for this file.
  - FC.py
    - [x] This file needs to be implemented. See mppt_dP_dV_feedback_control.py
      for further details on how to implement this.
    - [ ] Tests should be written for this file.
- Controller/
  - DataController.py
    - [ ] Further methods used for MPPT algorithms should be implemented, with
      more control on what can be selected and done. For example, arguments for
      the stride algorithm along with the MPPT algorithm (if applicable) should be
      able to be passed in.
  - Console.py
    - [ ] This Class could be converted into a builder class for objects. Besides
      buttons, it should have combo boxes and/or text boxes with validation.
  - SourceView.py
    - [x] This Class should simplify its UI layout and data management scheme.
  - MPPTView.py
    - [x] This Class should implement its UI layout scheme and data management
      scheme.