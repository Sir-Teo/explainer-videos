from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Exposure(VoiceoverScene):
    def construct(self):
        self.card()
        self.renewal()
        self.principles()
        self.contexts()

    def card(self):
        card = chapter_card(3, r"Exposure, \ and the return of fear", r"Is extinction forgetting?",
                            lit={2002: r"Bouton", 2014: r"Craske et al."}, part=PART, scale=("circuit", "person"),
                            marr=("how",))
        with self.voiceover("Chapter three. Exposure, and the return of fear."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def renewal(self):
        d = load("renewal")
        head = heading(r"Extinction is new learning")
        tr = np.asarray(d["trace"], float)
        n = len(tr)
        A = axes([0, n + 10], [0, 1.05], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"fear", center=[-3.2, 0.3, 0], font_size=14)
        line = curve(A.ax, np.arange(n), tr, PERSON, stroke_width=4)
        zones = VGroup()
        for x0, x1, name, c in ((0, 15, r"context A: \ shocks", AUTH), (15, n, r"context B: \ no shocks", GOOD)):
            r = Rectangle(width=abs(A.ax.c2p(x1, 0)[0] - A.ax.c2p(x0, 0)[0]), height=3.0, stroke_width=0,
                          fill_color=c, fill_opacity=0.08).move_to([(A.ax.c2p(x0, 0)[0] + A.ax.c2p(x1, 0)[0]) / 2,
                                                                  A.ax.c2p(0, 0.5)[1], 0])
            zones.add(VGroup(r, label(name, font_size=12, color=c).next_to(r, UP, buff=0.05)))
        tests = VGroup()
        for k, (ctx, c) in enumerate((("B", GOOD), ("A", AUTH), ("C", MODEL))):
            v = float(d[ctx])
            tests.add(VGroup(Dot(A.ax.c2p(n + 3 + 3 * k, v), radius=0.09, color=c),
                             label(ctx, font_size=14, color=c).next_to(A.ax.c2p(n + 3 + 3 * k, v), UP, buff=0.1)))
        lt = label(r"tests", font_size=13, color=GREY_A).next_to(A.ax.c2p(n + 6, 0), DOWN, buff=0.15)
        rows = rows_of([
            (r"Bouton, \ 2002: \ extinction does not erase the fear; \ it adds a second, \ inhibitory memory, \ "
             r"tied to the context where it was learned", WHITE),
            (r"Psyche: \ fear learned in context A, \ extinguished in context B", MODEL),
            (r"tested in B, \ no fear; \ back in A, \ or in a new place C, \ the fear returns: \ renewal", AUTH),
            (r"fear also comes back with time (spontaneous recovery) and after a single shock (reinstatement); \ "
             r"relapse after therapy is the rule these predict", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.renewal}; \ Bouton (2002)")
        with self.voiceover(
            "If exposure works, why does fear come back? <bookmark mark='a'/> Mark Bouton's answer: extinction "
            "doesn't erase the fear. It adds a second, inhibitory memory, and that memory is tied to the context "
            "where it was learned. <bookmark mark='b'/> In Psyche, fear is learned in context A and extinguished in "
            "context B. <bookmark mark='c'/> Tested in B, no fear. Back in A, or in a new place, C, the fear "
            "returns. That's renewal. <bookmark mark='d'/> Fear also comes back with time, spontaneous recovery, and "
            "after a single shock, reinstatement. Relapse after therapy is what these predict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zones))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(line), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(x, scale=1.4) for x in tests], lag_ratio=0.5),
                      FadeIn(lt))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def principles(self):
        head = heading(r"Making exposure last")
        items = [
            (r"violate expectations", r"design each exposure to test a specific feared outcome, \ and let it not "
                                      r"happen", GOOD),
            (r"vary the contexts", r"practise in many places, \ so the new learning is not tied to the clinic", SYMP),
            (r"drop safety behaviours", r"carrying a pill or a phone to call for help is a small avoidance", PERSON),
            (r"retrieval cues", r"reminders of what was learned, \ carried back into the old contexts", MODEL),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=18, width=3.6), wrapped_label(how, 8.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.0, 0])
        foot = wrapped_label(r"Craske and colleagues, \ 2014: \ an inhibitory-learning approach to exposure; \ "
                             r"exposure-based treatments are among the best-supported in psychology",
                             12.0, 19, GREY_A).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Craske et al.\ (2014)")
        with self.voiceover(
            "If extinction is new learning, it can be learned better. <bookmark mark='a'/> Michelle Craske and "
            "colleagues set out the principles. Design each exposure to test a specific feared outcome, and let it "
            "not happen. <bookmark mark='b'/> Practise in many places, so the new learning isn't tied to the clinic. "
            "<bookmark mark='c'/> Drop safety behaviours: carrying a pill, or a phone to call for help, is a small "
            "avoidance. <bookmark mark='d'/> And use retrieval cues that carry what was learned back into the old "
            "contexts. Exposure-based treatments are among the best-supported in all of psychology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(foot))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def contexts(self):
        d = load("contexts")
        head = heading(r"Many places, \ computed")
        n = np.asarray(d["n"], float)
        A = axes([0.4, 6.6], [0, 1.0], x_length=5.4, y_length=3.0, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"contexts used for extinction",
                 ylabel=r"fear in a new place", center=[-3.3, 0.5, 0], font_size=13)
        b = bars(A.ax, n, d["fear"], [AUTH] + [GOOD] * 5, width=0.6)
        eq = MathTex(r"\text{fear}_{\text{new}} = E - \big(1 - (1 - s)^n\big)\, I", font_size=30,
                     color=MODEL).move_to([-3.3, -2.3, 0])
        rows = rows_of([
            (r"Psyche: \ the inhibition learned in extinction is tied to a context's features, \ and a new place "
             r"shares a quarter of its features with each extinction context", WHITE),
            (rf"extinguished in one place, \ fear in a new one is {d['fear'][0]:.2f} of its peak", AUTH),
            (rf"spread over six places, \ it is {d['fear'][-1]:.2f}: \ each new place retrieves more of what was "
             rf"learned", GOOD),
            (r"a toy model of Craske's second principle; \ trials that vary the setting of exposure test it in "
             r"people", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.renewal\_contexts}")
        with self.voiceover(
            "Psyche can test the second principle. <bookmark mark='a'/> Suppose the inhibition learned in extinction "
            "is tied to a context's features, and any new place shares a quarter of its features with each place "
            "where extinction happened. <bookmark mark='b'/> Extinguished in one place, the fear in a new one comes "
            "back at about three quarters of its peak. <bookmark mark='c'/> Spread over six places, it comes back at "
            "under a fifth. Each new place retrieves more of what was learned. <bookmark mark='d'/> It's a toy model "
            "of Craske's second principle, and trials that vary the setting of exposure test it in people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(x) for x in b[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
