import chainer
import numpy as np

from test.util import generate_kernel_test_case, wrap_template
from webdnn.frontend.chainer.converter import ChainerConverter
from webdnn.graph.order import OrderNCHW


@wrap_template
def template(ksize=3, stride=1, pad=0, nobias=True, description=""):
    link = chainer.links.Convolution2D(4, 10, ksize=ksize, stride=stride, pad=pad, nobias=nobias)
    vx = chainer.Variable(np.random.rand(2, 4, 6, 11).astype(np.float32))
    vy = link(vx)

    graph = ChainerConverter().convert_from_inout_vars([vx], [vy])

    x = graph.inputs[0]
    y = graph.outputs[0]

    generate_kernel_test_case(
        description=f"[chainer] L.Convolution2D {description}",
        graph=graph,
        inputs={x: np.transpose(vx.data, [OrderNCHW.axes_dict[a] for a in x.order.axes])},
        expected={y: np.transpose(vy.data, [OrderNCHW.axes_dict[a] for a in y.order.axes])},
        EPS=1e-2
    )


def test():
    template()


def test_nobias():
    template(nobias=True)


def test_irregular_kernel_size():
    template(ksize=(3, 4))


def test_irregular_stride_size():
    template(stride=(2, 3))


def test_irregular_padding_size():
    template(pad=(1, 2))


def test_irregular_size():
    template(ksize=(3, 5), stride=(2, 3), pad=(1, 3))
