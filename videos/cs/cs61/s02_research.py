from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n) -> str:
    """A whole number as a speaker says it (British: 'one hundred and twenty-eight')."""
    n = int(round(n))
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " and " + say(n % 100))
    return say(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + say(n % 1000))


def box(text: str, color, size=18, w=None, h=0.55, fill=0.12, text_color=WHITE):
    """A rounded box with a Tex caption."""
    t = label(text, font_size=size, color=text_color)
    r = RoundedRectangle(width=w or t.width + 0.35, height=h, corner_radius=0.1, stroke_color=color,
                         stroke_width=1.8, fill_color=color, fill_opacity=fill)
    if t.width > r.width - 0.15:
        t.width = r.width - 0.15
    t.move_to(r)
    return VGroup(r, t)


def page(blocks, width=3.4, color=GREY_B, size=16):
    """A paper drawn as a page of labelled blocks; ``blocks`` is [(text, height, colour)]."""
    g = VGroup()
    for t, h, c in blocks:
        r = Rectangle(width=width - 0.3, height=h, stroke_width=0, fill_color=c, fill_opacity=0.22)
        txt = label(t, font_size=size, color=WHITE)
        if txt.width > width - 0.45:
            txt.width = width - 0.45
        g.add(VGroup(r, txt.move_to(r)))
    g.arrange(DOWN, buff=0.07)
    frame = Rectangle(width=width, height=g.height + 0.35, stroke_color=color, stroke_width=1.6, fill_color=BG,
                      fill_opacity=1).move_to(g)
    return VGroup(frame, g)


B = load("bias")


class Research(VoiceoverScene):
    def construct(self):
        self.card()
        self.question()
        self.evidence()
        self.shape()
        self.venues()
        self.ours()

    def card(self):
        card = chapter_card(1, r"What research is", r"What turns a question into a result?", lit=(1934, 1991),
                            extra=((1934, r"Popper: \ falsifiability"), (1954, r"Journal of the ACM"),
                                   (1991, r"arXiv")), part=PART)
        with self.voiceover("Chapter one. What research is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def question(self):
        head = label(r"A question that could come out wrong", font_size=36).to_edge(UP, buff=0.3)
        vague = box(r"Does the environment affect speed?", GREY_B, size=24, h=0.9)
        st = wrapped_label(r"Does growing an unused environment variable from 0 to 4{,}096 bytes move our word-count program's median "
                           r"time on this machine by more than its run-to-run noise?", 11.8, font_size=22, color=WHITE)
        sr = RoundedRectangle(width=12.4, height=st.height + 0.4, corner_radius=0.1, stroke_color=HEAD,
                              stroke_width=1.8, fill_color=HEAD, fill_opacity=0.12)
        sharp = VGroup(sr, st.move_to(sr))
        vague.move_to([0, 2.0, 0])
        sharp.move_to([0, 2.0, 0])
        tags = VGroup(label(r"which variable", font_size=17, color=DATA), label(r"which program", font_size=17,
                                                                               color=DATA),
                      label(r"which machine", font_size=17, color=DATA), label(r"compared with what", font_size=17,
                                                                              color=DATA)).arrange(RIGHT, buff=0.8)
        tags.next_to(sharp, DOWN, buff=0.2)
        steps = VGroup(box(r"hypothesis", HEAD, size=19, w=2.4), box(r"prediction", DATA, size=19, w=2.4),
                       box(r"test", KERN, size=19, w=2.4)).arrange(RIGHT, buff=0.9).move_to([-1.5, -0.6, 0])
        outs = VGroup(box(r"survives, \ for now", YES, size=18, w=2.6), box(r"refuted", NO, size=18, w=2.6)).arrange(
            DOWN, buff=0.35).next_to(steps, RIGHT, buff=0.9)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.08, color=GREY_B,
                                stroke_width=2) for i in range(2)],
                        *[Arrow(steps[2].get_right(), o.get_left(), buff=0.08, color=GREY_B, stroke_width=2)
                          for o in outs])
        back = CurvedArrow(outs[1].get_bottom() + DOWN * 0.05, steps[0].get_bottom() + DOWN * 0.05, angle=-PI / 5,
                           color=NO, stroke_width=2, tip_length=0.15)
        back_t = label(r"a better hypothesis", font_size=17, color=NO).next_to(back, DOWN, buff=0.08)
        pop = wrapped_label(r"Popper \ (1934): \ a claim is scientific if some observation could refute it", 12.4,
                            font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Research begins with a question, but not just any question. <bookmark mark='a'/> Does the environment "
            "affect speed? As asked, no experiment could ever say no. <bookmark mark='b'/> Sharpen it: which "
            "variable, which program, which machine, and compared with what. Now the answer could come out either "
            "way, and that is what makes it worth asking. <bookmark mark='c'/> A sharp question becomes a "
            "hypothesis; the hypothesis makes a prediction; and a test checks the prediction. "
            "<bookmark mark='d'/> If the test could have refuted it and did not, the hypothesis survives, for now. "
            "If it is refuted, you have learned something, and you come back with a better one. In 1934 the "
            "philosopher Karl Popper made this the mark of a scientific claim: that some observation could prove "
            "it wrong. A question whose answer you already know is not research, and neither is a claim that no "
            "result could ever contradict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(vague))
            vo.wait_until("a")
            self.play(Indicate(vague, color=GREY_A))
            vo.wait_until("b")
            self.play(ReplacementTransform(vague, sharp), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(steps[0]))
            self.play(GrowArrow(arrows[0]), FadeIn(steps[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(outs[0]))
            self.play(GrowArrow(arrows[3]), FadeIn(outs[1]))
            self.play(Create(back), FadeIn(back_t), FadeIn(pop))
        self.wait(0.4)
        self.clear_scene()

    def evidence(self):
        head = label(r"Three kinds of evidence", font_size=36).to_edge(UP, buff=0.3)
        cols = VGroup()
        for t, how, ex, chk, c in (
                (r"proof", r"a chain of steps from accepted axioms", r"Turing, \ 1936: \ the halting problem "
                 r"\ (Part 25)", r"a reader checks each step, \ or a proof assistant does \ (Part 54)", YES),
                (r"experiment", r"a controlled comparison, \ repeated", r"Mytkowicz et al., \ 2009: \ measurement "
                 r"bias \ (this part)", r"anyone reruns it, \ and gets the same answer", DATA),
                (r"construction", r"build the thing, \ and show that it works", r"Ritchie and Thompson, \ 1974: \ "
                 r"the Unix paper \ (Part 31)", r"others use it, \ and it holds up", KERN)):
            frame = RoundedRectangle(width=4.0, height=4.0, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                     fill_color=c, fill_opacity=0.06)
            body = VGroup(label(t, font_size=30, color=c),
                          wrapped_label(how, 3.6, font_size=21, color=WHITE),
                          wrapped_label(ex, 3.6, font_size=19, color=GREY_A),
                          VGroup(label(r"checked by", font_size=18, color=c),
                                 wrapped_label(chk, 3.6, font_size=20, color=WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.1)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            body.move_to(frame).align_to(frame, UP).shift(DOWN * 0.25)
            cols.add(VGroup(frame, body))
        cols.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"most papers mix them: \ a system built, \ measured, \ and a theorem about why it "
                             r"works; \ what a paper claims decides which evidence it owes", 12.4, font_size=20,
                             color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Computer science answers questions with three kinds of evidence. <bookmark mark='a'/> The first is "
            "proof: a chain of steps from accepted axioms, like Turing's proof in 1936 that no program decides "
            "halting, from Part 25. A reader checks every step, or, since Part 54, a proof assistant does. "
            "<bookmark mark='b'/> The second is experiment: a controlled comparison, repeated, like the "
            "measurement-bias study at the heart of this part. It is checked when someone else runs it again and "
            "gets the same answer. <bookmark mark='c'/> The third is construction: build the thing and show that "
            "it works, like Dennis Ritchie and Ken Thompson's 1974 paper on Unix, the system behind Part 31. It "
            "is checked when others use it and it holds up. <bookmark mark='d'/> Most papers mix the three: a "
            "system built, measured, and a theorem about why it works. What a paper claims decides which evidence "
            "it owes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, col in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(col[0]), LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in col[1]], lag_ratio=0.25),
                          run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def shape(self):
        head = label(r"The shape of a paper", font_size=36).to_edge(UP, buff=0.3)
        blocks = [(r"title, \ authors", 0.32, GREY_B), (r"abstract", 0.42, HEAD), (r"1 \ introduction", 0.62, YES),
                  (r"2 \ background", 0.38, GREY_B), (r"3 \ design \ / \ the idea", 0.62, DATA),
                  (r"4 \ evaluation \ / \ proofs", 0.72, KERN), (r"5 \ related work", 0.4, LAM),
                  (r"6 \ conclusion", 0.3, GREY_B), (r"references", 0.36, GREY_B)]
        pg = page(blocks, width=3.5, size=17).move_to([-4.4, -0.35, 0])
        parts = pg[1]
        qs = VGroup(
            box(r"Does it matter?", YES, size=20, w=3.3),
            box(r"Is it right?", KERN, size=20, w=3.3),
            box(r"Is it new?", LAM, size=20, w=3.3),
        )
        qs[0].move_to([0.6, parts[2].get_y(), 0])
        qs[1].move_to([0.6, parts[5].get_y(), 0])
        qs[2].move_to([0.6, parts[6].get_y() - 0.25, 0])
        links = VGroup(*[Arrow(q.get_left(), parts[i].get_right(), buff=0.1, color=c, stroke_width=2)
                         for q, i, c in zip(qs, (2, 5, 6), (YES, KERN, LAM))])
        side = VGroup(
            wrapped_label(r"the introduction: \ the problem, \ why it matters, \ what is new, \ and a list of "
                          r"contributions", 4.2, font_size=18, color=WHITE),
            wrapped_label(r"the evaluation or proofs: \ evidence a sceptic accepts, \ with its limits stated", 4.2,
                          font_size=18, color=WHITE),
            wrapped_label(r"related work: \ what was known, \ and exactly what this adds", 4.2, font_size=18,
                          color=WHITE),
        )
        for s, q in zip(side, qs):
            s.next_to(q, RIGHT, buff=0.35)
        abst = wrapped_label(r"the abstract in four sentences: \ the context, \ the problem, \ what we did, \ what we "
                             r"found", 4.2, font_size=18, color=HEAD)
        abst.next_to(VGroup(qs[0], side[0]), UP, buff=0.4).align_to(qs, LEFT)
        with self.voiceover(
            "Results travel as papers, and papers have a shape. <bookmark mark='a'/> A title and authors; an "
            "abstract; an introduction; background; the idea or design; the evaluation, or the proofs; related "
            "work; a conclusion; and references. The order varies by field, but the parts recur. "
            "<bookmark mark='b'/> The abstract tells the whole story in about four sentences: the context, the "
            "problem, what we did, and what we found. <bookmark mark='c'/> Each remaining part answers one of the "
            "three questions every reader, and every reviewer, asks. Does it matter? That is the introduction's "
            "job: the problem, why it matters, and a list of contributions. <bookmark mark='d'/> Is it right? "
            "That is the evaluation or the proofs, with their limits stated. <bookmark mark='e'/> Is it new? That "
            "is related work: what was already known, and exactly what this paper adds. Chapter six reads papers "
            "with these questions in mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pg[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in parts], lag_ratio=0.25), run_time=3)
            vo.wait_until("b")
            self.play(Indicate(parts[1], color=HEAD), FadeIn(abst))
            for mk, i in zip("cde", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(qs[i]), GrowArrow(links[i]), FadeIn(side[i]))
        self.wait(0.4)
        self.clear_scene()

    def venues(self):
        head = label(r"Conferences and journals", font_size=36).to_edge(UP, buff=0.3)

        def lane(items, color, y):
            g = VGroup(*[box(t, color, size=19, h=0.62) for t in items]).arrange(RIGHT, buff=0.32)
            g.move_to([0.6, y, 0])
            arr = VGroup(*[Arrow(g[i].get_right(), g[i + 1].get_left(), buff=0.04, color=GREY_B, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.35) for i in range(len(g) - 1)])
            return VGroup(g, arr)
        conf = lane([r"deadline", r"3+ reviews", r"rebuttal", r"accept \ / \ reject", r"talk, \ proceedings"], DATA,
                    1.75)
        jour = lane([r"submit any time", r"reviews", r"revise", r"reviews", r"revise", r"accept"], LAM, 0.25)
        cl = VGroup(label(r"conference", font_size=22, color=DATA), label(r"a few months", font_size=17,
                                                                          color=GREY_A)).arrange(DOWN, buff=0.06)
        jl = VGroup(label(r"journal", font_size=22, color=LAM), label(r"months to years", font_size=17,
                                                                     color=GREY_A)).arrange(DOWN, buff=0.06)
        cl.next_to(conf, LEFT, buff=0.3)
        jl.next_to(jour, LEFT, buff=0.3)
        for lb, ln in ((cl, conf), (jl, jour)):
            if lb.get_left()[0] < -6.8:
                VGroup(lb, ln).shift(RIGHT * (-6.8 - lb.get_left()[0]))
        firsts = VGroup(
            wrapped_label(r"in computer science the selective conferences are the main venue: \ SOSP \ (since "
                          r"1967), \ STOC \ (1969), \ POPL \ (1973); \ many accept fewer than one paper in four", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"journals \ (the \textit{Journal of the ACM}, \ since 1954) \ carry longer, \ fuller "
                          r"versions; \ preprints go to arXiv \ (since 1991) \ first", 12.4, font_size=19,
                          color=GREY_A),
            wrapped_label(r"Fortnow \ (2009): \ ``time for computer science to grow up'', \ back toward journals; \ "
                          r"the debate continues", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where do papers go? In most sciences, to journals. Computer science is unusual. "
            "<bookmark mark='a'/> Its main venues are selective conferences. A paper meets a fixed deadline, is "
            "read by three or more members of a programme committee, the authors may answer in a short rebuttal, "
            "and within a few months it is accepted or rejected, then presented in a talk and printed in the "
            "proceedings. <bookmark mark='b'/> Many have long histories: the Symposium on Operating Systems "
            "Principles since 1967, the theory symposium STOC since 1969, and the programming-languages symposium "
            "POPL since 1973; many accept fewer than one paper in four. <bookmark mark='c'/> Journals work "
            "differently: submit any time, and go through rounds of review and revision that can take months or "
            "years. In computer science they often hold the longer, fuller version of a conference paper, and "
            "preprints appear on arXiv first. <bookmark mark='d'/> In 2009 Lance Fortnow argued that the field "
            "should grow up and move back toward journals. The debate continues."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in conf[0]], lag_ratio=0.35),
                      Create(conf[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(firsts[0]))
            vo.wait_until("c")
            self.play(FadeIn(jl), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in jour[0]], lag_ratio=0.35),
                      Create(jour[1]), run_time=3)
            self.play(FadeIn(firsts[1]))
            vo.wait_until("d")
            self.play(FadeIn(firsts[2]))
        self.wait(0.4)
        self.clear_scene()

    def ours(self):
        head = label(r"This part's experiment, \ as a paper", font_size=36).to_edge(UP, buff=0.3)
        reps, sizes, link_runs = B["reps"], len(B["env"]), len(B["link"][0]["runs"])
        secs = [
            (r"question", rf"does an unused environment variable, \ 0 to 4{{,}}096 bytes, \ or the link order, \ "
                          r"change the time of one C program on this machine?", HEAD),
            (r"method", rf"{sizes} sizes $\times$ {reps} runs, \ interleaved; \ {len(B['link'])} link orders "
                        rf"$\times$ {link_runs} runs; \ medians compared with the run-to-run noise", DATA),
            (r"evidence", rf"medians spread {100 * B['env_spread']:.1f}\% across sizes, \ "
                          rf"{100 * B['link_spread']:.1f}\% across link orders; \ both within the noise", YES),
            (r"threats to validity", r"a shared machine; \ one program, \ one compiler; \ address randomization "
                                     r"on", NO),
            (r"conclusion", r"no effect shown here: \ which is not the same as no effect", LAM),
        ]
        rows = VGroup()
        for t, body, c in secs:
            tl = label(t, font_size=23, color=c)
            bl = wrapped_label(body, 9.0, font_size=22, color=WHITE)
            rows.add(VGroup(tl, bl))
        for r in rows:
            r[0].move_to([-6.6, 0, 0], aligned_edge=LEFT)
            r[1].next_to([-3.6, 0, 0], RIGHT, buff=0).align_to(r[0], UP)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([0, -0.25, 0])
        for r in rows:
            r[1].set_x(-3.6 + r[1].width / 2)
            r[0].set_x(-6.6 + r[0].width / 2)
        rules = VGroup(*[Line([-6.6, r.get_bottom()[1] - 0.2, 0], [6.6, r.get_bottom()[1] - 0.2, 0], color=GREY_D,
                              stroke_width=1) for r in rows[:-1]])
        with self.voiceover(
            "Here is this part's own experiment, written as a paper would be. <bookmark mark='a'/> The question: "
            "does an unused environment variable, or the order of linking, change the time of one C program on "
            f"this machine? <bookmark mark='b'/> The method: {say(sizes)} sizes, {say(reps)} runs each, "
            f"interleaved; {say(len(B['link']))} link orders, {say(link_runs)} runs each; medians compared with "
            "the run-to-run noise. <bookmark mark='c'/> The evidence: the medians spread by about "
            f"{say(100 * B['env_spread'])} percent across sizes and under one percent across link orders, both "
            "within the noise. <bookmark mark='d'/> Threats to validity, the section honest papers never skip: a "
            "shared machine, one program, one compiler, and address randomization switched on. "
            "<bookmark mark='e'/> The conclusion: no effect shown here, which is not the same as no effect. The "
            "next chapter takes that experiment apart."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r, i in zip("abcde", rows, range(5)):
                vo.wait_until(mk)
                anims = [FadeIn(r[0], shift=RIGHT * 0.15), FadeIn(r[1])]
                if i:
                    anims.append(Create(rules[i - 1]))
                self.play(*anims)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, NO)
