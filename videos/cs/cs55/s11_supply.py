from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, mono, tag_box


def cbox(text, color, w=None, h=0.5, size=18, use_mono=False, fill=0.0):
    """A labelled rounded box (Tex, or monospace with ``use_mono``)."""
    t = mono(text, size=size, color=WHITE) if use_mono else label(text, font_size=size, color=WHITE)
    w = w or t.width + 0.35
    r = RoundedRectangle(width=w, height=h, corner_radius=0.07, stroke_color=color, stroke_width=1.8,
                         fill_color=color if fill else BG, fill_opacity=fill if fill else 1)
    if t.width > w - 0.12:
        t.width = w - 0.12
    t.move_to(r)
    return VGroup(r, t)


def arrow(a, b, color=GREY_B, width=2.4):
    return Arrow(a, b, buff=0.06, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.18,
                 max_stroke_width_to_length_ratio=10)


class Supply(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.confusion()
        self.solarwinds()
        self.xz()
        self.slowdown()
        self.defences()

    def card(self):
        card = chapter_card(10, r"Supply chains", r"Who else wrote the code you run?", lit=(2020, 2021, 2024),
                            extra=((2020, r"SolarWinds"), (2021, r"dependency confusion"), (2024, r"xz-utils")),
                            part=PART, layers=("practice", "apps"))
        with self.voiceover("Chapter ten. Supply chains."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        head = label(r"The code you did not write", font_size=36).to_edge(UP, buff=0.3)
        root = tag_box("app", HEAD, size=18).move_to([-3.6, 2.15, 0])
        lv1 = VGroup(*[tag_box(n, DATA, size=17) for n in ("web", "db", "log")]).arrange(RIGHT, buff=0.9)
        lv1.move_to([-3.6, 1.05, 0])
        lv2 = VGroup(*[tag_box(n, LAM, size=16) for n in ("http", "tls", "pool", "sql", "fmt", "time")])
        lv2.arrange(RIGHT, buff=0.2).move_to([-3.6, -0.05, 0])
        lv3 = VGroup(*[Dot(radius=0.09, color=GREY_B) for _ in range(12)]).arrange(RIGHT, buff=0.33)
        lv3.move_to([-3.6, -1.0, 0])
        e1 = VGroup(*[Line(root.get_bottom(), c.get_top(), color=GREY_D, stroke_width=1.5) for c in lv1])
        e2 = VGroup(*[Line(lv1[k // 2].get_bottom(), c.get_top(), color=GREY_D, stroke_width=1.5)
                      for k, c in enumerate(lv2)])
        e3 = VGroup(*[Line(lv2[k // 2].get_bottom(), c.get_top(), color=GREY_D, stroke_width=1.2)
                      for k, c in enumerate(lv3)])
        bad = lv3[7]
        cnt = label(r"$1 + 3 + 6 + 12$ packages: \ $n = 22$", font_size=19, color=GREY_A).next_to(lv3, DOWN,
                                                                                                 buff=0.3)
        ill = label(r"an illustrative tree", font_size=16, color=GREY_B).next_to(cnt, DOWN, buff=0.12)
        eqs = [MathTex(r"P", r"=", r"(1-p)^{n}", font_size=40),
               MathTex(r"\ln", r"P", r"=", r"n", r"\ln(1-p)", font_size=40),
               MathTex(r"\ln", r"P", r"\approx", r"-", r"n", r"p", font_size=40),
               MathTex(r"P", r"\approx", r"e^{-np}", font_size=40)]
        for e in eqs:
            e.move_to([3.6, 1.6, 0])
        whys = [label(r"each package independently clean, \ with probability $1-p$", font_size=19, color=GREY_A),
                label(r"take logarithms", font_size=19, color=GREY_A),
                label(r"$\ln(1-p) \approx -p$ \ for small $p$", font_size=19, color=GREY_A),
                label(r"the chance that \textit{nothing} in the tree is bad", font_size=19, color=HEAD)]
        for w in whys:
            w.move_to([3.6, 0.75, 0])
        ex = MathTex(r"n = 1000,\ \ p = 10^{-4}:", r"\quad", r"P \approx e^{-0.1} \approx 0.90", font_size=32,
                     color=NO).move_to([3.6, -0.3, 0])
        exn = label(r"illustrative numbers", font_size=16, color=GREY_B).next_to(ex, DOWN, buff=0.15)
        foot = wrapped_label(r"the risk grows with $n$, \ the number of strangers you trust, \ and it is decided by the "
                             r"least careful of them", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A program trusts far more than its compiler. <bookmark mark='a'/> It names three dependencies; they "
            "name six more; those name twelve, each written by a stranger and running with your program's "
            "authority. <bookmark mark='b'/> If each is clean with probability one minus p, independently, all n "
            "are clean with probability one minus p to the n. <bookmark mark='c'/> Take logarithms; "
            "<bookmark mark='d'/> for small p, the log of one minus p is about minus p, <bookmark mark='e'/> so "
            "the chance that nothing is bad is about e to the minus n p. <bookmark mark='f'/> A thousand packages, "
            "one bad in ten thousand: a one in ten chance of trouble, set by the least careful stranger."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root))
            vo.wait_until("a")
            self.play(Create(e1), FadeIn(lv1))
            self.play(Create(e2), FadeIn(lv2))
            self.play(Create(e3), FadeIn(lv3), FadeIn(cnt), FadeIn(ill))
            vo.wait_until("b")
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(eqs[0], eqs[1]), FadeTransform(whys[0], whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(eqs[1], eqs[2]), FadeTransform(whys[1], whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(eqs[2], eqs[3]), FadeTransform(whys[2], whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(ex), FadeIn(exn), bad.animate.set_color(NO).scale(1.6))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def confusion(self):
        head = label(r"Dependency confusion \ (Birsan, \ 2021)", font_size=36).to_edge(UP, buff=0.3)
        priv = VGroup(label(r"the company's private registry", font_size=19, color=YES),
                      tag_box("acme-billing 1.4.2", YES, size=18)).arrange(DOWN, buff=0.2).move_to([-3.8, 1.7, 0])
        pub = VGroup(label(r"the public registry", font_size=19, color=GREY_A),
                     tag_box("acme-billing 99.0.0", NO, size=18)).arrange(DOWN, buff=0.2).move_to([3.8, 1.7, 0])
        inst = cbox(r"installer: \ ``the highest version of \texttt{acme-billing}, \ from any registry''", KERN,
                    w=8.4, h=0.62, size=19).move_to([0, -0.2, 0])
        a1 = arrow(priv[1].get_bottom(), inst.get_top() + LEFT * 2.2, YES)
        a2 = arrow(pub[1].get_bottom(), inst.get_top() + RIGHT * 2.2, NO, width=5)
        pick = label(r"$99.0.0 > 1.4.2$: \ the stranger's package wins, \ and its install script runs on the "
                     r"build machine", font_size=20, color=NO).next_to(inst, DOWN, buff=0.35)
        ill = label(r"an illustrative package name", font_size=16, color=GREY_B).next_to(pub, UP, buff=0.12)
        fixes = wrapped_label(r"fixes: \ private names in a namespace the company owns; \ each name bound to one "
                              r"registry; \ lockfiles that pin every package by its hash \ (Part 41's content "
                              r"addressing)", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2021 Alex Birsan turned a resolver's own rules against it. <bookmark mark='a'/> Companies keep "
            "internal packages in a private registry, under names that leak in public code. <bookmark mark='b'/> "
            "Publish the same name on the public registry with a higher version, <bookmark mark='c'/> and an "
            "installer that looks in both takes the highest, wherever it lives; the stranger's install script runs "
            "inside the company. He reached dozens of companies, and reported it to them. <bookmark mark='d'/> The "
            "fixes are names and hashes: a namespace you own, one registry per name, and every package pinned by "
            "its content hash, Part 41's lockfile."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(priv), FadeIn(inst), GrowArrow(a1))
            vo.wait_until("b")
            self.play(FadeIn(pub), FadeIn(ill))
            vo.wait_until("c")
            self.play(GrowArrow(a2), inst[0].animate.set_stroke(NO))
            self.play(FadeIn(pick), a1.animate.set_opacity(0.3))
            vo.wait_until("d")
            self.play(FadeIn(fixes))
        self.wait(0.4)
        self.clear_scene()

    def solarwinds(self):
        head = label(r"Poisoning the build \ (SolarWinds, \ 2020)", font_size=36).to_edge(UP, buff=0.3)
        names = [r"source repository", r"build server", r"code signing", r"update server", r"customers"]
        boxes = VGroup(*[cbox(n, GREY_B, w=2.2, h=0.66, size=18) for n in names]).arrange(RIGHT, buff=0.42)
        boxes.move_to([0, 0.9, 0])
        arrs = VGroup(*[arrow(boxes[i].get_right(), boxes[i + 1].get_left()) for i in range(4)])
        status = [(r"clean", YES), (r"backdoor inserted \\ during each build", NO), (r"valid signature", HEAD),
                  (r"a routine update", GREY_A), (r"installed by thousands", NO)]
        chips = VGroup()
        for bx, (t, c) in zip(boxes, status):
            chips.add(Tex(r"\begin{tabular}{c}" + t + r"\end{tabular}", font_size=18, color=c).next_to(bx, DOWN,
                                                                                                     buff=0.25))
        inj = Arrow(boxes[1].get_top() + UP * 1.0, boxes[1].get_top(), buff=0.05, color=NO, stroke_width=4,
                    max_tip_length_to_length_ratio=0.25)
        injl = label(r"attackers inside the build environment", font_size=18, color=NO).next_to(inj, UP, buff=0.08)
        facts = VGroup(
            wrapped_label(r"disclosed December 2020; \ found by the security firm FireEye, \ investigating a breach of "
                          r"its own", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"SolarWinds told regulators that fewer than 18,000 customers had installed the affected "
                          r"Orion updates", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"a signature says \textit{who} built a binary, \ not \textit{what source} it was built "
                          r"from: \ Thompson's point, \ at industrial scale", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(chips, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "The build is another way in. <bookmark mark='a'/> SolarWinds sells Orion, software that monitors "
            "networks and so is trusted with them. <bookmark mark='b'/> Attackers inside its "
            "build environment made the build insert a backdoor as it ran, so the source repository stayed clean, "
            "<bookmark mark='c'/> and every binary was then signed with the company's own key and shipped as a "
            "routine update. <bookmark mark='d'/> When it was disclosed in December 2020, found by FireEye while "
            "investigating a breach of its own, SolarWinds put the number of customers who had installed it at "
            "fewer than eighteen thousand. <bookmark mark='e'/> The signature was genuine. It said who built the "
            "binary, not what it was built from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), *[GrowArrow(a) for a in arrs])
            vo.wait_until("a")
            self.play(boxes[4][0].animate.set_stroke(DATA))
            vo.wait_until("b")
            self.play(GrowArrow(inj), FadeIn(injl), boxes[1][0].animate.set_stroke(NO), FadeIn(chips[0]),
                      FadeIn(chips[1]))
            vo.wait_until("c")
            self.play(FadeIn(chips[2]), FadeIn(chips[3]), boxes[2][0].animate.set_stroke(HEAD))
            vo.wait_until("d")
            self.play(FadeIn(chips[4]), FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("e")
            self.play(FadeIn(facts[2]))
        self.wait(0.4)
        self.clear_scene()

    def xz(self):
        head = label(r"The xz-utils backdoor \ (2024)", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -6.0, 6.0, 2.15

        def X(t):
            return x0 + (t - 2021.0) / (2024.4 - 2021.0) * (x1 - x0)
        spine = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(t), y - 0.07, 0], [X(t), y + 0.07, 0], color=GREY_C),
                                label(str(t), font_size=17, color=GREY_B).next_to([X(t), y, 0], UP, buff=0.1))
                         for t in (2021, 2022, 2023, 2024)])
        ev = [(2021.75, r"a newcomer starts sending patches", GREY_A),
              (2022.5, r"2022--23: \ other accounts press the lone volunteer maintainer; \ the newcomer becomes a co-maintainer",
               KERN),
              (2024.15, r"releases 5.6.0 and 5.6.1 carry the backdoor", NO)]
        evs = VGroup()
        for k, (t, txt, c) in enumerate(ev):
            d = Dot([X(t), y, 0], radius=0.08, color=c)
            w = wrapped_label(txt, (2.6, 3.4, 3.4)[k], font_size=18, color=c).next_to(d, DOWN, buff=0.2)
            if k == 0:
                w.align_to(d, RIGHT)
            elif k == 1:
                w.align_to(d, LEFT).shift(LEFT * 0.1)
            else:
                w.align_to([6.8, 0, 0], RIGHT)
            evs.add(VGroup(d, w))
        steps = [(r"git repository: \ what reviewers read", YES),
                 (r"release tarball: \ what distributions built, \ with one extra build-script change", NO),
                 (r"the build unpacks code hidden in binary ``test'' files into \texttt{liblzma}", NO),
                 (r"some distributions link OpenSSH's server to \texttt{libsystemd}, \ which loads "
                  r"\texttt{liblzma}", KERN),
                 (r"inside \texttt{sshd} it intercepts the check of a client's key: \ only the attacker's private key "
                  r"opens it", NO)]
        chain = VGroup(*[wrapped_label(t, 11.6, font_size=20, color=c) for t, c in steps])
        chain.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(evs, DOWN, buff=0.6).set_x(0.35)
        bullets = VGroup(*[Dot(radius=0.05, color=GREY_B).next_to(c, LEFT, buff=0.2) for c in chain])
        with self.voiceover(
            "And sometimes the supplier is the attacker. <bookmark mark='a'/> In 2021 a newcomer began sending patches "
            "to xz-utils, a compression library inside almost every Linux system, maintained by one volunteer. "
            "<bookmark mark='b'/> Other accounts pressed him to share the work, and the newcomer became a "
            "co-maintainer. <bookmark mark='c'/> In early 2024 two releases carried a backdoor. <bookmark mark='d'/> "
            "It was not in the repository that reviewers read, but in the release archives distributions build "
            "from, where a changed build script unpacked code hidden in binary test files into the library. "
            "<bookmark mark='e'/> Where OpenSSH's server loads that library through systemd, it intercepted the "
            "check of a client's key, so only the attacker's key could open it."
        ) as vo:
            self.play(FadeIn(head), Create(spine), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(evs[0]))
            vo.wait_until("b")
            self.play(FadeIn(evs[1]))
            vo.wait_until("c")
            self.play(FadeIn(evs[2]))
            vo.wait_until("d")
            self.play(FadeIn(chain[0]), FadeIn(bullets[0]))
            self.play(FadeIn(chain[1]), FadeIn(bullets[1]))
            self.play(FadeIn(chain[2]), FadeIn(bullets[2]))
            vo.wait_until("e")
            self.play(FadeIn(chain[3]), FadeIn(bullets[3]))
            self.play(FadeIn(chain[4]), FadeIn(bullets[4]))
        self.wait(0.4)
        self.clear_scene()

    def slowdown(self):
        head = label(r"Half a second", font_size=36).to_edge(UP, buff=0.3)
        unit = 6.0
        before = Rectangle(width=unit * 0.35, height=0.55, stroke_width=0, fill_color=YES, fill_opacity=0.8)
        after = Rectangle(width=unit * 0.85, height=0.55, stroke_width=0, fill_color=NO, fill_opacity=0.8)
        bl = label(r"an SSH login, \ before", font_size=20, color=WHITE)
        al = label(r"after the upgrade", font_size=20, color=WHITE)
        rows = VGroup(VGroup(bl, before), VGroup(al, after))
        for r, y in zip(rows, (1.5, 0.6)):
            r[0].move_to([-4.6, y, 0]).align_to([-6.5, 0, 0], LEFT)
            r[1].move_to([-2.4, y, 0], aligned_edge=LEFT)
        extra = Rectangle(width=unit * 0.5, height=0.55, stroke_color=HEAD, stroke_width=2, fill_opacity=0)
        extra.move_to(after.get_right(), aligned_edge=RIGHT)
        el = label(r"about 500 ms more", font_size=20, color=HEAD).next_to(extra, DOWN, buff=0.15)
        sch = label(r"schematic: \ only the difference is the published figure", font_size=16,
                    color=GREY_B).next_to(rows, UP, buff=0.2).align_to(rows, LEFT)
        story = VGroup(
            wrapped_label(r"29 March 2024: \ Andres Freund, \ a PostgreSQL developer benchmarking on Debian's "
                          r"unstable branch, \ noticed \texttt{sshd} using unexpected CPU, \ slower logins and "
                          r"\texttt{valgrind} errors", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"he traced them to \texttt{liblzma} and reported it to the oss-security list: \ "
                          r"CVE-2024-3094", 12.4, font_size=20, color=YES),
            wrapped_label(r"it was caught before the stable releases of the major distributions shipped it \ --- \ by "
                          r"one engineer's curiosity about a timing, \ Chapter 4's side channel working for the "
                          r"defence", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(el, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "It was found by accident. <bookmark mark='a'/> On the twenty-ninth of March 2024, Andres Freund, a "
            "PostgreSQL developer benchmarking on Debian's unstable branch, noticed the SSH server using unexpected "
            "processor time, logins about half a second slower, and a memory checker complaining. <bookmark mark='b'/> He traced it to the compression library and reported it "
            "publicly. <bookmark mark='c'/> The stable releases of the major distributions had not yet shipped it. "
            "Two years of patient preparation were undone by half a second, noticed by one engineer: Chapter "
            "four's side channel, working for once for the defence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl), GrowFromEdge(before, LEFT), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(al), GrowFromEdge(after, LEFT))
            self.play(Create(extra), FadeIn(el), FadeIn(story[0]))
            vo.wait_until("b")
            self.play(FadeIn(story[1]))
            vo.wait_until("c")
            self.play(FadeIn(story[2]))
        self.wait(0.4)
        self.clear_scene()

    def defences(self):
        head = label(r"Knowing what you run", font_size=36).to_edge(UP, buff=0.3)
        names = [r"source commit", r"build", r"artifact", r"deploy"]
        what = [r"its hash names it \\ (Part 41)", r"signed provenance: \\ which source, \\ which builder",
                r"its hash pinned \\ in a lockfile", r"verify both \\ before running"]
        cols = [DATA, KERN, LAM, YES]
        boxes = VGroup(*[cbox(n, c, w=2.5, h=0.62, size=19) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.7)
        boxes.move_to([0, 1.5, 0])
        arrs = VGroup(*[arrow(boxes[i].get_right(), boxes[i + 1].get_left()) for i in range(3)])
        subs = VGroup(*[Tex(r"\begin{tabular}{c}" + w + r"\end{tabular}", font_size=18, color=c).next_to(b, DOWN,
                                                                                                      buff=0.22)
                        for w, b, c in zip(what, boxes, cols)])
        notes = VGroup(
            wrapped_label(r"\textbf{SLSA} \ (2021): \ graded levels of evidence about how an artifact was built", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"\textbf{SBOM}: \ a bill of materials, \ every component and version, \ so that when the "
                          r"next backdoor is found, \ everyone can tell at once whether they run it", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{reproducible builds}: \ anyone can rebuild from source and compare the bytes \ "
                          r"--- \ Chapter 12", 12.4, font_size=20, color=YES),
            wrapped_label(r"none of these checks that the source itself is honest: \ that still takes people reading "
                          r"it", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(subs, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "The defences make each link checkable. <bookmark mark='a'/> A commit is named by its hash; the build "
            "records signed provenance, which source and which builder; the artifact's hash is pinned in a "
            "lockfile; the deployer checks both. <bookmark mark='b'/> The SLSA framework, from 2021, grades this "
            "evidence; a bill of materials lists every component, so that when the next backdoor is found, "
            "everyone can tell at once whether they run it. <bookmark mark='c'/> And reproducible builds "
            "let anyone rebuild from source and compare bytes, which is where the next chapter begins. "
            "<bookmark mark='d'/> None of it checks that the source is honest. That still takes people reading it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b), FadeIn(s)) for b, s in zip(boxes, subs)],
                                  lag_ratio=0.5), LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.5),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
