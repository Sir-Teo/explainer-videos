from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Redish(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.computed()
        self.test()

    def card(self):
        card = chapter_card(8, r"Addiction as learning gone wrong", r"What if a reward can never be predicted away?",
                            lit={2004: r"Redish", 2007: r"Panlilio et al."}, part=PART, scale=("circuit",),
                            marr=("what", "how"))
        with self.voiceover("Chapter eight. Addiction as learning gone wrong."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def idea(self):
        head = heading(r"An error that never goes away")
        eq1 = MathTex(r"\delta = r - V", font_size=40, color=GOOD)
        eq2 = MathTex(r"\delta = \max(r - V + D,\; D)", font_size=40, color=AUTH)
        l1 = label(r"a natural reward: \ the error shrinks to zero as $V$ learns $r$", font_size=18, color=GOOD)
        l2 = label(r"a drug, \ in Redish's model: \ the surge $D$ keeps the error at least $D$", font_size=18,
                   color=AUTH)
        g = VGroup(VGroup(eq1, l1).arrange(DOWN, buff=0.2), VGroup(eq2, l2).arrange(DOWN, buff=0.2)).arrange(
            DOWN, buff=0.6).move_to([0, 1.1, 0])
        rows = rows_of([
            (r"Part 17: \ learning stops when a reward is fully predicted, \ because the prediction error falls to "
             r"zero", WHITE),
            (r"Redish, \ 2004: \ a drug that releases dopamine directly adds a surge $D$ that no prediction can "
             r"cancel", AUTH),
            (r"so the value of taking the drug keeps rising, \ with every use, \ without limit", YOU),
        ], 12.4, 22, 0.4).move_to([0, -1.9, 0])
        tag = published_tag(r"Redish (2004)")
        with self.voiceover(
            "Now put the drug into Part 17's learning rule. <bookmark mark='a'/> For a natural reward, learning stops "
            "when the reward is fully predicted, because the prediction error falls to zero. "
            "<bookmark mark='b'/> In 2004 David Redish proposed that a drug which releases dopamine directly adds a "
            "surge that no prediction can cancel. The error never falls below it. <bookmark mark='c'/> So the value "
            "of taking the drug keeps rising, with every use, without limit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(g[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def computed(self):
        d = load("redish")
        head = heading(r"The model, \ computed")
        n = len(d["natural"])
        A = axes([0, n], [-0.5, 7], x_length=5.8, y_length=3.4, xticks=[0, 100, 200, 300], yticks=[0, 2, 4, 6],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"uses", ylabel=r"learned value $V$",
                 center=[-3.2, 0.3, 0], font_size=13)
        t = np.arange(n)
        nat = curve(A.ax, t, d["natural"], GOOD, stroke_width=3)
        natc = curve(A.ax, t, d["natural_cost"], GREY_B, stroke_width=2)
        drug = curve(A.ax, t, d["drug"], AUTH, stroke_width=3)
        drugc = DashedVMobject(curve(A.ax, t, d["drug_cost"], PERSON, stroke_width=3), num_dashes=40)
        key = VGroup(label(r"natural reward 1", font_size=13, color=GOOD),
                     label(r"natural reward 1, \ cost 1", font_size=13, color=GREY_B),
                     label(r"drug: \ reward 0.5, \ surge 0.2", font_size=13, color=AUTH),
                     label(r"drug with a cost of 1", font_size=13, color=PERSON)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08)
        key.next_to(A, DOWN, buff=0.3)
        rows = rows_of([
            (r"Psyche, \ one TD learner: \ a natural reward's value settles at the reward", GOOD),
            (r"add a cost as large as the reward, \ and its value settles at zero: \ the behaviour stops", GREY_A),
            (rf"the drug's value passes the natural reward's and keeps climbing: \ {d['drug'][-1]:.1f} after "
             rf"{n} uses", AUTH),
            (rf"add the same cost to the drug: \ it still climbs, \ to {d['drug_cost'][-1]:.1f}; \ punishment cannot "
             rf"teach it to stop", PERSON),
        ], 5.8, 19, 0.36).move_to([3.5, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.redish}; \ after Redish (2004)")
        with self.voiceover(
            "Psyche runs it on one learner. <bookmark mark='a'/> A natural reward's value settles at the reward. "
            "<bookmark mark='b'/> Add a cost as large as the reward, and its value settles at zero. The behaviour "
            "stops. <bookmark mark='c'/> The drug's value passes the natural reward's and keeps climbing, use after "
            "use. <bookmark mark='d'/> Add the same cost to the drug, and it still climbs. In this model, punishment "
            "can't teach the learner to stop. That matches one hallmark of addiction: use that continues despite "
            "harm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(nat), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(natc), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(drug), FadeIn(key[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(drugc), FadeIn(key[3]), run_time=2.0)
        self.clear_scene()

    def test(self):
        head = heading(r"A prediction, \ tested")
        rows = rows_of([
            (r"the model makes a sharp prediction: \ since the drug's error never reaches zero, \ a drug reward "
             r"should never be ``blocked'' (Part 16), \ because it always teaches something new", MODEL),
            (r"Panlilio and colleagues, \ 2007: \ in rats self-administering cocaine, \ blocking happened anyway", AUTH),
            (r"so the simplest version fails; \ later models add habits, \ multiple learning systems and changes "
             r"with use", WHITE),
            (r"what survives: \ addiction as a learning system the drug exploits, \ with predictions that can be "
             r"tested and fail", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Panlilio et al.\ (2007)")
        with self.voiceover(
            "A good model makes predictions that could fail, and this one did. <bookmark mark='a'/> Since the drug's "
            "prediction error never reaches zero, a drug reward should never be blocked, Part 16's effect, because it "
            "always teaches something new. <bookmark mark='b'/> In 2007 Leigh Panlilio and colleagues tested this in "
            "rats self-administering cocaine. Blocking happened anyway. <bookmark mark='c'/> So the simplest version "
            "fails, and later models add habits, multiple learning systems, and changes that build with use. "
            "<bookmark mark='d'/> What survives is addiction as a learning system that a drug exploits, described in "
            "models precise enough to be tested, and to fail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
