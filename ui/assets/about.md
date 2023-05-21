# Eclipse

Eclipse is a multifunctional application to characterize UT Austin's LHR Solar
power generation system. It performs the following tasks:

- control and monitor the IV Curve Tracer,
- characterize and analyze photovoltaic systems,
- create and model said systems,
- and simulate a virtual power generation system.

---

## What's New (Doc)

`Version 4.0.0`

Version 4.0.0 revamps the user interface for the software application, moving
over to custom QML files to describe the user interface. This has reduced the
backend code debt significantly while allowing the team to focus on custom
components for visualizing photovoltaic models.

We've also moved over to PySide6 from PyQt6, which comes with the LGPL license.

Further photovoltaic analysis has also been integrated, allowing for cell
comparison, binning, and matching.

---

## Credits

The primary maintainer of this software is Matthew Yu (matthewjkyu@gmail.com).

Thanks to the following for their help in developing this software and providing
feedback.

- Roy Mor
- Jared McArthur
- Afnan Mir
- Gary Hallock

---

## Copyright

Copyright (C) 2023 by Matthew Yu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
