# README

## Author/Maintainer

The author and maintainer of this utility is Matthew Yu (2020).

## Testing

Tests are stored for each class in `ArraySimulation/tests/`. These can be run
from the root folder `ArraySimulation/` with the command `pytest .`

All tests are by default `ON`. Some tests may be marked as `additional`; these
may take significant time to process due to their time complexity or processing
requirements. To not run these, use the command `pytest . -m "not additional"`.
