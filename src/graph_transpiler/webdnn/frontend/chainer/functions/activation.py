from webdnn.graph.operators.concat import Concat

try:
    import chainer
except ImportError:
    pass

from webdnn.frontend.chainer.converter import ChainerConverter
from webdnn.graph.operators.clipped_relu import ClippedRelu
from webdnn.graph.operators.elu import Elu
from webdnn.graph.operators.hard_sigmoid import HardSigmoid
from webdnn.graph.operators.leaky_relu import LeakyRelu
from webdnn.graph.operators.relu import Relu
from webdnn.graph.operators.sigmoid import Sigmoid
from webdnn.graph.operators.softmax import Softmax
from webdnn.graph.operators.softplus import Softplus
from webdnn.graph.operators.tanh import Tanh


@ChainerConverter.register_handler("ClippedReLU")
def _convert_clipped_relu(converter: ChainerConverter, c_op: "chainer.functions.ClippedReLU"):
    x = converter.get_variable(c_op.inputs[0])
    y, = ClippedRelu(None, cap=c_op.cap)(x)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("CReLU")
def _convert_crelu(converter: ChainerConverter, c_op: "chainer.functions.CReLU"):
    x = converter.get_variable(c_op.inputs[0])
    y1, = Relu(None)(x)
    y2, = Relu(None)(-x)
    y, = Concat(None, axis=x.order.axes[c_op.axis])(y1, y2)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("ELU")
def _convert_elu(converter: ChainerConverter, c_op: "chainer.functions.ELU"):
    x = converter.get_variable(c_op.inputs[0])
    if c_op.alpha == 0:
        y, = Relu(None)(x)

    elif c_op.alpha == 1:
        y, = Elu(None)(x)

    else:
        y1, = Elu(None)(x)
        y2, = Relu(None)(x)
        y = (y1 * c_op.alpha) + y2 * (1 - c_op.alpha)

    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("HardSigmoid")
def _convert_hard_sigmoid(converter: ChainerConverter, c_op: "chainer.functions.HardSigmoid"):
    x = converter.get_variable(c_op.inputs[0])
    y, = HardSigmoid(None)(x)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("LeakyReLU")
def _convert_leaky_relu(converter: ChainerConverter, c_op: "chainer.functions.LeakyReLU"):
    x = converter.get_variable(c_op.inputs[0])
    y, = LeakyRelu(None, slope=c_op.slope)(x)
    converter.set_variable(c_op.outputs[0](), y)


# noinspection PyUnusedLocal
@ChainerConverter.register_handler("LogSoftmax")
def _convert_log_softmax(converter: ChainerConverter, c_op: "chainer.functions.LogSoftmax"):
    # TODO
    raise NotImplementedError("[ChainerConverter] LogSoftmax is not supported")


# noinspection PyUnusedLocal
@ChainerConverter.register_handler("LSTM")
def _convert_lstm(converter: ChainerConverter, c_op: "chainer.functions.LSTM"):
    # TODO
    raise NotImplementedError("[ChainerConverter] LSTM is not supported")


# noinspection PyUnusedLocal,PyUnresolvedReferences
@ChainerConverter.register_handler("PReLU")
def _convert_prelu(converter: ChainerConverter, c_op: "chainer.functions.activation.prelu.PReLUFunction"):
    # TODO
    raise NotImplementedError("[ChainerConverter] PReLU is not supported")


@ChainerConverter.register_handler("ReLU")
def _convert_relu(converter: ChainerConverter, c_op: "chainer.functions.ReLU"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Relu(None)(x)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Sigmoid")
def _convert_sigmoid(converter: ChainerConverter, c_op: "chainer.functions.Sigmoid"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Sigmoid(None)(x)
    converter.set_variable(c_op.outputs[0](), y)


# noinspection PyUnusedLocal
@ChainerConverter.register_handler("SLSTM")
def _convert_slstm(converter: ChainerConverter, c_op: "chainer.functions.SLSTM"):
    # TODO
    raise NotImplementedError("[ChainerConverter] SLSTM is not supported")


@ChainerConverter.register_handler("Softmax")
def _convert_softmax(converter: ChainerConverter, c_op: "chainer.functions.Softmax"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Softmax(None, axis=x.order.axes[c_op.axis])(x)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Softplus")
def _convert_softplus(converter: ChainerConverter, c_op: "chainer.functions.Softplus"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Softplus(None, beta=c_op.beta)(x)
    converter.set_variable(c_op.outputs[0](), y)


@ChainerConverter.register_handler("Tanh")
def _convert_tanh(converter: ChainerConverter, c_op: "chainer.functions.Tanh"):
    x = converter.get_variable(c_op.inputs[0])
    y, = Tanh(None)(x)
    converter.set_variable(c_op.outputs[0](), y)
