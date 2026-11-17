from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.small()
        self.need()
        self.decoding()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: how many people does a brain study need?",
                            r"What can 25 people show, and what takes 25,000?", lit={2022: r"brain-wide associations"},
                            part=PART, scale=("brain", "person"), marr=("how",))
        with self.voiceover(
            "Chapter fourteen. Frontier: how many people does a brain study need?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def small(self):
        p = load("power")
        m = archive.MAREK_2022.data
        head = heading(r"2022: \ the links between brain measures and behaviour are small")
        A = axes([-0.8, 0.8], [0, 0.065], x_length=6.6, y_length=3.5, xticks=[-0.8, -0.4, 0, 0.4, 0.8], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=rf"the correlation one study of {p['n']} people reports", ylabel=r"",
                 center=[-3.3, -0.6, 0])
        ax = A.ax
        h = hist(ax, p["edges"], p["small_hist"], NOISE, opacity=0.7)
        cuts = VGroup(*[DashedLine(ax.c2p(s * p["critical"], 0), ax.c2p(s * p["critical"], 0.062), color=THRESH,
                                   stroke_width=2.5) for s in (-1, 1)])
        truth = Line(ax.c2p(p["small_r"], 0), ax.c2p(p["small_r"], 0.062), color=MODEL, stroke_width=4)
        tl = label(rf"the truth: \ {p['small_r']:.2f}", font_size=24, color=MODEL).next_to(ax.c2p(p["small_r"], 0.062), UP, buff=0.05)
        cl = label(r"``significant'' beyond these lines", font_size=22, color=THRESH).next_to(A, UP, buff=0.42).shift(RIGHT * 1.6)
        rows = rows_of([
            (rf"about {fmt_int(m['people'])} people in three datasets: \ the typical link has $r$ near "
             rf"{m['median_r']:.2f}", DATA),
            (rf"the typical study had about {m['median_n']} people", DATA),
            (rf"with {p['n']} people and a true $r$ of {p['small_r']:.2f}: \ {pct(p['small_power'])} of studies "
             r"reach significance", WHITE),
            (rf"and those report $r = {r2(p['small_sig'])}$ on average, \ {p['inflation_small']:.0f} times too "
             rf"large; \ {pct(p['small_wrong'])} have the wrong sign", BAD),
        ], 5.0, 27, 0.26).move_to([4.45, -0.4, 0])
        keep_in_frame(rows)
        src = published_tag(archive.MAREK_2022.cite)
        tag = psyche_tag(r"histogram: simulated studies (Psyche)")
        few = VGroup(*[Dot(radius=0.12, color=NOISE) for _ in range(m["median_n"])]).arrange_in_grid(rows=5, buff=0.16)
        few.move_to([-4.9, 0.3, 0])
        few_l = label(rf"the typical study: \ {m['median_n']} people", font_size=28, color=NOISE).next_to(few, DOWN, buff=0.3)
        many = Rectangle(width=3.5, height=3.1, stroke_width=0, fill_color=DATA, fill_opacity=0.55).move_to([-0.6, 0.3, 0])
        many_l = VGroup(label(rf"the 2022 study: \ about {fmt_int(m['people'])}", font_size=28, color=DATA),
                        label(r"(not drawn to scale)", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.1)
        many_l.next_to(many, DOWN, buff=0.25)
        opening = VGroup(few, few_l, many, many_l)
        with self.voiceover(
            "The frontier of this part is a number: how many people a study needs. For twenty years the "
            "typical study relating a brain measure to a trait, an ability or a diagnosis had about "
            f"{m['median_n']} people. <bookmark mark='a'/> In 2022 a large group put three very big "
            f"datasets together, about {m['people']:,} people, and asked how strong those links "
            f"really are. The typical one has a correlation near {m['median_r']:.2f}. Even the strongest "
            "are small. <bookmark mark='b'/> Now see what that does to a small study. Here are "
            f"twenty thousand simulated studies of {p['n']} people each, of a link whose true size is "
            f"{p['small_r']:.2f}, which would be one of the stronger ones. Their results scatter widely, "
            f"because {p['n']} people can't pin a correlation down. <bookmark mark='c'/> Only "
            f"{100 * p['small_power']:.0f} percent reach significance, barely more than chance. "
            "<bookmark mark='d'/> And look at which ones those are. To be significant with "
            f"{p['n']} people, a correlation has to be at least {p['critical']:.2f}. So the studies that "
            f"get published report {p['small_sig']:.2f} on average, about "
            f"{p['inflation_small']:.0f} times the truth, and nearly one in five of them has the sign "
            "wrong. It's Part 4's filter, with a scanner attached."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            self.play(FadeIn(few, lag_ratio=0.05), FadeIn(few_l), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(many), FadeIn(many_l), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(opening), run_time=0.5)
            self.play(FadeIn(A), FadeIn(h, lag_ratio=0.02), Create(truth), FadeIn(tl), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(cuts), FadeIn(cl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def need(self):
        p = load("power")
        e = archive.ELLIOTT_2020.data
        head = heading(r"So how many?")
        cells = VGroup(
            big_number(fmt_int(p["usual_need"]), rf"people, if the true $r$ is {p['usual_r']:.1f}", MODEL, 84, 3.9, 30),
            big_number(fmt_int(p["small_need"]), rf"if it is {p['small_r']:.2f}", THRESH, 84, 3.9, 30),
            big_number(fmt_int(round(p["tiny_need"], -3)), rf"if it is {p['tiny_r']:.2f}", BAD, 84, 3.9, 30),
        ).arrange(RIGHT, buff=1.0).move_to([0, 1.1, 0])
        cap = label(r"for an 80\% chance of detecting the link", font_size=26, color=GREY_A).next_to(cells, UP, buff=0.3)
        rows = rows_of([
            (rf"part of the reason the links are small: \ the brain measures are noisy. \ Task fMRI's "
             rf"test-retest reliability averages {e['icc']:.1f} over {e['experiments']} experiments", DATA),
            (r"the reply: \ models that combine many brain measures, \ tested on new people, \ do better with "
             r"fewer people. \ How much better is being argued now.", WHITE),
            (r"What a small study \emph{can} do: \ an experiment within each person, \ where the effect is "
             r"large. \ That is what the first chapters of this part were.", P.ACCENT),
        ], 12.6, 29, 0.26).move_to([0, -1.9, 0])
        src = published_tag(archive.ELLIOTT_2020.cite)
        tag = psyche_tag(r"sample sizes: computed")
        with self.voiceover(
            "So how many people does it take? That's a calculation, for an eighty percent chance of "
            f"detecting the link. <bookmark mark='a'/> If the true correlation is {p['usual_r']:.1f}, "
            f"which is what small studies used to report, about {p['usual_need']:,} people. "
            f"<bookmark mark='b'/> If it's {p['small_r']:.2f}, about {round(p['small_need'], -2):,.0f}. "
            f"If it's {p['tiny_r']:.2f}, the typical value, nearly eighty thousand. "
            "<bookmark mark='c'/> Part of the reason the links are so small is the instrument. When the "
            "reliability of common brain-scan measures was added up, the average was about "
            f"{e['icc']:.1f}. You saw in chapter nine what that does to any correlation. "
            "<bookmark mark='d'/> There's a reply, and it's a fair one. Models that combine thousands of "
            "brain measures at once, and are tested on people they've never seen, find stronger links with "
            "fewer people. How much stronger is being argued as this is made. <bookmark mark='e'/> And "
            "don't over-learn the lesson. Small studies aren't useless. A handful of people is plenty when "
            "each one is their own control and the effect is large: the tuning curve, the N400, the map of "
            "the visual field. What twenty-five people can't tell you is how brains differ between "
            "people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(cells[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cells[1], shift=UP * 0.1), FadeIn(cells[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def decoding(self):
        t = archive.TANG_2023.data
        head = heading(r"2023: \ the gist of a story, read from a scanner")
        heard = quote_card(r"what the person heard: \ a story, \ in someone's own words", r"spoken aloud in the scanner room",
                           width=5.8, font_size=28, color=EEGC).move_to([-3.5, 1.0, 0])
        out = quote_card(r"what the decoder wrote: \ different words, \ much of the same meaning",
                         r"from the blood-flow signal alone", width=5.8, font_size=28, color=BLOOD).move_to([3.5, 1.0, 0])
        arrow = Arrow(heard.get_right(), out.get_left(), buff=0.1, color=GREY_B, stroke_width=4)
        rows = rows_of([
            (rf"{t['participants']} people, \ each scanned for about {t['hours']} hours while listening to "
             r"stories, \ to train a model of \emph{their} brain", WHITE),
            (r"it recovers the gist, not the words; \ it also works, more weakly, on a story the person only "
             r"imagines telling", MODEL),
            (r"it needs the person's cooperation: \ when they deliberately thought of something else, \ it failed", THRESH),
            (r"This is chapter ten's honest version: \ a model, \ tested on new data, \ with a score.", P.ACCENT),
        ], 12.6, 29, 0.24).move_to([0, -1.75, 0])
        src = published_tag(archive.TANG_2023.cite)
        tag = note(r"the cards describe the result; they do not quote it").to_corner(DR, buff=0.15)
        with self.voiceover(
            "And here's what the honest kind of mind reading looks like when it works. "
            f"<bookmark mark='a'/> In 2023 a group in Texas scanned {t['participants']} people for about "
            f"{t['hours']} hours each while they listened to stories, and trained a model, for each "
            "person, to predict that person's brain activity from the meaning of the words. Then they ran "
            "it backwards on a new story. <bookmark mark='b'/> The decoder doesn't recover the words. The "
            "blood is far too slow for that. It recovers the gist: a paraphrase, often close in meaning, "
            "in different words. It does the same, more weakly, when the person only imagines telling a "
            "story. <bookmark mark='c'/> And it has limits that matter. It needs many hours of that "
            "person's own data. A model trained on one person doesn't read another. And it needs their "
            "cooperation: when the participants deliberately thought about something else, it failed. "
            "<bookmark mark='d'/> So it's a real advance, and it's exactly the shape chapter ten asked "
            "for. A model, a test on new data, and a score. It's also the reason people have started to "
            "write about the privacy of a brain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(heard), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(out), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def open(self):
        head = heading(r"What is not settled")
        items = [
            (r"How far can the small links be strengthened?",
             r"Better measures, longer scans of each person, and models tested on new people.", THRESH),
            (r"Can a scan say anything useful about one person?",
             r"Group averages are solid. \ A diagnosis or a prediction for an individual mostly is not yet.", BLOOD),
            (r"What is between the blood and the thought?",
             r"A voxel holds hundreds of thousands of neurons. \ A map of where is not a theory of how.", EEGC),
            (r"Who may read a brain, and with whose consent?",
             r"The decoders need cooperation today. \ The question is being asked before they do not.", P.ACCENT),
        ]
        rows = VGroup()
        for q, a, col in items:
            rows.add(VGroup(wrapped_label(q, 12.6, 34, col), wrapped_label(a, 12.6, 29, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.1, 0])
        keep_in_frame(rows)
        star = wrapped_label(r"$\star$ \ Problem 7: \ design the study that could show a brain measure predicts "
                             r"something about one person that their behaviour does not.", 12.6, 29, P.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So here's what isn't settled. <bookmark mark='a'/> How far can those small links be "
            "strengthened? By better measures, by scanning each person for much longer, and by models "
            "tested on new people. Nobody knows yet where the ceiling is. <bookmark mark='b'/> Can a scan "
            "say anything useful about one person? Averages over groups are solid. A diagnosis, or a "
            "forecast, for an individual mostly isn't there yet. <bookmark mark='c'/> What lies between "
            "the blood and the thought? A single voxel holds hundreds of thousands of neurons. A map of "
            "where things happen isn't a theory of how. That's most of the rest of this series. "
            "<bookmark mark='d'/> And who may read a brain? Today's decoders need the person's help. The "
            "question of consent is being asked now, before they don't. <bookmark mark='e'/> The starred "
            "problem asks you to design a study that could show a brain measure tells you something about "
            "a person that their behaviour doesn't."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(star, shift=UP * 0.1))
        self.clear_scene()
