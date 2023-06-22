from typing import Any, List

from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
import json


class GNNNodeClassificationRunner(UncallableNamespace, IllegalAttrChecker):
    def train(self, graph_name: str, model_name: str, feature_properties: List[str], target_property: str,
              target_node_label: str = None, node_labels: List[str] = None) -> "Series[Any]":
        configMap = {
            "featureProperties": feature_properties,
            "targetProperty": target_property,
        }
        node_properties = feature_properties + [target_property]
        if target_node_label:
            configMap["targetNodeLabel"] = target_node_label
        mlTrainingConfig = json.dumps(configMap)
        # TODO query avaiable node labels
        node_labels = ["Paper"] if not node_labels else node_labels
        self._query_runner.run_query(f"CALL gds.upload.graph('{graph_name}', {{mlTrainingConfig: '{mlTrainingConfig}', modelName: '{model_name}', nodeLabels: {node_labels}, nodeProperties: {node_properties}}})")
