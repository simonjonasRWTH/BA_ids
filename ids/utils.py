from .autoregression.Autoregression import Autoregression
from .classifier.BLSTM import BLSTM
from .classifier.DecisionTree import DecisionTree
from .classifier.ExtraTrees import ExtraTrees
from .classifier.IsolationForest import IsolationForest
from .classifier.NaiveBayes import NaiveBayes
from .classifier.RandomForest import RandomForest
from .classifier.SVM import SVM
from .classifier.OCSVM import OCSVM
from .interarrivaltime.Mean import InterArrivalTimeMean
from .interarrivaltime.Range import InterArrivalTimeRange
from .kitsune.kitsune import Kitsune
from .oracles.DummyIDS import DummyIDS
from .oracles.OptimalIDS import OptimalIDS
from .simple.decimal import DecimalPlaces
from .simple.exists import ExistsIDS
from .simple.histogram import Histogram
from .simple.minmax import MinMax
from .simple.steadytime import SteadyTime

idss = [
    Autoregression,
    BLSTM,
    DecimalPlaces,
    DecisionTree,
    DummyIDS,
    ExistsIDS,
    ExtraTrees,
    Histogram,
    InterArrivalTimeMean,
    InterArrivalTimeRange,
    IsolationForest,
    Kitsune,
    MinMax,
    NaiveBayes,
    OCSVM,
    OptimalIDS,
    RandomForest,
    SVM,
    SteadyTime,
]


def get_all_iidss():
    return {ids._name: ids for ids in idss}
