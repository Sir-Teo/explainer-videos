"""Lab 1: subtract one task from another, then test what the subtraction assumed."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import chronometry as ch

TITLE = "Donders' subtraction, and a check that could fail"
GOAL = ("Simulate Donders' three methods with a chain of stages, recover the stage durations by subtraction, then "
        "show that a rival model has the same three means and that only the variances can tell when a stage was "
        "not purely inserted.")
TASKS = [
    "Cut the trials per method from 2,000 to 40. How wide are the standard errors of the two differences now?",
    "In prepared_models, change the go/no-go decision from 30 ms to 10 ms. Which stage durations move, and do the "
    "three means?",
    "Give the response stage of the simple task a CV of 0.2, 0.3, 0.42. At what value does the variance check "
    "first reject pure insertion with 4,000 trials?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    n = 2000
    models = ch.donders_models()  # stages built from Donders' own means: 201, 237 and 284 ms
    rt = {k: models[k].sample(n, rng) for k in "abc"}
    sub = ch.subtraction(rt["a"], rt["b"], rt["c"])
    lab.row("mean RT, methods a / c / b (ms)", " / ".join(f"{rt[k].mean():.1f}" for k in "acb") + "   (built in: 201 / 237 / 284)")
    lab.row("c - a: discrimination (ms)", f"{sub['discriminate']:.1f} +- {sub['discriminate_se']:.1f}   (built in: 36)")
    lab.row("b - c: choice (ms)", f"{sub['choose']:.1f} +- {sub['choose_se']:.1f}   (built in: 47)")
    assert abs(sub["discriminate"] - 36) < 5 * sub["discriminate_se"], "subtraction recovers the inserted stage"
    assert abs(sub["choose"] - 47) < 5 * sub["choose_se"]

    rival = ch.prepared_models()  # go/no-go contains a decision; a choice must be programmed
    stages = {s.name: s.mean for s in rival["b"].stages}
    lab.row("a rival model's means a / c / b (ms)", " / ".join(f"{rival[k].mean:.0f}" for k in "acb"))
    lab.row("its discrimination and choice (ms)", f"{stages['discriminate']:.0f} and {stages['choose']:.0f}   (Donders read 36 and 47)")
    assert all(abs(rival[k].mean - models[k].mean) < 1e-9 for k in "abc"), "the same three means"
    assert abs(stages["choose"] - 47) > 1, "but different stages"

    # two worlds with the same difference of means between the simple task and go/no-go
    m = 4000
    worlds = {"a stage is inserted": models["a"], "the response stage changes": models["a"].with_stage("respond", cv=0.42)}
    tests = {}
    for name, short in worlds.items():
        xs, xl = short.sample(m, rng), models["c"].sample(m, rng)
        tests[name] = dict(ch.insertion_test(xs, xl, n_boot=400, seed=seed), var_short=xs.var(), var_long=xl.var())
        t = tests[name]
        lab.row(f"{name}: Var[c] - Var[a] (ms^2)", f"{t['d_var']:+.0f} +- {t['se_var']:.0f}   mean difference {t['d_mean']:.1f} ms")
    ok, bad = tests["a stage is inserted"], tests["the response stage changes"]
    assert abs(ok["d_var"] - 36 ** 2 * 0.6 ** 2) < 5 * ok["se_var"], "variances add under pure insertion"
    assert bad["d_var"] < -5 * bad["se_var"], "a negative 'stage variance' refutes pure insertion"
    assert abs(ok["d_mean"] - bad["d_mean"]) < 4, "though the means cannot tell the two worlds apart"
    lab.note = ("Subtraction recovers a stage when the stage is purely inserted, but three means cannot show that "
                "it was: the variance of the harder task must exceed the easier one's, and here it can be checked.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(120.0, 460.0, 1.0)
    for k, color in zip("acb", (labs.BLUE, labs.PURPLE, labs.PINK)):
        ax[0].hist(rt[k], bins=np.arange(120, 461, 8), density=True, color=color, alpha=0.3)
        ax[0].plot(t, models[k].pdf(t), color=color, label=f"method {k}: mean {rt[k].mean():.0f} ms")
    ax[0].set(title="Three methods, one chain of stages", xlabel="reaction time (ms)", ylabel="density")
    ax[0].legend()
    names = list(tests)
    x = np.arange(2)
    ax[1].bar(x - 0.18, [tests[k]["var_short"] for k in names], 0.36, color=labs.BLUE, label="Var[RT] in the simple task")
    ax[1].bar(x + 0.18, [tests[k]["var_long"] for k in names], 0.36, color=labs.PURPLE, label="Var[RT] in go/no-go")
    ax[1].set_xticks(x, names)
    ax[1].set(title="The harder task must be the more variable one", ylabel="variance (ms$^2$)")
    ax[1].legend()
    lab.fig = fig
    return lab
