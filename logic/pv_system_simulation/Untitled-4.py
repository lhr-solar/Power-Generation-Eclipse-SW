
    # def fit_parameters(
    #     self, data, irradiance=None, temperature=None, ideality_factor=None
    # ):
    #     def residual(params, data, self):
    #         values = params.valuesdict()
    #         irradiance = values["irradiance"] * 1e7
    #         temperature = values["temperature"] * 1e7
    #         ideality_factor = values["ideality_factor"] * 1e7
    #         self.parameters["ideality_factor"] = ideality_factor

    #         # Generate an arbitrary amount of points
    #         points = self.get_voltage_curves(irradiance, temperature)
    #         # Match the size of either
    #         if len(data) > len(points):
    #             data = np.random.permutation(data)[: len(points)]
    #         elif len(data) < len(points):
    #             points = np.random.permutation(points)[: len(data)]

    #         # Compare similarity
    #         mae = similaritymeasures.mae(data, points)
    #         return mae

    #     data, fitting_parameters = super().fit_parameters(data, irradiance, temperature)

    #     # One optimizing parameter (N)
    #     fitting_parameters["ideality_factor"] = {
    #         "min": 0.5,
    #         "stc": 1.5,
    #         "max": 2.5,
    #         "val": ideality_factor,
    #         "given": ideality_factor is not None,
    #     }

    #     fitting_parameters = self._set_params_and_fit(
    #         data, fitting_parameters, residual
    #     )

    #     return data, fitting_parameters
