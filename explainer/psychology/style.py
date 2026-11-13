"""The colours of *Psychology, Built*: one meaning per colour, for the whole series (videos/psychology/SYLLABUS.md,
§3).

    from explainer.psychology import P
    curve.set_color(P.PSYCHE)      # the model's prediction: orange, in every part

Human data are white and Psyche is orange in every plot, so a glance tells model from data.  An original study is a
hollow marker and its replication a filled one.  Parts add names for their own objects in ``common.py``, built
from these where the meaning is the same.
"""

from types import SimpleNamespace

from manim import GREY_A, GREY_B, GREY_C, GREY_D, WHITE

P = SimpleNamespace(
    # who produced the numbers
    HUMAN=WHITE,  # human data: participants, historical measurements
    PSYCHE="#FF9F5A",  # the model subject: predictions, fits, simulated behaviour of one model
    POOL="#8FA8D9",  # the Pool: simulated participants (always tagged)
    # an experiment
    STIM=WHITE,  # the stimulus
    RESP="#5DADEC",  # the response
    # detection
    SIGNAL="#4FD1C5",
    NOISE=GREY_B,
    # learning
    PRED="#B48EF0",  # a prediction, an expectation
    ERR="#F26D6D",  # prediction error, residual, misfit
    REWARD="#F2C14E",
    # neurons
    EXC="#FF8A5B",  # excitation
    INH="#6FA8FF",  # inhibition
    # Bayes (as Statistics, Built)
    PRIOR="#B48EF0",
    LIK="#7BD88F",
    POST="#FF9F5A",
    # experiments on groups
    TREAT="#FF7F6E",
    CTRL="#7EC8F5",
    # bookkeeping
    ACCENT="#F7D154",  # the series' accent: chapter cards, the lit timeline and levels, "On you"
    ARCHIVE="#E3B98A",  # the Archive: historical data, with its source
    MECH="#FF9F5A",  # a faculty of the Homunculus replaced by mechanism (= PSYCHE)
    PERSON=GREY_A,  # a faculty still drawn as a little person
    GRID=GREY_D,
    DIM=GREY_C,
    TEXT_DIM=GREY_A,
)

# The Ledger's statuses (explainer.psychology.ledger.STATUSES)
STATUS_COLOR = {
    "replicated": "#5BD18B",
    "replicated, smaller": "#B5D86B",
    "contested": "#F2C14E",
    "failed": "#F25F5C",
    "not directly tested": GREY_B,
    "retracted": "#C56BD6",
    "story and record": "#6F9BF2",
}
