from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import (COST, CTRL, DATA, FUNC, HEAD, HIST, NO, PART, YES, bowl, fmt, say, load, pebble,
                                  pebble_pile, step_counter)


def lam_tex(s: str, font_size=30, redex_color=None) -> MathTex:
    """A term from compute (the redex wrapped in {{ }}) as MathTex with the redex its own part."""
    if "{{" in s:
        pre, rest = s.split("{{", 1)
        red, post = rest.split("}}", 1)
        parts = [p for p in (pre, red, post) if p.strip()]
        m = MathTex(*parts, font_size=font_size, color=FUNC)
        if redex_color:
            m[parts.index(red)].set_color(redex_color)
        m.redex = m[parts.index(red)]
        return m
    m = MathTex(s, font_size=font_size, color=FUNC)
    m.redex = None
    return m


def frames_rgba(frames: np.ndarray, on, off) -> np.ndarray:
    a = np.zeros(frames.shape + (4,), np.uint8)
    on_, off_ = hex_rgb(on), hex_rgb(off)
    a[..., :3] = np.where(frames[..., None] > 0, on_, off_)
    a[..., 3] = 255
    return a


class Models(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.card()
        self.church()
        self.reduction()
        self.counters()
        self.minsky()
        self.automata()
        self.web()

    def card(self):
        card = chapter_card(8, r"Other machines, same power", r"Do different definitions of computing agree?",
                            lit=(1936, 1967, 1970, 2004), part=PART)
        with self.voiceover("Chapter eight. Other machines, same power."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def church(self):
        hc = history_card(r"1932--36", r"Alonzo Church, \ Princeton", r"a calculus with nothing but functions: \ the "
                          r"$\lambda$-calculus", width=5.6, font_size=22).to_corner(UL, buff=0.35)
        syn = VGroup(
            label(r"three kinds of term:", font_size=28, color=GREY_A),
            cmath(r"x", r"\qquad", r"\lambda x.\, M", r"\qquad", r"M\, N", font_size=42,
                  colors={r"\lambda x.\, M": FUNC, r"M\, N": DATA}),
            label(r"a variable, \quad a function of $x$, \quad applying $M$ to $N$", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.2).move_to(UP * 1.6 + RIGHT * 2.6)
        beta = VGroup(label(r"one rule, \ $\beta$-reduction:", font_size=28, color=GREY_A),
                      cmath(r"(\lambda x.\, M)\, N", r"\;\longrightarrow_\beta\;", r"M[x := N]", font_size=40,
                            colors={r"(\lambda x.\, M)\, N": FUNC, r"M[x := N]": YES})).arrange(DOWN, buff=0.2)
        beta.next_to(syn, DOWN, buff=0.5)
        nums = VGroup(*[cmath(rf"{n}", r"=", rf"\lambda f\, x.\;" + (r"f\,(" * n) + "x" + (")" * n), font_size=32,
                              colors={rf"{n}": DATA}) for n in range(4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for k in nums:
            k[2].set_color(FUNC)
        nums.move_to(DOWN * 1.9 + LEFT * 3.0)
        nl = label(r"Church numerals: \ the number $n$ is ``apply $f$, $n$ times''", font_size=26, color=DATA)
        nl.next_to(nums, UP, buff=0.25).align_to(nums, LEFT)
        with self.voiceover(
            "Church's answer to Hilbert looked nothing like a machine. <bookmark mark='a'/> His lambda calculus has only "
            "three kinds of expression: a variable; a function, lambda x dot M, meaning the function that takes x to M; "
            "and an application, M applied to N. <bookmark mark='b'/> And one rule of computation, beta reduction: a "
            "function applied to an argument becomes its body, with the argument substituted for the variable. "
            "<bookmark mark='c'/> There are no numbers. You build them. The number n is the function that applies f to "
            "x, n times: zero applies it no times, three applies it three times."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(syn))
            vo.wait_until("b")
            self.play(FadeIn(beta))
            vo.wait_until("c")
            self.play(FadeIn(nl), LaggedStart(*[FadeIn(n, shift=RIGHT * 0.15) for n in nums], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reduction(self):
        d = load("lam")
        seq = d["plus23"]
        plus = cmath(r"\mathrm{PLUS}", r"=", r"\lambda m\, n\, f\, x.\;", r"m\, f\,", r"(n\, f\, x)", font_size=40,
                     colors={r"\mathrm{PLUS}": CTRL, r"\lambda m\, n\, f\, x.\;": FUNC, r"m\, f\,": FUNC,
                             r"(n\, f\, x)": FUNC}).to_edge(UP, buff=0.35)
        pl = label(r"``apply $f$ $n$ times, \ then $m$ more times''", font_size=26, color=GREY_A).next_to(plus, DOWN,
                                                                                                  buff=0.15)
        rows = VGroup(*[lam_tex(s["tex"], font_size=28, redex_color=HEAD) for s in seq])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(pl, DOWN, buff=0.4)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        rows.set_x(0.2)
        arrows = VGroup(*[MathTex(r"\to_\beta", font_size=26, color=GREY_B).next_to(r, LEFT, buff=0.15)
                          for r in rows[1:]])
        n = len(seq) - 1
        five = label(r"$= 5$", font_size=36, color=YES).next_to(rows[-1], RIGHT, buff=0.3)
        tab = VGroup(*[label(rf"$\mathrm{{{c['op']}}}\ {c['a']}\ {c['b']}$:\ {c['steps']} steps", font_size=22,
                             color=GREY_A) for c in d["counts"] if c["a"] == 2 and c["b"] == 3])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Addition is a function too. PLUS takes m and n, and returns the numeral that applies f n times, then m "
            "more times. <bookmark mark='a'/> Now compute two plus three by reduction alone. Each line comes from the "
            "one above by one beta step, on the highlighted part; this is the leftmost, outermost choice, which our "
            "reducer always takes. <bookmark mark='b'/> "
            f"After {n} steps there is nothing left to reduce: lambda f x, f applied five times. Five. Multiplication "
            "and powers work the same way, with a few more steps. Church showed that numerals, pairs, lists, "
            "recursion, anything, can be built from functions alone."
        ) as vo:
            self.play(FadeIn(plus), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for i in range(1, len(rows)):
                if rows[i - 1].redex is not None:
                    self.play(Indicate(rows[i - 1].redex, color=HEAD, scale_factor=1.08), run_time=0.6)
                self.play(FadeIn(arrows[i - 1]), TransformFromCopy(rows[i - 1], rows[i]), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(five), FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counters(self):
        d = load("counters")
        hist = d["history3"]
        prog = d["prog3"]
        hc = history_card(1961, r"Marvin Minsky", r"counter machines: \ a few counters that hold whole numbers, \ and a "
                          r"numbered list of instructions", width=5.6, font_size=22).to_corner(UL, buff=0.35)
        xs = [-3.6, 0.0, 3.6]
        bowls = VGroup(*[bowl(2.6, 1.0).move_to([x, -2.3, 0]) for x in xs])
        names = VGroup(*[label(rf"$r_{i}$", font_size=32, color=DATA).next_to(b, DOWN, buff=0.15)
                         for i, b in enumerate(bowls)])
        piles = []
        seed = 5
        for i, x in enumerate(xs):
            n = hist[0][1][i]
            piles.append([pebble(0.16, seed=seed + k) for k in range(n)])
            seed += 20

        def spot(i, k):  # the k-th pebble's place in bowl i
            r, c = divmod(k, 5)
            return np.array([xs[i] + (c - 2) * 0.36, -2.55 + r * 0.3, 0])

        for i in range(3):
            for k, p in enumerate(piles[i]):
                p.move_to(spot(i, k))
        lines = [r"0: \ if $r_1 > 0$: \ $r_1 \mathrel{-}= 1$, \ go to 1; \ else go to 2",
                 r"1: \ $r_0 \mathrel{+}= 1$, \ go to 0",
                 r"2: \ if $r_0 > 0$: \ $r_0 \mathrel{-}= 1$, \ go to 3; \ else go to 4",
                 r"3: \ $r_2 \mathrel{+}= 1$, \ go to 2",
                 r"4: \ halt"]
        code = VGroup(*[label(t, font_size=26, color=GREY_A) for t in lines]).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.14)
        code.move_to(RIGHT * 2.6 + UP * 1.6)
        pc = SurroundingRectangle(code[0], color=HEAD, buff=0.06, corner_radius=0.06)
        what = label(r"$r_2 := r_0 + r_1$", font_size=34, color=YES).next_to(code, DOWN, buff=0.3)
        cnt = step_counter().to_corner(UR, buff=0.3)
        with self.voiceover(
            "Here is a third definition, and the opening's pebbles come back. <bookmark mark='a'/> A counter machine has a "
            "few bowls of pebbles, and a numbered list of instructions of only two kinds: add a pebble to a bowl; or, if "
            "a bowl is not empty, take a pebble out and go to one instruction, and if it is empty, go to another. "
            "<bookmark mark='b'/> This five-line program moves every pebble from bowl one into bowl zero, then every "
            "pebble from bowl zero into bowl two. It computes r zero plus r one. <bookmark mark='c'/> Three plus four:"
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(bowls), FadeIn(names))
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for pile in piles for p in pile], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(code))
            vo.wait_until("b")
            self.play(FadeIn(what), Create(pc))
            vo.wait_until("c")
            self.play(FadeIn(cnt))
        with self.voiceover(
            f"pebble by pebble, {len(hist) - 1} steps, and bowl two holds seven. A person moving pebbles by these rules "
            "could compute anything a Turing machine can, given enough bowls, pebbles and patience. Minsky proved it."
        ):
            for i in range(len(hist) - 1):
                pcn, regs = hist[i]
                npc, nregs = hist[i + 1]
                anims = [pc.animate(run_time=0.35).move_to(code[npc]).set(width=code[npc].width + 0.12),
                         cnt.tracker.animate(run_time=0.35).set_value(i + 1)]
                ins = prog[pcn]
                if ins[0] == "dec" and regs[ins[1]] > 0:
                    p = piles[ins[1]].pop()
                    self._held = p
                    anims.append(p.animate(run_time=0.35).shift(UP * 0.9))
                elif ins[0] == "inc":
                    r = ins[1]
                    p = getattr(self, "_held", None) or pebble(0.16, seed=99 + i)
                    self._held = None
                    piles[r].append(p)
                    anims.append(p.animate(run_time=0.35).move_to(spot(r, len(piles[r]) - 1)))
                self.play(*anims)
            self.play(Indicate(VGroup(*piles[2]), color=YES))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minsky(self):
        d = load("counters")
        r = next(x for x in d["runs"] if x["a"] == 3 and x["b"] == 4)
        thm = theorem_card(r"Minsky (1961, 1967)", r"Two counters are enough: \ any counter machine, and so any Turing "
                           r"machine, can be simulated by a machine with just two bowls.", width=11.0, font_size=26)
        thm.to_edge(UP, buff=0.35)
        enc = cmath(r"A", r"=", r"2^{r_0}", r"\cdot", r"3^{r_1}", r"\cdot", r"5^{r_2}", font_size=44,
                    colors={r"A": DATA, r"2^{r_0}": CTRL, r"3^{r_1}": CTRL, r"5^{r_2}": CTRL}).move_to(UP * 1.2)
        how = label(r"$r_1 \mathrel{+}= 1$: \ multiply $A$ by 3, \ using bowl $B$ as scratch \\ is $r_1 > 0$? \ is $A$ "
                    r"divisible by 3?", font_size=26, color=GREY_A).next_to(enc, DOWN, buff=0.3)
        A = np.asarray(d["A"], float)
        ax = CornerAxes(x_range=[0, 1, 0.25], y_range=[0, 5.1, 1], x_length=6.0, y_length=2.6, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to(DOWN * 2.15 + LEFT * 2.4)
        xs = np.linspace(0, 1, len(A))
        cA = curve(ax, xs, np.log10(np.maximum(A, 1)), DATA, 2.5)
        axl = label(r"$\log_{10} A$ during the run", font_size=22, color=DATA).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        nums = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (rf"start: \ $A = 2^3 3^4 = {fmt(r['godel_in'])}$", GREY_A),
            (rf"end: \ $A = 5^7 = {fmt(r['godel_out'])}$", YES),
            (rf"three bowls: \ {r['three_steps']} steps", GREY_A),
            (rf"two bowls ({d['two_len']} instructions): \ {fmt(r['steps'])} steps", COST),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(DOWN * 2.1 + RIGHT * 3.6)
        with self.voiceover(
            "In fact two bowls are enough. <bookmark mark='a'/> The trick is to pack all the counters into one number: "
            "two to the r zero, times three to the r one, times five to the r two. <bookmark mark='b'/> Adding one to r "
            "one means multiplying by three, which a second bowl can do as scratch space; testing r one means asking "
            "whether the number is divisible by three. <bookmark mark='c'/> We wrote a compiler that turns any program "
            f"into a two-bowl program; the adder becomes {d['two_len']} instructions. On three plus four, the big bowl "
            f"starts with {say(r['godel_in'])} pebbles and ends with {say(r['godel_out'])}, five to the seventh. "
            f"Three bowls took {r['three_steps']} steps. Two bowls take {say(r['steps'])}. Same power; an exponential "
            "price."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Write(enc))
            vo.wait_until("b")
            self.play(FadeIn(how))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(axl))
            self.play(Create(cA), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.4), run_time=2.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def automata(self):
        g = np.asarray(load("rule110")["grid"])
        rule = 110
        icons = VGroup()
        for k in range(7, -1, -1):
            nb = [(k >> 2) & 1, (k >> 1) & 1, k & 1]
            out = (rule >> k) & 1
            top = VGroup(*[Square(0.26, stroke_width=1, stroke_color=GREY_C, fill_color=WHITE if b else BACKGROUND,
                                  fill_opacity=1) for b in nb]).arrange(RIGHT, buff=0)
            bot = Square(0.26, stroke_width=1, stroke_color=GREY_C, fill_color=HEAD if out else BACKGROUND,
                         fill_opacity=1).next_to(top, DOWN, buff=0.06)
            icons.add(VGroup(top, bot))
        icons.arrange(RIGHT, buff=0.32).to_edge(UP, buff=0.35)
        il = label(r"Rule 110: \ each cell's next colour from itself and its two neighbours", font_size=24,
                   color=GREY_A).next_to(icons, DOWN, buff=0.2)
        crop = g[:240, -360:]
        img = bitmap(crop, [BACKGROUND, HEAD], width=7.8, height=5.2).move_to(DOWN * 1.05 + LEFT * 2.4)
        tl = label(r"time $\downarrow$", font_size=22, color=GREY_B).next_to(img, LEFT, buff=0.12)
        thm = theorem_card(r"Cook (2004)", r"Rule 110 is Turing-complete: \ its gliders can be arranged to simulate any "
                           r"Turing machine. \ (Conjectured by Wolfram.)", width=4.8, font_size=22)
        thm.move_to(RIGHT * 4.4 + DOWN * 1.2)
        with self.voiceover(
            "Even simpler. A row of cells, each black or white. At every tick, each cell looks at itself and its two "
            "neighbours and changes colour by a fixed table of eight cases. <bookmark mark='a'/> This table is called "
            "Rule 110. Start it from a single black cell and draw each generation under the last. <bookmark mark='b'/> "
            "Structure appears: triangles, and gliders that crawl across the background and collide. "
            "<bookmark mark='c'/> In 2004 Matthew Cook proved that those collisions can be arranged to simulate any "
            "Turing machine. Eight cases, and nothing else, is universal."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.1) for i in icons], lag_ratio=0.1), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(tl))
            vo.wait_until("b")
            self.play(Indicate(img, scale_factor=1.02, color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(thm, shift=LEFT * 0.2))
        frames = np.asarray(load("life")["frames"])
        rgba = frames_rgba(frames, YES, BACKGROUND)
        life_img = ImageMobject(rgba[0])
        life_img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        life_img.scale_to_fit_width(9.6).move_to(DOWN * 0.4)
        tr = ValueTracker(0)
        life_img.add_updater(lambda m: setattr(m, "pixel_array", rgba[min(int(tr.get_value()), len(rgba) - 1)]))
        lh = label(r"Conway's Game of Life (1970): \ a glider gun", font_size=30, color=YES).to_edge(UP, buff=0.4)
        lt = label(r"a live cell survives with 2 or 3 live neighbours; \ a dead cell with exactly 3 comes alive",
                   font_size=24, color=GREY_A).next_to(lh, DOWN, buff=0.15)
        lu = note(r"universal too: \ Berlekamp, Conway and Guy (1982)", font_size=22).to_corner(DR, buff=0.35)
        with self.voiceover(
            "In two dimensions, John Conway's Game of Life: a cell lives on with two or three live neighbours, and comes "
            "to life with exactly three. <bookmark mark='a'/> This pattern, Bill Gosper's glider gun, fires a stream of "
            "gliders forever. Streams of gliders can carry signals, and collisions can do logic. The Game of Life is "
            "universal too."
        ) as vo:
            self.play(FadeOut(Group(icons, il, img, tl, thm)), FadeIn(lh), FadeIn(lt), FadeIn(life_img))
            vo.wait_until("a")
            self.play(tr.animate.set_value(len(rgba) - 1), FadeIn(lu), run_time=9.0, rate_func=linear)
        life_img.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def web(self):
        names = [(r"Turing \\ machines", CTRL), (r"$\lambda$-calculus", FUNC), (r"recursive \\ functions", FUNC),
                 (r"counter \\ machines", DATA), (r"Rule 110", HEAD), (r"Game of \\ Life", YES),
                 (r"Pebble-32 \\ (Part 6)", C.CS_CODE), (r"your \\ laptop", GREY_A)]
        R = 2.8
        boxes = VGroup()
        for i, (t, c) in enumerate(names):
            ang = PI / 2 - i * TAU / len(names)
            b = node_box(t, c, font_size=24).move_to([R * 1.45 * np.cos(ang), R * np.sin(ang) - 0.3, 0])
            boxes.add(b)
        links = VGroup()
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                links.add(Line(boxes[i].get_center(), boxes[j].get_center(), color=GREY_D, stroke_width=1.2))
        links.set_z_index(-1)
        for b in boxes:
            b[0].set_fill(BACKGROUND, opacity=1)
        center = label(r"each simulates \\ every other", font_size=30, color=GREY_A).move_to(DOWN * 0.3)
        center.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.1)
        with self.voiceover(
            "Machines with tapes; functions alone; recursive definitions, which Gödel and Kleene studied; bowls of "
            "pebbles; a row of cells; a grid of cells. <bookmark mark='a'/> Each was proposed independently, each looks "
            "completely different, and each can simulate every other one. They all compute exactly the same functions. "
            "<bookmark mark='b'/> So will Pebble, the computer we build in Part 6, and so does the laptop you are "
            "watching on, apart from its finite memory."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes[:6]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(links, lag_ratio=0.02), FadeIn(center), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes[6:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
