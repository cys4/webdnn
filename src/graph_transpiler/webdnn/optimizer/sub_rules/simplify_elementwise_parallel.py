from typing import Tuple

from webdnn.graph import traverse
from webdnn.graph.graph import Graph
from webdnn.graph.operators.elementwise import Elementwise
from webdnn.graph.operators.elementwise_add import ElementwiseAdd
from webdnn.graph.optimize_rule import OptimizeRule
from webdnn.graph.variables.constant_variable import ConstantVariable
from webdnn.util import flags


class SimplifyElementwiseParallel(OptimizeRule):
    def flags(self):
        return [
            flags.optimize.OPTIMIZE,
            flags.optimize.SIMPLIFY_ELEMENTWISE,
            flags.optimize.SIMPLIFY_ELEMENTWISE_PARALLEL
        ]

    def optimize(self, graph: Graph) -> Tuple[Graph, bool]:
        flag_changed = False
        for op1 in traverse.filter_nodes(traverse.listup_operators(graph), Elementwise):  # type: Elementwise
            if len(op1.inputs) <= 1:
                continue

            x0 = op1.inputs["x0"]
            x1 = op1.inputs["x1"]

            if isinstance(op1, ElementwiseAdd):
                op2 = x0.output_from
                op3 = x1.output_from

                if isinstance(op2, ElementwiseAdd) and isinstance(op3, ElementwiseAdd) and len(x0.input_to) == 1 and len(x1.input_to) == 1:

                    #
                    #  x2 -+
                    #      +-[op2: ElementwiseAdd]-> x0 -+
                    #  x3 -+                             |
                    #                                    +-[op1: ElementwiseAdd]-> y
                    #  x4 -+                             |
                    #      +-[op3: ElementwiseAdd]-> x1 -+
                    #  x5 -+
                    #

                    x2 = op2.inputs["x0"]
                    x3 = op2.inputs["x1"]
                    x4 = op3.inputs["x0"]
                    x5 = op3.inputs["x1"]

                    cs = []
                    xs = []

                    for x in [x2, x3, x4, x5]:
                        if isinstance(x, ConstantVariable):
                            cs.append(x)
                        else:
                            xs.append(x)

                    if len(cs) >= 2:
                        y = op1.outputs["y"]

                        y_new = cs[0]
                        for c in cs[1:]:
                            y_new = y_new + c
                        for x in xs:
                            y_new = y_new + x

                        op1.remove_all()
                        op2.remove_all()
                        op3.remove_all()

                        y.change_order(y_new.order)
                        y_new.replace(y)
                        flag_changed = True

        return graph, flag_changed
