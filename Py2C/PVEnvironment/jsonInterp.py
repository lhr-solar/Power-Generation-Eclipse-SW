"""
jsonInterp.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 03/06/21
Last Modified: 03/06/21

Description: Test file trying to implement PVEnvironment interpolation of valid
json files.

TODO: enable extrapolation for data beyond the maxCycle parameter.
"""

import json
import jsbeautifier

source = {}
fn = "../External/SingleCell.json"
MAX_CYCLE = 1000

f = open(fn)
source = json.load(f)

print("\n".join("{}\t{}".format(k, v) for k, v in source.items()))

# For module entry in the PV MODEL
for (key1, module) in source["pv_model"].items():
    print("\n")
    print("\n".join("{}\t{}".format(k, v) for k, v in module.items()))
    print("\n")

    # If the module type is array and requires interpolation
    if module["env_type"] == "Array":
        if module["needs_interp"] == True:
            # Gather a list of all current cycle events.
            entries = []
            for entry in module["env_regime"]:
                entries.append(entry)
            print(entries)
            print()

            # Take the current entry and next entry, and add all interpolations
            # to a new list.
            newEntries = []

            for idx, entry in enumerate(entries[0:-1]):
                thisElem = entry
                nextElem = entries[(idx + 1) % len(entries)]
                numEntries = nextElem[0] - thisElem[0]
                slopeIrrad = (nextElem[1] - thisElem[1]) / numEntries
                print(slopeIrrad)
                slopeTemp = (nextElem[2] - thisElem[2]) / numEntries
                print(slopeTemp)
                for idx in range(thisElem[0], nextElem[0] + 1):
                    newEntries.append(
                        [
                            idx,
                            thisElem[1] + slopeIrrad * (idx - thisElem[0]),
                            thisElem[2] + slopeTemp * (idx - thisElem[0]),
                        ]
                    )
                print(thisElem, nextElem)

            # Write the last interpolated event for all cycles extending
            # to max_cycles.
            lastEvent = newEntries[-1]
            print(lastEvent)
            for cycle in range(lastEvent[0] + 1, MAX_CYCLE + 1):
                newEntries.append([cycle, lastEvent[1], lastEvent[2]])

            print("\n".join("{}\t{}".format(k, v) for k, v in module.items()))

            module["env_regime"] = newEntries

            module["needs_interp"] = False
            # Write back to file. JSBeautifier puts internal arrays on a single line.
            with open(fn, "w") as fp:
                options = jsbeautifier.default_options()
                options.indent_size = 4
                fp.write(jsbeautifier.beautify(json.dumps(source), options))
