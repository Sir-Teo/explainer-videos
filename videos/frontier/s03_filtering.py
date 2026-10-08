from __future__ import annotations

from explainer import *  # noqa: F403
from videos.frontier.common import chip, label, load, note, page_card, source

ROWS = [  # (stats key, on-screen stage)
    ("input", r"crawled pages"),
    ("url", r"URL blocklist"),
    ("extract", r"has extractable text"),
    ("lang", r"English (fastText $>0.65$)"),
    ("gopher_rep", r"repetition rules"),
    ("gopher_qual", r"quality rules"),
    ("c4", r"C4 line rules"),
    ("fineweb", r"FineWeb rules"),
]

EXAMPLES = {  # stage -> (URL substring, caption)
    "extract": ("longsboardshop", r"no text at all: a page that only redirects"),
    "gopher_rep": ("assemblergames", r"too many duplicated lines"),
    "gopher_qual": ("motoman", r"fewer than 50 words"),
    "c4": ("glenwaverleyelectrician", r"contains a curly bracket: template syntax left in"),
    "fineweb": ("coursehandbook.mq", r"few lines end in punctuation: navigation menus"),
}
FALSE_POSITIVE = "codebricks.io/blog/cat-and-mouse"


class Filtering(VoiceoverScene):
    def construct(self):
        self.f = load("funnel")
        self.build_funnel()
        self.early_stages()
        self.rules()
        self.false_positive()
        self.summary()

    # ------------------------------------------------------------------
    def example(self, stage: str, sub: str):
        ex = next(e for e in self.f["examples"][stage] if sub in e["url"])
        return ex

    def card_for(self, stage):
        sub, cap = EXAMPLES[stage]
        ex = self.example(stage, sub)
        card = page_card(ex["text"], ex["url"], width=5.6, lines=7, chars=44, font_size=16, color=C.REMOVED)
        reason = chip(ex["reason"].replace("_", " "), color=C.REMOVED, font_size=20, mono=True)
        caption = label(cap, font_size=24, color=GREY_A)
        g = VGroup(card, reason, caption).arrange(DOWN, buff=0.18)
        g.move_to(RIGHT * 3.55 + DOWN * 0.3)
        if g.height > 6.4:
            g.scale_to_fit_height(6.4)
        return g

    # ------------------------------------------------------------------
    def build_funnel(self):
        st = self.f["stats"]
        n0 = st["input"]["docs"]
        self.n0 = n0
        maxw = 3.7
        rows = VGroup()
        for key, name in ROWS:
            n = st[key]["docs"]
            nm = label(name, font_size=24, color=GREY_A)
            bar = Rectangle(width=maxw * n / n0, height=0.36, stroke_width=0, fill_color=C.KEPT, fill_opacity=0.85)
            cnt = label(f"{n:,}".replace(",", "{,}"), font_size=24)
            rows.add(VGroup(nm, bar, cnt))
        x_bar = -5.3
        for i, r in enumerate(rows):
            y = 2.6 - i * 0.72
            r[1].move_to([x_bar, y, 0], aligned_edge=LEFT)
            r[0].next_to(r[1], UP, buff=0.06).align_to(r[1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.12)
        self.rows = rows
        title = label(r"The FineWeb recipe, run on 10{,}498 real pages", font_size=34).to_edge(UP, buff=0.3)
        title.set_x(0)
        self.title = title
        src = source(r"filters: Hugging Face \texttt{datatrove} (FineWeb's own code), defaults as in FineWeb")
        self.src = src
        with self.voiceover(
            "Next, filtering. We took the exact recipe behind FineWeb, Hugging Face's open web dataset of fifteen "
            "trillion tokens, and ran their own code on those ten thousand pages. <bookmark mark='r'/> Here's how "
            "many pages survive each step."
        ) as vo:
            self.play(FadeIn(title), FadeIn(src))
            vo.wait_until("r")
            self.play(FadeIn(rows[0]))

    def reveal(self, i, run_time=0.8):
        r = self.rows[i]
        prev = self.rows[i - 1][1]
        ghost = prev.copy().set_fill(C.REMOVED, opacity=0.5).move_to(r[1], aligned_edge=LEFT)
        self.add(ghost)
        self.play(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1]), ghost.animate.set_opacity(0).shift(RIGHT * 0.3),
                  run_time=run_time)
        self.remove(ghost)

    # ------------------------------------------------------------------
    def early_stages(self):
        st = self.f["stats"]
        n_url = st["input"]["docs"] - st["url"]["docs"]
        assert 50 < n_url < 120
        ex = self.example("extract", EXAMPLES["extract"][0])
        html = ex["text"].strip()
        assert html.startswith("<!DOCTYPE html>") and "location.href" in html
        en = st["lang"]["docs"] / st["extract"]["docs"]
        assert 0.30 < en < 0.36
        bl = label(r"blocklist: 4.56 million domains\\(adult content, malware, spam)", font_size=26, color=GREY_A)
        bl.move_to(RIGHT * 3.5 + UP * 1.2)
        card = self.card_for("extract")

        with self.voiceover(
            "First, a blocklist of four and a half million domains removes adult sites, malware and spam. "
            "<bookmark mark='x'/> Pages with no extractable text go next, like this one, which does nothing but "
            "redirect your browser. <bookmark mark='l'/> Then a language classifier keeps only pages that are "
            "confidently English: about a third of what's left."
        ) as vo:
            self.reveal(1)
            self.play(FadeIn(bl))
            vo.wait_until("x")
            self.play(FadeOut(bl), FadeIn(card, shift=LEFT * 0.3))
            self.reveal(2)
            vo.wait_until("l")
            self.play(FadeOut(card))
            self.reveal(3)

    # ------------------------------------------------------------------
    def rules(self):
        rule_text = {
            "gopher_rep": r"Gopher repetition: $>30\%$ duplicated lines, top 2-gram $>20\%$ of characters, \dots",
            "gopher_qual": r"Gopher quality: 50--100{,}000 words; $\geq 80\%$ of words contain a letter; at least 2 of \emph{the, be, to, of, and, that, have, with}",
            "c4": r"C4: drop lines without terminal punctuation; drop pages containing ``lorem ipsum'' or \{",
            "fineweb": r"FineWeb: $<12\%$ of lines end in punctuation, $>67\%$ of lines under 30 characters, too many duplicated lines",
        }
        narr = {
            "gopher_rep": "Then come rules written by hand. Repetition rules, from DeepMind's Gopher paper, drop pages "
                          "where too many lines, paragraphs or phrases repeat, like this forum index: zero replies, "
                          "last post by Archive, over and over.",
            "gopher_qual": "Quality rules drop pages with fewer than fifty words, or where too few words contain a "
                           "letter, or that lack ordinary words like the and and. Like this login form.",
            "c4": "Rules from Google's C4 dataset drop lines that don't end in punctuation, and any page with lorem "
                  "ipsum or a curly bracket in it: a sign of code or templates. This page is spun advertising text "
                  "with its template syntax still showing.",
            "fineweb": "And FineWeb added three rules of its own, chosen by training small models on the output: drop "
                       "pages where few lines end in punctuation, where most lines are very short, or where many lines "
                       "repeat. Menus and navigation, mostly.",
        }
        for i, key in enumerate(["gopher_rep", "gopher_qual", "c4", "fineweb"], start=4):
            card = self.card_for(key)
            rule = label(rule_text[key], font_size=22, color=C.EDU)
            if rule.width > 13.2:
                rule.width = 13.2
            rule.to_edge(DOWN, buff=0.25)
            with self.voiceover(narr[key]) as vo:
                self.play(FadeOut(self.src), FadeIn(rule), FadeIn(card, shift=LEFT * 0.3), run_time=0.8)
                self.reveal(i)
            self.play(FadeOut(card), FadeOut(rule), run_time=0.5)

    # ------------------------------------------------------------------
    def false_positive(self):
        ex = self.example("gopher_qual", FALSE_POSITIVE)
        assert ex["reason"] == "gopher_below_alpha_threshold"
        card = page_card(ex["text"], ex["url"], width=5.6, lines=7, chars=44, font_size=16, color=C.EDU)
        reason = chip("gopher below alpha threshold", color=C.REMOVED, font_size=20, mono=True)
        cap = label(r"a programming puzzle, thrown out by mistake", font_size=24, color=GREY_A)
        g = VGroup(card, reason, cap).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.55 + DOWN * 0.3)
        with self.voiceover(
            "These rules are blunt. This page, a programming puzzle full of symbols, was thrown out for having too "
            "few real words. At web scale that's an acceptable trade: losing some good pages costs far less than "
            "training on bad ones."
        ):
            self.play(FadeIn(g, shift=LEFT * 0.3))
        self.play(FadeOut(g))

    # ------------------------------------------------------------------
    def summary(self):
        st = self.f["stats"]
        frac_docs = st["fineweb"]["docs"] / st["input"]["docs"]
        frac_bytes = st["fineweb"]["bytes"] / st["input"]["bytes"]
        assert 0.12 < frac_docs < 0.14 and 0.0030 < frac_bytes < 0.0040
        box = SurroundingRectangle(self.rows[-1], color=C.KEPT, buff=0.12, corner_radius=0.08)
        res = VGroup(
            label(rf"{100 * frac_docs:.0f}\% of pages survive", font_size=36, color=C.KEPT),
            label(rf"holding {100 * frac_bytes:.2f}\% of the original bytes", font_size=30, color=GREY_A),
            label(r"FineWeb: the same recipe (plus deduplication)\\over 96 crawls $\rightarrow$ 15 trillion tokens",
                  font_size=28),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.5 + DOWN * 0.2)
        with self.voiceover(
            "In the end, thirteen percent of the pages survive, holding about a third of a percent of the original "
            "bytes. <bookmark mark='f'/> FineWeb ran this, plus deduplication, over ninety-six crawls, and ended up "
            "with fifteen trillion tokens."
        ) as vo:
            self.play(Create(box), FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("f")
            self.play(FadeIn(res[2]))
        self.wait(0.6)
        self.clear_scene()
