from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a checkout form, \ predicted", r"Which design is faster, \ before "
                     r"anyone tests it?", scale=("person", "society"))
        self.where()
        self.form()
        self.limits()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"UX research", r"interviews, \ usability tests and diary studies: \ what people try to do and where they "
                             r"fail", MODEL),
            (r"quantitative UXR", r"surveys, \ logs and experiments at scale: \ Parts 2 to 4, \ 46 and 47 in daily use",
             PERSON),
            (r"design systems", r"shared components with tested sizes, \ contrast and states, \ so every team inherits "
                                r"them", GOOD),
            (r"accessibility and data visualization", r"standards to meet, \ and charts that readers judge correctly",
             SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In UX research: interviews, usability tests and diary studies, "
           "about what people try to do and where they fail. <bookmark mark='b'/> In quantitative UX research: "
           "surveys, logs and experiments at scale, which is Parts 2 to 4, 46 and 47 in daily use. "
           "<bookmark mark='c'/> In design systems: shared components with tested sizes, contrast and states, so "
           "every team inherits them. <bookmark mark='d'/> And in accessibility and data visualization, with "
           "standards to meet and charts that readers judge correctly.", chip_w=4.4, text_w=7.8)

    def form(self):
        d = load("klm")
        head = heading(r"Two checkout forms, \ by keystroke-level model")
        A = axes([0.3, 2.7], [0, 65], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 20, 40, 60],
                 yfmt=lambda v: f"{v:.0f} s", ylabel=r"predicted time", center=[-4.0, 0.3, 0], font_size=12)
        b = bars(A.ax, [1, 2], [d["form_a"], d["form_b"]], [AUTH, GOOD], width=0.6)
        names = VGroup(*[label(s, font_size=14, color=c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, (s, c) in enumerate(zip([r"click each field", r"tab and autofill"], [AUTH, GOOD]))])
        cnt = d["counts"]
        rows = rows_of([
            (r"seven fields: \ name, \ email, \ card number, \ expiry, \ code, \ address, \ and a button", WHITE),
            (rf"design A: \ click into each field: \ {cnt['P'][0]} points, \ {cnt['H'][0]} hand moves, \ "
             rf"{cnt['M'][0]} mental operators: \ {d['form_a']:.0f} s", AUTH),
            (rf"design B: \ tab between fields, \ Enter to submit: \ {cnt['P'][1]} point, \ {cnt['H'][1]} hand move: "
             rf"\ {d['form_b']:.0f} s, \ {d['form_a'] - d['form_b']:.0f} s saved for every buyer", GOOD),
            (rf"for a fast typist the saving is {d['skilled_a'] - d['skilled_b']:.0f} s: \ the hand moves and "
             rf"thinking dominate, \ not the typing", MODEL),
            (r"the analysis took an hour, \ before any user saw either form: \ then test the winner with users, \ for "
             r"the errors the model cannot see", YOU),
        ], 7.4, 19, 0.32).move_to([2.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.klm\_time}")
        with self.voiceover(
            "Here's a worked analysis. <bookmark mark='a'/> A checkout form with seven fields: name, email, card "
            "number, expiry, code, address, and a button. <bookmark mark='b'/> Design A makes the buyer click into "
            "each field. That's nine points, fourteen hand moves and fifteen mental operators: about a minute. "
            "<bookmark mark='c'/> Design B lets them tab between fields and press Enter to submit. One point, one hand "
            "move, and about thirty-seven seconds: twenty-three seconds saved for every buyer. <bookmark mark='d'/> "
            "For a fast typist the saving is even larger, because the hand moves and the thinking dominate, not the "
            "typing. <bookmark mark='e'/> The analysis takes an hour, before any user sees either form. Then test the "
            "winner with users, for the errors the model can't see."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            for m, r in zip("de", rows[3:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def limits(self):
        rows_section(self, r"What the model leaves out", [
            (r"errors: \ a mistyped card number costs far more than any operator", AUTH),
            (r"learning: \ a first-time buyer is not a skilled user; \ the model's M's undercount their thinking", MODEL),
            (r"trust and motivation: \ whether the buyer finishes at all", PERSON),
            (r"so the model ranks designs for experts quickly, \ and a test with real users finds what it cannot", YOU),
        ], "What does the model leave out? <bookmark mark='a'/> Errors: a mistyped card number costs far more than "
           "any operator. <bookmark mark='b'/> Learning: a first-time buyer isn't a skilled user, and the model's "
           "mental operators undercount their thinking. <bookmark mark='c'/> Trust and motivation: whether the buyer "
           "finishes at all. <bookmark mark='d'/> So the model ranks designs for experts quickly, and a test with real "
           "users finds what it can't.")
