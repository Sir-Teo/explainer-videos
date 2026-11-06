from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box)


class Deps(VoiceoverScene):
    def construct(self):
        self.card()
        self.diamond()
        self.semver()
        self.reduction()
        self.gadget()
        self.trace_steps()
        self.solvers()
        self.ecosystems()
        self.supply()

    def card(self):
        card = chapter_card(5, r"Dependencies", r"Which versions of everything can be installed together?",
                            lit=(2006, 2018), extra=((2006, r"Di Cosmo et al.: \ EDOS, \ NP-complete"),
                                                     (2018, r"Weizenbaum: \ PubGrub")), part=PART)
        with self.voiceover("Chapter five. Dependencies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def diamond(self):
        d = load("deps")["diamond"]["chosen"]
        head = label(r"A diamond", font_size=36).to_edge(UP, buff=0.3)
        app = module_box(r"app", HEAD, w=1.6).move_to([-3.0, 2.0, 0])
        a = module_box(r"A 1.x", DATA, w=1.6).move_to([-4.6, 0.5, 0])
        b10 = module_box(r"B 1.0", LAM, w=1.6).move_to([-2.2, 0.5, 0])
        b11 = module_box(r"B 1.1", YES, w=1.6).move_to([-0.4, 0.5, 0])
        cs = VGroup(*[module_box(rf"C {v}", YES if v == d["C"] else GREY_B, w=1.3) for v in (1, 2, 3)]).arrange(
            RIGHT, buff=0.4).move_to([-2.6, -1.2, 0])

        def arr(x, y, txt, col=GREY_B):
            ar = Arrow(x.get_bottom(), y.get_top(), buff=0.05, stroke_width=2, color=col,
                       max_tip_length_to_length_ratio=0.12)
            return VGroup(ar, label(txt, font_size=14, color=col).move_to(ar.get_center() + RIGHT * 0.35))
        e = VGroup(arr(app, a, r"any"), arr(app, b10, r"1.0 or 1.1"), arr(a, cs[1], r"C $\ge 2$"),
                   arr(b10, cs[0], r"C $< 2$", NO), arr(b11, cs[1], r"C $\le 2$", YES))
        notes = VGroup(
            wrapped_label(r"\textbf{semantic versioning}: \ \texttt{MAJOR.MINOR.PATCH}; \ a constraint like "
                          r"\texttt{>=2,<3} says which releases a package believes it works with", 5.0, font_size=19,
                          color=WHITE),
            wrapped_label(r"A needs C 2 or later; \ B 1.0 needs C before 2: \ no C satisfies both", 5.0,
                          font_size=19, color=NO),
            wrapped_label(rf"the solver backtracks to B 1.1, \ which allows C 2: \ \texttt{{A {d['A']}, B "
                          rf"{d['B'] // 10}.{d['B'] % 10}, C {d['C']}}}", 5.0, font_size=19, color=YES),
            wrapped_label(r"a \textbf{lockfile} records the answer, \ so every machine installs exactly the same "
                          r"versions until someone asks to update", 5.0, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.2, 0.2, 0])
        with self.voiceover(
            "Programs depend on packages, and packages on other packages, each published in many versions. "
            "<bookmark mark='a'/> Semantic versioning numbers releases major, minor, patch, and constraints say which "
            "releases a package expects to work with. <bookmark mark='b'/> Here an application needs A and B. A "
            "needs C version two or later; B version one point zero needs C before two. No single C satisfies both, "
            "and only one version of each package can be installed: the diamond. <bookmark mark='c'/> A resolver "
            "backtracks: B one point one allows C two, and everything fits. <bookmark mark='d'/> A lockfile records "
            "the answer, so every machine and every build installs exactly the same versions until someone asks "
            "to update."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(app), FadeIn(a), FadeIn(b10), FadeIn(b11), FadeIn(cs))
            vo.wait_until("b")
            self.play(FadeIn(e[:4]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(e[4]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def reduction(self):
        d = load("deps")
        g = d["gadget"]
        head = label(r"Choosing versions is NP-complete", font_size=36).to_edge(UP, buff=0.3)
        f = d["formula"]

        def lit(x):
            return (r"\lnot " if x < 0 else "") + f"x_{{{abs(x)}}}"
        formula = MathTex(r" \land ".join("(" + r" \lor ".join(lit(x) for x in c) + ")" for c in f), font_size=26,
                          color=HEAD).next_to(head, DOWN, buff=0.45)
        rows = [[r"for each variable $x_i$", r"a package \texttt{xi} \ with versions 0 and 1"],
                [r"for each clause $c_j$", r"a package \texttt{cj} \ with one version per literal"],
                [r"version $k$ of \texttt{cj}", r"requires \texttt{xi} at the value making literal $k$ true"],
                [r"the root", r"requires every \texttt{cj}, \ any version"]]
        tab = grid_table([r"in the formula", r"in the package universe"], rows, widths=[3.8, 7.6], row_h=0.48,
                         font_size=20, mono_cols=())
        tab.next_to(formula, DOWN, buff=0.4).set_x(0)
        ch = g["chosen"]
        xs = ", ".join(f"x{i}={ch[f'x{i}']}" for i in range(1, 5) if f"x{i}" in ch)
        lines = VGroup(
            wrapped_label(r"installable \ $\iff$ \ satisfiable: \ a solution picks, \ in each clause, \ a literal "
                          r"made true \ (Di Cosmo et al., 2006)", 12.4, font_size=21, color=YES),
            wrapped_label(rf"our solver on these {g['packages']} packages \ ({g['clauses']} clauses): \ "
                          rf"\texttt{{{xs}}}, \ which satisfies the formula", 12.4, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How hard is this in general? As hard as anything in Part 26. <bookmark mark='a'/> Take any formula in "
            "three-variable clauses. <bookmark mark='b'/> For each variable, publish a package with two versions, "
            "zero and one. For each clause, publish a package with one version per literal, and let version k "
            "require the variable package at whichever value makes literal k true. Finally let the root require "
            "every clause package, in any version. <bookmark mark='c'/> A consistent installation chooses, in every "
            "clause, a literal that its variable choices make true: it is a satisfying assignment, and every "
            "satisfying assignment gives one. So deciding whether a set of packages can be installed is "
            "NP-complete, as Roberto Di Cosmo and colleagues showed in 2006. Our resolver, given the packages for "
            "this formula, returns an assignment that satisfies it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(formula))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def solvers(self):
        d = load("deps")
        head = label(r"Solving it anyway", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['vars']}", f"{r['packages']}", f"{r['median_conflicts']:,}", f"{r['satisfiable'] * 100:.0f}\\%"]
                for r in d["hardness"]]
        tab = grid_table([r"variables", r"packages", r"solver conflicts \ (median)", r"installable"], rows,
                         widths=[2.0, 2.0, 3.6, 2.2], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][2].set_color(NO)
        lines = VGroup(
            wrapped_label(r"random formulas at the hard ratio \ (4.26 clauses per variable, \ Part 26), \ written as "
                          r"packages and given to our CDCL solver: \ the work grows fast", 12.4, font_size=20,
                          color=GREY_A),
            wrapped_label(r"real resolvers survive because real universes are easy: \ few conflicts, \ prefer the "
                          r"newest version, \ backtrack rarely; \ \textbf{PubGrub} \ (Dart, \ 2018; \ now also Python's "
                          r"uv) \ learns from conflicts like CDCL \ and explains failures in words", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"or avoid the problem: \ Go's \textbf{minimal version selection} \ takes the oldest "
                          r"version every constraint allows \ --- \ polynomial, \ because constraints can only say "
                          r"``at least''", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "NP-completeness is about the worst case. <bookmark mark='a'/> Write random hard formulas as packages, at "
            "Part 26's threshold of four point two six clauses per variable, and our CDCL solver's work climbs "
            "steeply: six conflicts at twenty variables, over four hundred at eighty. <bookmark mark='b'/> Real "
            "package universes are far kinder: most constraints are loose, the newest version usually works, and "
            "conflicts are rare. Natalie Weizenbaum's PubGrub, written for Dart and now also used by Python's uv, "
            "learns from each conflict as CDCL does, and can explain in plain words why no solution "
            "exists. <bookmark mark='c'/> Go chose to remove the problem instead. Its minimal version selection "
            "allows only lower bounds, and takes the oldest version that satisfies all of them, which is "
            "computable in polynomial time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def supply(self):
        head = label(r"The supply chain", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"every dependency is code from strangers that runs with your privileges: \ "
                          r"\texttt{event-stream} \ (2018: \ a new maintainer added a wallet stealer), \ SolarWinds \ "
                          r"(2020: \ a compromised build server), \ xz \ (2024)", 12.4, font_size=22, color=NO),
            wrapped_label(r"\textbf{signatures} on releases and commits; \ \textbf{SBOMs}, \ the list of everything "
                          r"inside a build; \ \textbf{SLSA} levels for how a build was produced and attested", 12.4,
                          font_size=22, color=YES),
            wrapped_label(r"reproducible builds \ (Chapter 4) \ let independent parties check a binary against its "
                          r"source; \ Part 61 returns to trust in software", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"\textbf{vendoring} \ (copying dependencies into the repository) \ trades updates for "
                          r"control", 12.4, font_size=22, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Every dependency is code written by strangers that runs with your program's privileges. "
            "<bookmark mark='a'/> In 2018 a new maintainer of the popular event-stream package added code that "
            "tried to steal cryptocurrency wallets. In 2020 attackers who had compromised SolarWinds' build system "
            "shipped a backdoor inside a signed update. In 2024 came xz. <bookmark mark='b'/> The defences are "
            "signatures on releases and commits, software bills of materials that list everything inside a build, "
            "and the SLSA levels, which grade how trustworthy the process that produced a build was. "
            "<bookmark mark='c'/> Reproducible builds let independent parties check a binary against its source, "
            "and Part 61 returns to the deeper question of trusting software at all. <bookmark mark='d'/> Vendoring, "
            "copying dependencies into your own repository, trades easy updates for control."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def ecosystems(self):
        head = label(r"Ecosystems", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{npm} allows several versions of one package side by side, \ nested under the "
                          r"packages that need them: \ the diamond disappears, \ and installations grow to thousands "
                          r"of packages", 12.4, font_size=22, color=DATA),
            wrapped_label(r"\textbf{pip}, \ \textbf{Cargo} \ (per major version) \ and most system package "
                          r"managers allow one version: \ smaller installs, \ and the resolution problem of this "
                          r"chapter", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"\textbf{left-pad} \ (March 2016): \ an eleven-line npm package was unpublished, \ and "
                          r"builds across the industry that depended on it, \ directly or not, \ failed within hours; "
                          r"\ npm then restricted unpublishing", 12.4, font_size=22, color=NO),
            wrapped_label(r"lockfiles record a \textbf{hash} of every package \ (npm's \texttt{integrity}, \ pip's "
                          r"\texttt{--require-hashes}): \ the same name and version can never silently become "
                          r"different code", 12.4, font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Ecosystems answer the diamond differently. <bookmark mark='a'/> JavaScript's npm lets several versions "
            "of the same package coexist, each nested under the packages that need it. The diamond disappears, and "
            "an ordinary application installs thousands of packages. <bookmark mark='b'/> Python's pip and most "
            "operating-system package managers allow one version of each package, which keeps installs small and "
            "brings back the resolution problem we just saw. <bookmark mark='c'/> Small packages make long chains. "
            "In March 2016 an eleven-line npm package called left-pad was withdrawn by its author, and builds across "
            "the industry that depended on it, often without knowing, failed within hours. "
            "<bookmark mark='d'/> Today lockfiles record a hash of every package's contents, Chapter 1's idea again, "
            "so that a name and version can never silently become different code."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def trace_steps(self):
        t = load("trace")
        head = label(r"A resolver at work", font_size=36).to_edge(UP, buff=0.3)

        def ver(p, v):
            return f"{v // 10}.{v % 10}" if p == "B" else f"{v}"
        rows = VGroup()
        for kind, p, v, allowed in t["steps"]:
            if kind == "try":
                txt, col = rf"try \texttt{{{p} {ver(p, v)}}}, \ the newest allowed", WHITE
            elif kind == "conflict":
                txt, col = rf"conflict: \ \texttt{{{p} {ver(p, v)}}} chosen, \ but something needs {p} in "
                txt += r"\{" + ", ".join(ver(p, a) for a in allowed) + r"\}"
                col = NO
            else:
                txt, col = rf"undo \texttt{{{p} {ver(p, v)}}}, \ try the next", HEAD
            rows.add(label(txt, font_size=21, color=col))
        res = t["result"]
        rows.add(label(r"solution: \ " + r", \ ".join(rf"\texttt{{{k} {ver(k, v)}}}" for k, v in res.items()),
                       font_size=22, color=YES))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        note = wrapped_label(r"depth-first search with the newest version first: \ exponential in the worst case "
                             r"\ (the reduction above), \ quick when constraints are loose; \ CDCL and PubGrub add "
                             r"learning, \ so a conflict is never rediscovered", 4.6, font_size=19,
                             color=GREY_A).move_to([4.3, -0.4, 0])
        with self.voiceover(
            "Here is what a simple resolver does on the diamond, step by step. <bookmark mark='a'/> It takes the "
            "requirements in order and tries the newest allowed version of each: the application, A version one, "
            "B version one point one, and then C version three, the newest. <bookmark mark='b'/> But B one point "
            "one allows C only up to two: a conflict. The resolver undoes its choice of C and tries the next "
            "version, two, which satisfies everyone. <bookmark mark='c'/> This depth-first search, newest first, is "
            "exponential in the worst case, as the reduction promises, and quick when constraints are loose. CDCL "
            "and PubGrub add learning: once a combination has failed, it is never tried again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def semver(self):
        head = label(r"Does semantic versioning work?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"the promise: \ upgrading within a major version never breaks you", 12.4, font_size=23,
                          color=WHITE),
            wrapped_label(r"Raemaekers, van Deursen and Visser \ (2014): \ in the Maven repository about a third of "
                          r"releases contained at least one breaking change, \ minor and patch releases included", 12.4,
                          font_size=23, color=NO),
            wrapped_label(r"and Hyrum's law \ (Part 40) \ means even a true bug fix breaks someone who relied on the "
                          r"bug", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"hence lockfiles, \ tests run on every upgrade, \ and tools that compare a library's API "
                          r"between versions to check the version number it claims \ (Rust's "
                          r"\texttt{cargo-semver-checks}, \ Elm's enforced versions)", 12.4, font_size=23,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Semantic versioning is a promise, and promises can be checked. <bookmark mark='a'/> The promise is that "
            "upgrading within a major version never breaks you. <bookmark mark='b'/> When Steven Raemaekers and "
            "colleagues compared successive releases in Java's Maven repository, about a third of releases contained "
            "at least one breaking change, minor and patch releases included. <bookmark mark='c'/> And Hyrum's law "
            "from Part 40 means that even a genuine bug fix breaks someone who relied on the bug. "
            "<bookmark mark='d'/> So lockfiles pin exact versions, upgrades are tested, and some ecosystems check "
            "the promise mechanically: Elm refuses to publish a release whose version number understates its API "
            "changes, and Rust has tools that do the same comparison."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def gadget(self):
        d = load("deps")
        f = d["formula"]
        ch = d["gadget"]["chosen"]
        head = label(r"The formula, \ as packages", font_size=36).to_edge(UP, buff=0.3)
        xs = VGroup()
        for i in range(1, 5):
            vs = VGroup(*[module_box(rf"\texttt{{x{i}={v}}}", YES if ch.get(f"x{i}") == v else GREY_C, w=1.2, h=0.45,
                                     font=14) for v in (0, 1)]).arrange(DOWN, buff=0.12)
            xs.add(vs)
        xs.arrange(RIGHT, buff=1.0).move_to([0, -1.9, 0])
        cs = VGroup()
        for j, c in enumerate(f, 1):
            vs = VGroup(*[module_box(rf"\texttt{{c{j}.{k}}}", YES if ch.get(f"c{j}") == k else GREY_C, w=1.0, h=0.42,
                                     font=13) for k in range(1, len(c) + 1)]).arrange(RIGHT, buff=0.06)
            cs.add(vs)
        cs.arrange(RIGHT, buff=0.35).move_to([0, 0.9, 0])
        root = module_box(r"root", HEAD, w=1.2).move_to([0, 2.4, 0])
        arrows = VGroup()
        for j, c in enumerate(f):
            arrows.add(Line(root[0].get_bottom(), cs[j].get_top(), color=GREY_C, stroke_width=1.2))
            for k, l in enumerate(c):
                v = 1 if l > 0 else 0
                tgt = xs[abs(l) - 1][1 - v]
                chosen = ch.get(f"c{j + 1}") == k + 1
                arrows.add(Line(cs[j][k][0].get_bottom(), tgt[0].get_top(), color=YES if chosen else GREY_D,
                                stroke_width=2.2 if chosen else 0.8))
        note = wrapped_label(r"each clause package's chosen version points at a variable version it requires; \ "
                             r"the green choices are one consistent installation \ --- \ and a satisfying "
                             r"assignment", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Drawn out, the reduction looks like any package graph. <bookmark mark='a'/> At the top, the root "
            "requires every clause package. Each clause package offers one version per literal, and each of those "
            "versions requires one version of one variable package. <bookmark mark='b'/> A resolver's answer picks "
            "one version of every package, here in green. Following the chosen arrows down, every variable gets "
            "exactly one value, and every clause has a literal that value makes true. Installing these packages and "
            "satisfying the formula are the same problem, written in two notations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), FadeIn(cs), FadeIn(xs))
            vo.wait_until("a")
            self.play(Create(arrows), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
