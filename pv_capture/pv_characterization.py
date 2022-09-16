"""_summary_
@file       pv_characterization.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Methods to parse and save pv characterization files.
@version    0.0.0
@date       2022-09-15
"""


class PVCharacterization:
    def __init__(self):
        self.loaders = {}
        self.version_instances = [
            # Define versions here.
            pv_char_version_0_0_0()
        ]
        self.versions = [instance.get_version() for instance in self.version_instances]
        for instance in self.version_instances:
            self.set_version_loader(instance.get_version(), instance)

    def set_version_loader(self, version, loader_instance):
        self.loaders[version] = loader_instance

    def get_version(self):
        """_summary_
        Gets the latest loader version for PV characterization.

        Returns:
            str: Version numbering.
        """
        return self.versions[-1]

    def get_version_loader(self, file_path):
        file_candidate = open(file_path, "r")

        lines = file_candidate.readlines()
        if len(lines) == 0:
            return [False, "Invalid file format (no version arg)."]

        version_args = lines[0].split()
        if len(version_args) != 2:
            return [False, "Invalid file format (wrong num of version args)."]

        version = version_args[1]
        if version not in self.loaders:
            return [False, "Invalid file format (bad version)."]

        return [True, self.loaders[version]]

    def get_version_loader(self, version):
        return self.loaders[version]

    def load_file(self, file_path):
        return None

    def store_file(self, data):
        return None

    def characterize_data(self, data):
        data["power"] = []
        data["v_oc"] = 0.0
        data["i_sc"] = 0.0
        data["v_mpp"] = 0.0
        data["i_mpp"] = 0.0
        data["p_mpp"] = 0.0
        data["ff"] = 0.0
        data["eff"] = 0.0

        for (voltage, current) in zip(data["voltage"], data["current"]):
            power = voltage * current

            if voltage > data["v_oc"]:
                data["v_oc"] = voltage

            if current > data["i_sc"]:
                data["i_sc"] = current

            if power > data["p_mpp"]:
                data["v_mpp"] = voltage
                data["i_mpp"] = current
                data["p_mpp"] = power

            data["power"].append(power)

        data["ff"] = data["p_mpp"] / (data["v_oc"] * data["i_sc"])

        # TODO: Efficiency; requires p_in, which is dependent on the area of the PV.
        # data["eff"] = data["v_oc"] * data["i_sc"] * data["ff"] /

        return data

    def normalize_data(self, data):
        """_summary_
        Normalize the data to 1000 G and 25 C.

        Args:
            data (dict): Dict of the data to normalize.

        Returns:
            dict: Normalized dict data
        """
        # TODO: Normalize the data.
        return self.characterize_data(data)


class pv_char_version_0_0_0(PVCharacterization):
    def __init__(self):
        pass

    def get_version(self):
        return "v0.0.0"

    def load_file(self, file_path):
        file = open(file_path, "r")
        lines = file.readlines()

        data = {
            "version": lines[0].split()[1],
            "file_name": lines[1].split()[1],
            "brief": " ".join(lines[2].split()[1:]),
            "author": " ".join(lines[3].split()[1:]),
            "last_modified": lines[4].split()[1],
            "pv_type": lines[5].split()[1],
            "pv_id": lines[6].split()[1],
            "voltage": [],
            "current": [],
        }

        data["irradiance"] = lines[8].split()[2]
        data["temperature"] = lines[9].split()[2]

        lines = lines[11:]
        lines = [line.strip() for line in lines]
        for line in lines:
            entry = line.split(",")
            data["voltage"].append(float(entry[0]))
            data["current"].append(float(entry[1]))

        return data

    def store_file(self, file_path, data):
        file = open(file_path, "w+")
        file.write(f"__version: {data['version']}\n")
        file.write(f"__file: {data['file_name']}\n")
        file.write(f"__brief: {data['brief']}\n")
        file.write(f"__author: {data['author']}\n")
        file.write(f"__last_modified: {data['last_modified']}\n")
        file.write(f"__pv_type: {data['pv_type']}\n")
        file.write(f"__pv_id: {data['pv_id']}\n")
        file.write(f"\n")
        file.write(f"irradiance (G) {data['irradiance']}\n")
        file.write(f"temperature (C) {data['temperature']}\n")
        file.write(f"\n")
        file.write((f"Voltage (V),Current (A)\n"))
        for entry in zip(data["voltage"], data["current"]):
            file.write(f"{entry}\n")
        file.close()
