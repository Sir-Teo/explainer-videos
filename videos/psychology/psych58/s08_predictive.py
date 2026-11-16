from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Predictive(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Predictive coding", r"Does the cortex send its predictions down?", scale=("brain",),
                     marr=("how",))
        self.rao()
        self.errors()
        self.evidence()

    def rao(self):
        rows_section(self, r"Predictions down, \ errors up", [
            (r"Rao and Ballard, \ 1999: \ a hierarchy where each level predicts the activity of the level below", WHITE),
            (r"what goes up is only the error: \ the part of the input the prediction did not explain", MODEL),
            (r"each level adjusts its causes to shrink the errors, \ above and below: \ inference by gradient "
             r"descent", PERSON),
            (r"it explained end-stopping: \ a cell that stops firing when a line extends past its field, \ because "
             r"long lines are predicted from above", GOOD),
            (r"the same idea as efficient coding: \ do not send what the receiver can already predict", YOU),
        ], "Does the cortex send its predictions down? <bookmark mark='a'/> In 1999 Rajesh Rao and Dana Ballard "
           "built a hierarchy where each level predicts the activity of the level below. <bookmark mark='b'/> What "
           "goes up is only the error: the part of the input the prediction didn't explain. <bookmark mark='c'/> "
           "Each level adjusts its causes to shrink the errors above and below it. That's inference by gradient "
           "descent. <bookmark mark='d'/> It explained end-stopping: cells that stop firing when a line extends past "
           "their field, because long lines are predicted from above. <bookmark mark='e'/> It's the same idea as "
           "efficient coding: don't send what the receiver can already predict.",
           tag=published_tag(r"Rao \& Ballard (1999)"))

    def errors(self):
        d = load("pc")
        head = heading(r"Error units, \ expected and surprising")
        n = len(d["exp_e0"])
        t = np.arange(n)
        A = axes([0, n], [0, 6.2], x_length=5.6, y_length=3.2, xticks=[0, 20, 40, 60], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"settling steps",
                 ylabel=r"error activity", center=[-3.3, 0.2, 0], font_size=12)
        ce = curve(A.ax, t, d["exp_e0"], GOOD, stroke_width=4)
        cs = curve(A.ax, t, d["sur_e0"], AUTH, stroke_width=4)
        cp = curve(A.ax, t, d["sur_e1"], MODEL, stroke_width=3)
        key = VGroup(label(r"expected input", font_size=13, color=GOOD),
                     label(r"surprising input", font_size=13, color=AUTH),
                     label(r"its prior error", font_size=13, color=MODEL)).arrange(RIGHT, buff=0.35)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Psyche's two-level network: \ 16 inputs, \ 4 causes, \ a prior on the causes", WHITE),
            (r"an expected input: \ the error units barely respond", GOOD),
            (r"a surprising one: \ a burst of error that the causes absorb as they settle", AUTH),
            (r"what remains is a disagreement with the prior: \ the network has learned something", MODEL),
            (r"the prediction for physiology: \ responses to the expected are suppressed, \ to the unexpected "
             r"enhanced", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{efficient.predictive\_coding}")
        with self.voiceover(
            "Here's the loop, small enough to watch. <bookmark mark='a'/> Psyche's two-level network has sixteen "
            "inputs, four causes, and a prior on the causes. <bookmark mark='b'/> Give it an expected input, and the "
            "error units barely respond. <bookmark mark='c'/> Give it a surprising one, and there's a burst of error "
            "that the causes absorb as they settle. <bookmark mark='d'/> What remains is a disagreement with the "
            "prior. The network has learned something. <bookmark mark='e'/> So the prediction for physiology is that "
            "responses to the expected are suppressed, and responses to the unexpected are enhanced."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(ce))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(cs), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(cp))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def evidence(self):
        chips_section(self, r"What the evidence supports", [
            (r"supported", r"expected stimuli evoke smaller responses: \ repetition suppression, \ the mismatch "
                           r"negativity (Part 15), \ omission responses", GOOD),
            (r"supported", r"mouse V1 responds to mismatches between running and visual flow (Keller and colleagues, "
                           r"\ 2012)", GOOD),
            (r"contested", r"separate error and prediction neurons, \ in separate layers, \ as the scheme requires: \ "
                           r"evidence is patchy", AUTH),
            (r"the catch", r"suppression of the expected is also predicted by adaptation and by attention, \ so "
                           r"it cannot single out predictive coding", PERSON),
        ], "What does the evidence support? <bookmark mark='a'/> Expected stimuli evoke smaller responses: "
           "repetition suppression, the mismatch negativity from Part 15, and responses to omitted stimuli. "
           "<bookmark mark='b'/> Mouse primary visual cortex responds to mismatches between running and visual flow, "
           "as Georg Keller and colleagues found in 2012. <bookmark mark='c'/> Contested: separate error neurons and "
           "prediction neurons, in separate layers, as the scheme requires. The evidence is patchy. "
           "<bookmark mark='d'/> And the catch: suppression of the expected is also predicted by adaptation and by "
           "attention, so on its own it can't single out predictive coding.", chip_w=3.0, text_w=9.0)
