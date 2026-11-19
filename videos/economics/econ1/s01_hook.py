from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


def paris(seed: int = 1845) -> VGroup:
    """Paris at night, drawn: the ring of the city wall, the Seine, and a few hundred houses with lit windows."""
    rng = np.random.default_rng(seed)
    wall = Ellipse(width=6.6, height=4.7, stroke_color=GREY_C, stroke_width=3, fill_color=NIGHT, fill_opacity=1)
    river_pts = [np.array(p) for p in ((-3.7, 0.55, 0), (-2.2, 0.05, 0), (-0.9, 0.55, 0), (0.4, 0.2, 0),
                                       (1.6, -0.55, 0), (2.8, -0.2, 0), (3.7, -0.65, 0))]
    river = VMobject(stroke_color="#2C4A70", stroke_width=12)
    river.set_points_smoothly(river_pts)
    houses = VGroup()
    windows = VGroup()
    tries = 0
    while len(houses) < 230 and tries < 5000:
        tries += 1
        x, y = rng.uniform(-3.1, 3.1), rng.uniform(-2.15, 2.15)
        if (x / 3.1) ** 2 + (y / 2.2) ** 2 > 0.92:
            continue
        ry = np.interp(x, [p[0] for p in river_pts], [p[1] for p in river_pts])
        if abs(y - ry) < 0.28:
            continue
        w, h = rng.uniform(0.12, 0.24), rng.uniform(0.1, 0.18)
        house = Rectangle(width=w, height=h, stroke_width=0, fill_color="#1B2433", fill_opacity=1).move_to([x, y, 0])
        win = Square(side_length=0.045, stroke_width=0, fill_color=LAMP, fill_opacity=0.95).move_to([x, y, 0])
        houses.add(house)
        windows.add(win)
    g = VGroup(wall, river, houses, windows)
    g.wall, g.river, g.houses, g.windows = wall, river, houses, windows
    return g


def departments(n: int = 80, seed: int = 80) -> VGroup:
    """France's departments as a ring of dots around the city (schematic), each joined to it by a road."""
    rng = np.random.default_rng(seed)
    dots, roads = VGroup(), VGroup()
    for k in range(n):
        a = TAU * k / n + rng.uniform(-0.03, 0.03)
        r = rng.uniform(2.2, 3.35)
        p = np.array([1.75 * r * np.cos(a), 1.08 * r * np.sin(a), 0])
        d = Dot(p, radius=0.045, color=GREY_B)
        road = Line(p, p * 0.24, color=GREY_D, stroke_width=1.2)
        dots.add(d)
        roads.add(road)
    g = VGroup(roads, dots)
    g.dots, g.roads = dots, roads
    return g


GOODS = ["#D9A25F", "#B5486B", "#9C7A4B", E.FISH, "#F2F2E8", "#8A8F99"]  # grain, wine, wood, fish, milk, coal


class Hook(VoiceoverScene):
    def construct(self):
        self.night()
        self.title()
        self.queen()
        self.two_things()
        self.three_questions()
        self.objectives()

    # ------------------------------------------------------------------
    def night(self):
        b = tables.BASTIAT_1845.data
        city = paris()
        where = VGroup(label(r"Paris, \ 1845", font_size=40, color=LAMP),
                       label(r"about a million people", font_size=26, color=GREY_A))
        where.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.45)
        ring = departments()
        quote = quote_card(b["million"] + r" \dots \ " + b["sleeping"], r"Fr\'ed\'eric Bastiat, \emph{Economic "
                           r"Sophisms} (1845)", width=8.6, font_size=28).to_edge(DOWN, buff=0.35)
        src = published_tag(tables.BASTIAT_1845.tag, corner=DR, font_size=18)
        with self.voiceover(
            "In the 1840s, a French economist named Frédéric Bastiat came to Paris for a visit, and found himself "
            "thinking about something most people never think about at all. "
            "<bookmark mark='a'/> Here, he wrote, are a million human beings who would all die in a few days if "
            "supplies of all sorts did not flow into this great metropolis. <bookmark mark='b'/> Flour, meat, "
            "wine, firewood, candles, cloth: a vast quantity of things has to come through the city's gates "
            "tomorrow, and the day after, and every day after that. <bookmark mark='c'/> And yet, he wrote, all "
            "are sleeping peacefully at this moment, without being disturbed for a single instant by the idea of "
            "so frightful a prospect."
        ) as vo:
            self.play(FadeIn(city.wall), Create(city.river), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(h) for h in city.houses], lag_ratio=0.004),
                      LaggedStart(*[FadeIn(w) for w in city.windows], lag_ratio=0.004), FadeIn(where), run_time=2.4)
            vo.wait_until("a")
            self.play(city.animate.scale(0.72).shift(UP * 1.35), FadeIn(quote, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("c")
            order = np.random.default_rng(7).permutation(len(city.windows))
            self.play(LaggedStart(*[city.windows[int(i)].animate.set_fill(opacity=0.06) for i in order],
                                  lag_ratio=0.02), run_time=vo.remaining(1.0))
        self.play(FadeOut(quote), FadeOut(src), FadeOut(where), city.animate.scale(1 / 0.72).move_to(ORIGIN))

        how = label(r"neither too much, \ nor too little", font_size=44, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        q_src = published_tag(tables.BASTIAT_1845.tag, corner=DR, font_size=18)
        flows = VGroup()
        with self.voiceover(
            "Nobody in Paris was in charge of feeding Paris. There was no ministry of bread that counted the mouths "
            "and ordered the wheat. <bookmark mark='a'/> Eighty departments, Bastiat said, the whole of France, had "
            "worked that day, without any plan and without arranging it among themselves, to keep the city "
            "supplied. <bookmark mark='b'/> And he asked the question that this whole series is about. How does "
            "each day manage to bring to this gigantic market just what is necessary: <bookmark mark='c'/> "
            "neither too much, nor too little?"
        ) as vo:
            self.play(city.animate.scale(0.26), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromPoint(r, r.get_start()) for r in ring.roads], lag_ratio=0.01),
                      LaggedStart(*[FadeIn(d, scale=0.5) for d in ring.dots], lag_ratio=0.01), run_time=2.6)
            for k, road in enumerate(ring.roads):
                if k % 2 == 0:
                    f = flowing(road, GOODS[k % len(GOODS)], n=2, period=3.2 + 0.4 * (k % 5), radius=0.035)
                    flows.add(f)
            self.add(flows)
            vo.wait_until("c")
            self.play(FadeIn(how, shift=UP * 0.15), FadeIn(q_src))
            self.wait(1.5)
        for f in flows:
            f.clear_updaters()
        self.clear_scene()

    def title(self):
        logo = scissors_logo(1.5)
        t = label(SERIES_EN, font_size=72)
        sub = label(r"Part 1 \ \textperiodcentered\ \ Who Feeds Paris?", font_size=40, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part one: who feeds Paris?"):
            self.play(Create(logo.demand), Create(logo.supply), run_time=1.2)
            self.play(FadeIn(logo.price, scale=0.3), Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(0.8)
        self.clear_scene()

    def queen(self):
        a = tables.BRITISH_ACADEMY_2009.data
        visit = history_card(r"5 November 2008", r"Queen Elizabeth II visits the London School of Economics",
                             r"Professor Luis Garicano shows her a display about the credit crunch", color=E.MISS,
                             width=7.2, font_size=26).to_edge(UP, buff=0.5).shift(LEFT * 2.6)
        ask = quote_card(r"Why had nobody noticed that the credit crunch was on its way?",
                         r"the Queen's question, as the British Academy's letter put it", width=7.0,
                         font_size=30, color=E.MISS).next_to(visit, DOWN, buff=0.35).align_to(visit, LEFT)
        letter = history_card(r"22 July 2009", r"Tim Besley and Peter Hennessy, for the British Academy",
                              r"a letter to the Queen, after a forum of economists, bankers, regulators and "
                              r"officials on 17 June", color=E.SOURCE, width=5.6, font_size=24)
        letter.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=0.4)
        answer = quote_card(r"\dots principally a failure of the collective imagination of many bright people, "
                            r"both in this country and internationally, to understand the risks to the system as a "
                            r"whole.", r"Besley and Hennessy (2009)", width=13.0, font_size=30)
        answer.to_edge(DOWN, buff=0.75)
        src = published_tag(tables.BRITISH_ACADEMY_2009.tag, corner=DR, font_size=18)
        with self.voiceover(
            "A hundred and sixty years later, on the fifth of November 2008, Queen Elizabeth the Second visited the "
            "London School of Economics. The world was in the worst financial crisis since the 1930s. "
            "<bookmark mark='a'/> An economist, Luis Garicano, showed her a display about what had happened, and "
            "she asked the obvious question: why had nobody noticed that it was coming? <bookmark mark='b'/> The "
            "British Academy gathered economists, bankers, regulators and civil servants to answer her, and in July "
            "2009 two of its fellows sent her a letter. <bookmark mark='c'/> Many people, it said, had seen "
            "trouble ahead. But the form it would take, and its timing and its ferocity, were foreseen by nobody. "
            "And it ended like this: the failure was principally a failure of the collective imagination of many "
            "bright people to understand the risks to the system as a whole."
        ) as vo:
            self.play(FadeIn(visit, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(letter, shift=LEFT * 0.2), FadeIn(src))
            vo.wait_until("c")
            self.play(visit.animate.set_opacity(0.35), ask.animate.set_opacity(0.35), FadeIn(answer, shift=UP * 0.2))
        self.clear_scene()

    def two_things(self):
        left = panel(6.2, 4.6, center=[-3.4, -0.3, 0])
        right = panel(6.2, 4.6, center=[3.4, -0.3, 0])
        city = paris(seed=3).scale(0.2).move_to(left.get_center() + UP * 0.1)
        ring = departments(80, seed=2).scale(0.55).move_to(city)
        for d in ring.dots:
            d.scale(0.6)
        lt = label(r"an order nobody designed", font_size=30, color=E.ACCENT).next_to(left, UP, buff=0.2)
        c = load("collapses")
        ax = axes([0, 24], [80, 102], x_length=5.0, y_length=3.0, xticks=[0, 12, 24], yticks=[80, 90, 100],
                  xlabel=r"months after December 2007", font_size=18).move_to(right.get_center() + DOWN * 0.1)
        line = curve(ax.ax, c["months"][:25], c["ip07"][:25], WHITE, stroke_width=4)
        rt = label(r"a failure nobody saw coming", font_size=30, color=E.MISS).next_to(right, UP, buff=0.2)
        ylab = label(r"US industrial production, \ Dec 2007 = 100", font_size=18, color=GREY_A)
        ylab.next_to(ax.ax, UP, buff=0.15).align_to(ax.ax, LEFT)
        src = data_tag(r"Federal Reserve, industrial production (FRED, retrieved 18 Nov 2026)", corner=DR,
                       font_size=17)
        with self.voiceover(
            "So economics has to explain two things at once. <bookmark mark='a'/> An order that nobody designed, "
            "which works well enough to feed a city of a million people, every day, without anyone in charge. "
            "<bookmark mark='b'/> And the same order failing, badly enough to stop the world, in ways that a great "
            "many clever people did not see coming. <bookmark mark='c'/> This series is a course in how economists "
            "study both. It is built from scratch, and it is technical on purpose: every idea is written down as a "
            "model, solved in code that runs, and set against data."
        ) as vo:
            self.play(FadeIn(left), FadeIn(lt), FadeIn(ring), FadeIn(city))
            flows = VGroup(*[flowing(r, GOODS[k % len(GOODS)], n=1, period=2.6 + 0.3 * (k % 4), radius=0.03)
                             for k, r in enumerate(ring.roads) if k % 3 == 0])
            self.add(flows)
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rt), FadeIn(ax), FadeIn(ylab), FadeIn(src))
            self.play(Create(line), run_time=2.5)
            vo.wait_until("c")
            self.wait(0.5)
        for f in flows:
            f.clear_updaters()
        self.clear_scene()

    def three_questions(self):
        rows = VGroup()
        for n, q, a, c in (
            (r"1", r"Who chooses, and facing what?",
             r"what each person, firm and government wants, knows, and cannot do: \ played first by you", E.DEMAND),
            (r"2", r"What happens when the choices meet?",
             r"an equilibrium, derived and computed, \ and a verdict on it: \ who gains, who loses", E.AGORA),
            (r"3", r"How would we know?",
             r"how each number was measured, \ how far the estimates disagree, \ what the forecasts got right",
             E.ACCENT),
        ):
            num = label(n, font_size=72, color=c)
            body = VGroup(label(q, font_size=50, color=c), wrapped_label(a, 11.2, 31, GREY_A))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        head = heading(r"Three questions, for every topic", font_size=40)
        rows.next_to(head, DOWN, buff=0.65)
        with self.voiceover(
            "It puts three questions to every topic. <bookmark mark='a'/> One: who chooses, and facing what? The "
            "people, firms and governments in the story: what each one wants, what each one knows, and what each "
            "one can't do. We'll write that down as mathematics, and often you'll play the part yourself first. "
            "<bookmark mark='b'/> Two: what happens when the choices meet? That's an equilibrium, which we'll derive "
            "and then compute, and then judge: who gains, who loses, and whether anything better was possible. "
            "<bookmark mark='c'/> And three: how would we know? Economists can rarely run the experiment they'd "
            "like to run. So every number the series relies on comes with how it was measured, how far the "
            "estimates disagree, and what happened when someone used it to make a forecast."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 1", font_size=34, color=GREY_B), label(r"Who Feeds Paris?", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"trade in a market where you know only your own card, \ and see where the price goes",
            r"what anything costs when you are alone; \ why two people gain from trade even when one is better at "
            r"everything; \ why a pin factory beats a pin maker",
            r"prices as messages that carry what nobody knows in full; \ incentives that work, and one that "
            r"backfired",
            r"two thousand years of income in one picture; \ what a model is for; \ two times the whole system "
            r"failed",
            r"the economy as plumbing, \ and the devices that run through all sixty-eight parts",
        ], color=E.ACCENT, font_size=32, width=13.0)
        with self.voiceover(
            "Part one: who feeds Paris? <bookmark mark='a'/> You'll trade in a market where you know only your own "
            "card, and watch where the price goes. <bookmark mark='b'/> Then we build an economy from one person "
            "upward: what anything costs when you're alone, why two people gain from trading even when one of them "
            "is better at everything, and why a pin factory makes so many more pins than a pin maker. "
            "<bookmark mark='c'/> We'll see prices carry information that nobody has in full, and incentives that "
            "work, and one that backfired. <bookmark mark='d'/> We'll look at two thousand years of income in a "
            "single picture, at what a model is for, and at two times the whole system failed. "
            "<bookmark mark='e'/> And we'll set up the devices that run through all sixty-eight parts."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
