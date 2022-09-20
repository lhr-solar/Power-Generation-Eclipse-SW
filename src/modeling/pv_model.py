"""_summary_
@file       pv_model.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Methods to model the characteristics of PVs.
@version    0.0.0
@date       2022-09-17
"""

from src.modeling.pv_model_ideal_cell import PVModelIdealCell


class PVModel:
    def __init__(self):
        self.models = {
            PVModelIdealCell.model_name(): PVModelIdealCell(0.721, 6.15, 153)
        }

    def list_models(self):
        return list(self.models.keys())

    def get_model(self, model_name):
        if model_name in self.models:
            return [True, self.models[model_name]]
        else:
            return [False, "Not in provided models."]

    # def model_has_cache(self, model_name):
    #     return False

    # def model(self, model_name):
    #     if self.model_has_cache(model_name):
    #         return self.model_cached(model_name)
    #     return None

    # def model_cached(self, model_name):
    #     return None
