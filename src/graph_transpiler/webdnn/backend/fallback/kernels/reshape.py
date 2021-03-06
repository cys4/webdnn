from typing import List

from webdnn.backend.code_generator.allocator import MemoryLayout
from webdnn.backend.fallback.generator import FallbackDescriptorGenerator
from webdnn.backend.fallback.kernel import Kernel
from webdnn.graph.operators.reshape import Reshape
from webdnn.util.misc import mul

# EcmaScript3 to support older browsers

source = """
reshape: function(input_arrays, output_arrays, option) {
var x = input_arrays[0];
var y = output_arrays[0];
var length = option.length | 0;

for (var i = 0; i < length; i++) {
  y[i] = x[i];
}

},

"""


# noinspection PyUnusedLocal
@FallbackDescriptorGenerator.register_handler(Reshape)
def reshape(op: Reshape, memory_layout: MemoryLayout) -> List[Kernel]:
    # Operation without need for transposition is currently supported
    x = op.inputs["x"]
    y = op.outputs["y"]

    assert x.order == op.parameters["in_order"]
    assert y.order == op.parameters["out_order"]
    assert y.size == mul(op.parameters["out_shape"])

    kernel = Kernel(
        {"reshape": source},
        "reshape",
        inputs=[x],
        outputs=[y],
        call_option={"length": x.size}
    )

    return [kernel]
