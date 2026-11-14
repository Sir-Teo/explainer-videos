from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


def chamber(scale=1.0):
    """An operant chamber, drawn: a lever, a food cup, a light and a speaker, and a line to the recorder."""
    walls = Rectangle(width=3.4, height=2.4, stroke_color=GREY_B, stroke_width=3)
    lever = Rectangle(width=0.5, height=0.1, stroke_width=0, fill_color=CS, fill_opacity=1).move_to(
        walls.get_left() + RIGHT * 0.25 + DOWN * 0.2)
    cup = Rectangle(width=0.4, height=0.35, stroke_color=US, stroke_width=3).move_to(walls.get_left() + RIGHT * 0.2 +
                                                                                     DOWN * 0.8)
    light = Circle(radius=0.13, stroke_width=0, fill_color=YOU, fill_opacity=1).move_to(walls.get_left() +
                                                                                       RIGHT * 0.3 + UP * 0.7)
    rat = VGroup(Ellipse(width=0.9, height=0.45, color=WHITE, stroke_width=3),
                 Circle(radius=0.14, color=WHITE, stroke_width=3).shift(LEFT * 0.5 + UP * 0.08)).move_to(
        walls.get_center() + DOWN * 0.7 + RIGHT * 0.3)
    tags = VGroup(label(r"lever", font_size=18, color=CS).next_to(lever, RIGHT, buff=0.1),
                  label(r"food", font_size=18, color=US).next_to(cup, RIGHT, buff=0.1),
                  label(r"light", font_size=18, color=YOU).next_to(light, RIGHT, buff=0.1))
    g = VGroup(walls, lever, cup, light, rat, tags).scale(scale)
    g.lever = lever
    return g


class Skinner(VoiceoverScene):
    def construct(self):
        self.card()
        self.box()
        self.shape()
        self.schedules()
        self.persistence()

    def card(self):
        card = chapter_card(3, r"Skinner's box", r"How do consequences shape behaviour over time?",
                            lit={1938: r"Skinner", 1957: r"Ferster \& Skinner"}, part=PART, scale=("mind",),
                            marr=("what",))
        with self.voiceover("Chapter three. Skinner's box."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def box(self):
        head = heading(r"The operant chamber")
        ch = chamber(1.2).move_to([-3.6, 0.5, 0])
        pen = VGroup(Rectangle(width=4.6, height=2.0, stroke_color=GREY_C, stroke_width=2),
                     label(r"the cumulative recorder", font_size=20, color=GREY_B)).move_to([3.4, 1.4, 0])
        pen[1].next_to(pen[0], UP, buff=0.1)
        steps = VMobject(color=CR, stroke_width=3)
        xs = np.linspace(-2.1, 2.1, 40)
        ys = np.cumsum(np.r_[0, (np.random.default_rng(3).random(39) < 0.6) * 0.04])
        steps.set_points_as_corners([pen[0].get_center() + np.array([x, -0.85 + y, 0]) for x, y in zip(xs, ys)])
        rows = rows_of([
            (r"Skinner, \ 1930s: \ an animal free to respond, \ and a lever that records every press", WHITE),
            (r"operant: \ the behaviour operates on the world; \ its consequences change how often it occurs", CR),
            (r"the recorder's pen steps up at each response: \ the slope is the rate", CS),
        ], 12.4, 27, 0.28).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.FERSTER_SKINNER_1957.cite)
        with self.voiceover(
            "In the 1930s, B. F. Skinner made Thorndike's method automatic. <bookmark mark='a'/> In his chamber a rat "
            "or a pigeon is free to respond whenever it likes, and every press of a lever or peck at a key is "
            "recorded. Food arrives by a rule the experimenter sets. <bookmark mark='b'/> Skinner called this "
            "behaviour operant, because it operates on the world, and its consequences change how often it happens. "
            "Pavlov's responses were elicited by a signal; operant responses are emitted. <bookmark mark='c'/> His "
            "most important instrument was a pen. It moves steadily across a roll of paper and steps up once at "
            "every response, so the slope of the line is the rate of responding. A whole session fits on one "
            "picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(ch.lever, color=CS), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pen), Create(steps), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def shape(self):
        d = load("shaping")
        head = heading(r"Shaping: \ reinforcing successive approximations")
        A = axes([0, 300], [-0.5, 6], x_length=7.4, y_length=3.8, xticks=[0, 100, 200, 300], yticks=[0, 2, 4, 6],
                 xlabel=r"trial", ylabel=r"typical height of the response", center=[-2.4, 0.4, 0])
        ax = A.ax
        x = np.arange(1, 301)
        tgt = DashedLine(ax.c2p(0, d["target"]), ax.c2p(300, d["target"]), color=US, stroke_width=2)
        tl = label(r"the target", font_size=20, color=US).next_to(ax.c2p(300, d["target"]), UP, buff=0.08).shift(LEFT * 0.6)
        c1 = curve(ax, x, d["mu"], CR, stroke_width=4)
        c0 = curve(ax, x, d["mu0"], INHIB, stroke_width=4)
        lg = legend([(CR, rf"successive approximation: \ {pct(d['hit'])} of trials rewarded"),
                     (INHIB, rf"waiting for the target: \ {pct(d['hit0'], 1)} rewarded")], font_size=20)
        lg.next_to(A, DOWN, buff=0.25)
        rows = rows_of([
            (r"a response the animal never makes cannot be reinforced", WHITE),
            (r"so reward whatever comes closest, \ then raise the bar", CR),
            (r"how pigeons were taught to play ping-pong, \ and dogs to guide the blind", CS),
        ], 4.2, 25, 0.36).move_to([4.6, 0.4, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{conditioning.shaping}; \ the criterion is the 60th percentile of the "
                         r"last 20 responses")
        with self.voiceover(
            "How do you teach an animal something it never does? <bookmark mark='a'/> You can't reinforce a response "
            "that doesn't happen. Psyche's rat is to rear up to a height of three, and its rears vary around a height "
            "of zero. <bookmark mark='b'/> If you wait for a three, you'll wait for ever: the red line barely moves, "
            "and almost nothing is rewarded. Instead, reward whatever is better than most recent attempts, and keep "
            "raising the bar. Each reward pulls the typical response toward it, and the green line climbs to the "
            "target and beyond. <bookmark mark='c'/> Skinner called it shaping by successive approximation. It's how "
            "he taught pigeons to play a kind of ping-pong, and how guide dogs, and many human skills, are trained "
            "today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(tgt), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c0), Create(c1), FadeIn(lg), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def schedules(self):
        d = load("schedules")
        head = heading(r"Four schedules, \ four signatures")
        panels = VGroup()
        names = {"FR": r"fixed ratio 20", "VR": r"variable ratio 20", "FI": r"fixed interval 60 s",
                 "VI": r"variable interval 60 s"}
        cols = {"FR": CS, "VR": US, "FI": CR, "VI": CONTEXT}
        centres = {"FR": [-3.4, 1.45, 0], "VR": [3.4, 1.45, 0], "FI": [-3.4, -1.65, 0], "VI": [3.4, -1.65, 0]}
        T = 300.0
        for k in ("FR", "VR", "FI", "VI"):
            keep = d[f"t_{k}"] <= T
            ymax = float(np.ceil(d[f"c_{k}"][keep].max() / 100.0) * 100)
            A = axes([0, T], [0, ymax], x_length=5.2, y_length=2.0, xticks=[0, 100, 200, 300], yticks=[0, ymax],
                     xlabel=r"seconds" if k in ("FI", "VI") else "", ylabel=r"responses" if k in ("FR", "FI") else "",
                     center=centres[k], font_size=17)
            ax = A.ax
            c = curve(ax, d[f"t_{k}"][keep], d[f"c_{k}"][keep], cols[k], stroke_width=3)
            rk = d[f"rf_{k}"] <= T
            ticks = VGroup(*[Line(ax.c2p(t, n) + DOWN * 0.05 + LEFT * 0.05, ax.c2p(t, n) + UP * 0.05 + RIGHT * 0.05,
                                  color=WHITE, stroke_width=2) for t, n in zip(d[f"rf_{k}"][rk], d[f"rf_c_{k}"][rk])])
            name = label(names[k], font_size=21, color=cols[k]).next_to(ax, UP, buff=0.08)
            rate = label(rf"{d[f'rate_{k}']:.0f} a minute", font_size=18, color=GREY_A).move_to(ax.c2p(240, 0.15 * ymax))
            panels.add(VGroup(A, c, ticks, name, rate))
        tag = psyche_tag(r"computed: \ \texttt{conditioning.schedule}; \ the first 5 minutes; \ ticks mark rewards; \ "
                         r"the signatures as Ferster and Skinner describe them")
        with self.voiceover(
            "Skinner and Charles Ferster spent years on a single question: what happens when not every response is "
            "rewarded? The rule that decides which ones are is a schedule of reinforcement, and each leaves its own "
            "signature on the record. Here are Psyche's. <bookmark mark='a'/> On a fixed ratio, every twentieth "
            "press pays. The record is a staircase: a pause after each reward, then a fast run to the next. "
            "<bookmark mark='b'/> On a variable ratio, a press pays at random, one time in twenty on average. "
            "There's no point in pausing, and the rate is the highest of all: this is the slot machine's schedule. "
            "<bookmark mark='c'/> On a fixed interval, the first press after sixty seconds pays. Animals learn the "
            "time. They stop after each reward and speed up as the interval ends, and the record curves upward in a "
            "scallop. <bookmark mark='d'/> On a variable interval, rewards become available at unpredictable times. "
            "The rate is moderate and remarkably steady, which is why it became the workhorse of the laboratory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[3]) for p in panels])
            for m, k in zip("abcd", range(4)):
                vo.wait_until(m)
                p = panels[k]
                self.play(Create(p[1]), FadeIn(p[2]), FadeIn(p[4]), run_time=2.0)
        self.clear_scene()

    def persistence(self):
        head = heading(r"Rewarded sometimes, \ given up slowly")
        rows = rows_of([
            (r"stop all rewards, \ and responding extinguishes, \ as Pavlov's salivation did", WHITE),
            (r"but after a schedule that paid only sometimes, \ it takes far longer: \ the partial reinforcement "
             r"extinction effect", US),
            (r"a run of losses is normal under a ratio schedule, \ so it signals nothing", CS),
            (r"a parent who gives in to tantrums now and then trains the most persistent tantrums", INHIB),
        ], 12.4, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "Schedules also decide what happens when the rewards stop. <bookmark mark='a'/> Take the food away and "
            "pressing extinguishes, as Pavlov's salivation did. <bookmark mark='b'/> But an animal rewarded on every "
            "press gives up quickly, while one rewarded only sometimes keeps going far longer. It's called the "
            "partial reinforcement extinction effect, and it's one of the most reliable findings in the field. "
            "<bookmark mark='c'/> One way to see it: after intermittent reward, a long run of failures is normal, so "
            "it takes a long time to notice that anything has changed. <bookmark mark='d'/> The practical lesson is "
            "uncomfortable. A parent who gives in to a tantrum now and then, but not always, is running a variable "
            "schedule, and trains the most persistent tantrums of all."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
