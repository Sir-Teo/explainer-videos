from __future__ import annotations

import numpy as np

from videos.stats.stats63.common import *  # noqa: F403


def fpr_of(p, ppv, fnr):
    return p / (1 - p) * (1 - ppv) / ppv * (1 - fnr)


class Impossibility(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. The impossibility theorem: why both sides of the COMPAS debate were right.", 9,
                            r"Impossibility", r"One line of algebra", lit=(2016, 2017))
        self.identity()
        self.plug()
        self.chart()
        self.kleinberg()
        self.thresholds()
        self.label_()
        self.choice()

    def identity(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Alexandra Chouldechova derived it in 2017. Take a binary label, high or low, in one "
            "group with base rate p. <bookmark mark='b'/> Count the true positives two ways. Among the high labels, a "
            "fraction PPV are rearrested; among the rearrested, a fraction one minus FNR are labelled high. <bookmark "
            "mark='c'/> And the false positives: among the high labels, one minus PPV; among the not rearrested, a fraction "
            "FPR. Dividing one count by the other, the number of high labels cancels. <bookmark mark='d'/> The false "
            "positive rate equals p over one minus p, times one minus PPV over PPV, times one minus the false negative "
            "rate. An identity, true of every classifier in every group.",
            [(r"\text{true pos.}", r"=", r"\mathrm{PPV} \cdot \#\text{high} = (1 - \mathrm{FNR}) \cdot p n", 40),
             (r"\text{false pos.}", r"=", r"(1 - \mathrm{PPV}) \cdot \#\text{high} = \mathrm{FPR} \cdot (1 - p) n", 40),
             (r"\text{divide}", r":", r"\frac{1 - \mathrm{PPV}}{\mathrm{PPV}} = \frac{\mathrm{FPR}(1 - p)}{(1 - \mathrm{FNR}) p}", 40),
             (r"\mathrm{FPR}", r"=", r"\frac{p}{1 - p} \cdot \frac{1 - \mathrm{PPV}}{\mathrm{PPV}} \cdot (1 - \mathrm{FNR})", 40)],
            [r"Chouldechova (2017)", r"two counts", r"$\#$high cancels", r"an identity"],
            colors=[(3, S.ACCENT)])

    def plug(self):
        d = load("compas")
        B, W = d["rates"]["Black"], d["rates"]["white"]
        self.lad_voiceover(
            f"<bookmark mark='a'/> Check it on the table. <bookmark mark='b'/> For Black defendants: a base rate of "
            f"{B['base']:.3f}, a PPV of {B['ppv']:.3f} and a false negative rate of {B['fnr']:.3f} give a false positive "
            f"rate of {d['chouldechova']['Black']:.3f}, exactly the observed value. <bookmark mark='c'/> For white "
            f"defendants, {W['base']:.3f}, {W['ppv']:.3f} and {W['fnr']:.3f} give {d['chouldechova']['white']:.3f}, again "
            f"exact. <bookmark mark='d'/> So with base rates of fifty-two and thirty-nine percent, the first factor is "
            f"{B['base'] / (1 - B['base']):.2f} for one group and {W['base'] / (1 - W['base']):.2f} for the other. Equal "
            f"PPVs and equal false negative rates would force the false positive rates apart by that ratio, "
            f"{B['base'] / (1 - B['base']) / (W['base'] / (1 - W['base'])):.2f} to one.",
            [(r"\text{Black}", r":", rf"\tfrac{{{B['base']:.3f}}}{{{1 - B['base']:.3f}}} \cdot \tfrac{{{1 - B['ppv']:.3f}}}{{{B['ppv']:.3f}}} \cdot {1 - B['fnr']:.3f} = {d['chouldechova']['Black']:.3f}", 38),
             (r"\text{white}", r":", rf"\tfrac{{{W['base']:.3f}}}{{{1 - W['base']:.3f}}} \cdot \tfrac{{{1 - W['ppv']:.3f}}}{{{W['ppv']:.3f}}} \cdot {1 - W['fnr']:.3f} = {d['chouldechova']['white']:.3f}", 38),
             (r"\text{observed}", r":", rf"{B['fpr']:.3f}, \ \ {W['fpr']:.3f}", 40),
             (r"\text{odds ratio of base rates}", r":", rf"{B['base'] / (1 - B['base']) / (W['base'] / (1 - W['base'])):.2f}", 40)],
            [r"exact", r"exact", r"the table", r"what equal PPV and FNR force"],
            colors=[(0, GRPA), (1, GRPB)])

    def chart(self):
        d = load("compas")
        B, W = d["rates"]["Black"], d["rates"]["white"]
        ppv, fnr = (B["ppv"] + W["ppv"]) / 2, (B["fnr"] + W["fnr"]) / 2
        ps = np.linspace(0.2, 0.7, 120)
        A = axes([0.2, 0.7], [0, 1.0], x_length=7.2, y_length=4.4, xlabel=r"base rate $p$ of the group",
                 ylabel=r"false positive rate forced by the identity", xticks=[0.2, 0.3, 0.4, 0.5, 0.6, 0.7], yticks=[0, 0.25, 0.5, 0.75, 1],
                 center=[-2.4, 0.2, 0])
        ax = A.ax
        cb = polyline(ax, ps, fpr_of(ps, B["ppv"], B["fnr"]), GRPA, 2.5, 0.6)
        cw = polyline(ax, ps, fpr_of(ps, W["ppv"], W["fnr"]), GRPB, 2.5, 0.6)
        common = polyline(ax, ps, fpr_of(ps, ppv, fnr), S.ACCENT, 4)
        db = Dot(ax.c2p(B["base"], B["fpr"]), radius=0.1, color=GRPA)
        dw = Dot(ax.c2p(W["base"], W["fpr"]), radius=0.1, color=GRPB)
        eb = Dot(ax.c2p(B["base"], fpr_of(B["base"], ppv, fnr)), radius=0.08, color=S.ACCENT)
        ew = Dot(ax.c2p(W["base"], fpr_of(W["base"], ppv, fnr)), radius=0.08, color=S.ACCENT)
        side = side_groups([
            [(r"orange and teal: \ each group's", GREY_A), (r"own PPV and FNR", GREY_A)],
            [(r"dots: \ the observed FPRs", WHITE), (rf"{B['fpr']:.2f} and {W['fpr']:.2f}", WHITE)],
            [(rf"gold: \ a shared PPV {ppv:.2f}, \ FNR {fnr:.2f}", S.ACCENT),
             (rf"forces {fpr_of(B['base'], ppv, fnr):.2f} and {fpr_of(W['base'], ppv, fnr):.2f}", S.ACCENT)],
            [(r"equal FPRs need equal base rates", BADC), (r"or a perfect classifier", BADC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> The identity as a picture: the false positive rate it forces, against a group's base "
            f"rate, holding the PPV and false negative rate fixed. Orange and teal use each group's own values. <bookmark "
            f"mark='b'/> The two observed false positive rates sit on their curves, as they must. <bookmark mark='c'/> Now "
            f"suppose a new score had exactly equal PPVs and false negative rates in both groups, at their averages, "
            f"{ppv:.2f} and {fnr:.2f}. The gold curve: at the two base rates, it forces false positive rates of "
            f"{fpr_of(B['base'], ppv, fnr):.2f} and {fpr_of(W['base'], ppv, fnr):.2f}. <bookmark mark='d'/> The disparity "
            f"ProPublica found is not a defect peculiar to COMPAS. Any score with equal predictive values and equal miss "
            f"rates must have it, unless base rates are equal or prediction is perfect."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"ProPublica's COMPAS data (the Museum)")))
            vo.wait_until("a")
            self.play(Create(cb), Create(cw), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(db), FadeIn(dw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(common), FadeIn(eb), FadeIn(ew), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def kleinberg(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Jon Kleinberg, Sendhil Mullainathan and Manish Raghavan proved the version for scores "
            "rather than labels, in 2016. <bookmark mark='b'/> Ask for three things: calibration within groups; balance "
            "for the positive class, meaning the people who are rearrested get the same average score in each group; and "
            "balance for the negative class, the same for people who are not. <bookmark mark='c'/> All three can hold "
            "together only if the base rates are equal, or prediction is perfect, every score zero or one. <bookmark "
            "mark='d'/> And approximately: if all three hold nearly, the base rates must be nearly equal or the prediction "
            "nearly perfect. The conflict is not an artefact of thresholds.",
            [(r"\text{calibration}", r":", r"P(Y = 1 \mid R = r, A) = r", 40),
             (r"\text{balance}", r":", r"E[R \mid Y = 1, A], \ E[R \mid Y = 0, A] \ \text{equal across } A", 40),
             (r"\text{all three}", r"\Rightarrow", r"\text{equal base rates, \ or perfect prediction}", 40),
             (r"\text{approximately}", r":", r"\text{also}", 40)],
            [r"Kleinberg, \ Mullainathan \& Raghavan (2016)", r"for scores", r"the theorem", r"robust"],
            colors=[(2, BADC)])

    def thresholds(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> So something must give, and the statistics can say what each choice costs. <bookmark "
            "mark='b'/> Sam Corbett-Davies, Emma Pierson, Avi Feller, Sharad Goel and Aziz Huq framed it in 2017 as Part "
            "forty-five's decision theory: detaining someone has a cost, releasing someone who reoffends has another. "
            "<bookmark mark='c'/> Under that framing the rule that minimizes expected cost is one threshold on a calibrated "
            "risk, the same for everyone, and it violates separation whenever base rates differ. <bookmark mark='d'/> "
            "Equalizing false positive rates instead needs different thresholds for different groups, detaining some "
            "lower-risk people of one group or releasing some higher-risk people of another. Each option is a value "
            "judgement; the arithmetic makes the trade explicit.",
            [(r"\text{decision theory}", r":", r"\text{costs of detaining and releasing}", 40),
             (r"\text{optimal}", r":", r"\text{one threshold on calibrated risk}", 40),
             (r"\text{consequence}", r":", r"\text{unequal error rates}", 40),
             (r"\text{equal FPR}", r":", r"\text{group-specific thresholds}", 40)],
            [r"Corbett-Davies et al. (2017)", r"Part 45", r"separation fails", r"a value judgement"],
            colors=[(1, S.ACCENT)])

    def label_(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And a statistician's caution about the outcome itself. <bookmark mark='b'/> Y is "
            "rearrest, not reoffending. Arrest depends on where police patrol and whom they stop. <bookmark mark='c'/> If "
            "one group is policed more heavily, its members are rearrested more often for the same behaviour, and a score "
            "calibrated to rearrest is calibrated to the policing, not to the conduct. <bookmark mark='d'/> That is Part "
            "forty-one's differential measurement error, in the outcome. Every criterion in this chapter inherits it, and no "
            "criterion computed from the data alone can detect it. Chapter eleven needs a causal model for exactly this "
            "reason.",
            [(r"Y", r"=", r"\text{rearrest, \ not reoffending}", 40),
             (r"\text{arrests}", r":", r"\text{depend on policing}", 40),
             (r"\text{calibration to}", r":", r"\text{a biased label}", 40),
             (r"\text{the fix}", r":", r"\text{a model of the measurement}", 40)],
            [r"the outcome", r"the measurement", r"bias inherited", r"Part 41; \ chapter 11"],
            colors=[(0, BADC)])

    def choice(self):
        self.list_voiceover(
            "<bookmark mark='a'/> What the theorem settles, and what it does not. <bookmark mark='b'/> It settles the "
            "dispute of 2016: both sides measured something real, and no score could have satisfied both. <bookmark "
            "mark='c'/> It does not say which criterion matters. That depends on the decision, on who bears each kind of "
            "error, and on whether the labels can be trusted. <bookmark mark='d'/> What a statistician owes is the full table "
            "of rates by group, with their uncertainty, and the constraints that link them.",
            [(r"the theorem:", GREY_A),
             (r"settles: \ both sides were right, \ and could not both be satisfied", S.ACCENT),
             (r"does not settle: \ which criterion, \ for which decision", GREY_A),
             (r"owed: \ every rate by group, \ with its uncertainty", OKC)])
