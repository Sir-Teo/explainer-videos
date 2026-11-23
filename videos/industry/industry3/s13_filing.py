from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403

ITEMS = [("Item 1", "Business", "what it sells, its segments, rivals, employees"),
         ("Item 1A", "Risk factors", "what management is required to warn about"),
         ("Item 7", "Management's discussion", "why the numbers moved; liquidity; adjusted measures"),
         ("Item 8", "Financial statements", "the three statements, the auditor's report"),
         ("Notes", "Notes to the statements", "segments, revenue by product and place, leases, debt"),
         ("Exhibits", "Exhibit 21 and others", "subsidiaries, major contracts")]

FOUND = [("Costco's members and warehouses", "Item 7 and Item 1", "cost"),
         ("Delta's seat miles and American Express", "Item 7, operating statistics", "dal"),
         ("Microsoft's OpenAI gains", "Note on other income", "msft"),
         ("JPMorgan's deposits and capital", "Item 7, selected financial data", "jpm")]


class Filing(VoiceoverScene):
    def construct(self):
        card(self, 12, "Reading a 10-K", "Where in a company's annual report are the answers?",
             "Chapter twelve. Reading a 10-K.", lit=("unit", "moat"))
        doc = RoundedRectangle(corner_radius=0.1, width=5.2, height=6.0, fill_color="#F3F1EA", fill_opacity=1,
                               stroke_width=0).move_to(LEFT * 3.6 + DOWN * 0.15)
        title = VGroup(TB("FORM 10-K", 26, "#1B1F27"), T("Annual report under the Securities Exchange Act", 13,
                                                         "#4A5263")).arrange(DOWN, buff=0.05).move_to(
            doc.get_top() + DOWN * 0.55)
        rows = VGroup()
        for k, (code, nm, what) in enumerate(ITEMS):
            y = doc.get_top()[1] - 1.35 - k * 0.72
            r = VGroup(TB(code, 17, "#1B1F27").move_to(np.array([doc.get_left()[0] + 0.25, y, 0]), aligned_edge=LEFT),
                       T(nm, 17, "#1B1F27").move_to(np.array([doc.get_left()[0] + 1.55, y, 0]), aligned_edge=LEFT))
            rows.add(r)
        notes = VGroup()
        for k, (code, nm, what) in enumerate(ITEMS):
            n = T(what, 17, I.TEXT).move_to(np.array([0.2, rows[k].get_center()[1], 0]), aligned_edge=LEFT)
            if n.width > 6.6:
                n.scale_to_fit_width(6.6)
            arrow = Arrow(np.array([doc.get_right()[0] - 0.05, rows[k].get_center()[1], 0]),
                          np.array([0.1, rows[k].get_center()[1], 0]), buff=0.05, color=I.FAINT, stroke_width=1.5,
                          max_tip_length_to_length_ratio=0.15)
            notes.add(VGroup(arrow, n))
        src = source("SEC EDGAR; the filings of this part's six companies", size=13)
        with self.voiceover(
            "Every American public company files an annual report with the Securities and Exchange Commission, "
            "the 10-K, free to anyone on the SEC's website. <bookmark mark='a'/> It always has the same parts. Item "
            "one, the business: what it sells, how it is organized, who it competes with, how many people it "
            "employs. <bookmark mark='b'/> Item one A, the risks the company is required to warn investors about. "
            "<bookmark mark='c'/> Item seven, management's discussion: why the numbers moved, where the cash came "
            "from, and the company's own adjusted measures, reconciled to the official ones. <bookmark mark='d'/> "
            "Item eight, the statements themselves, with the auditor's opinion. <bookmark mark='e'/> Then the notes, "
            "which is where the business underneath is described in numbers: sales by segment, product and country, "
            "leases, debt and when it falls due. <bookmark mark='f'/> And the exhibits, down to the list of "
            "subsidiaries. Between annual reports, companies file a shorter quarterly report, the 10-Q, and a "
            "brief 8-K whenever something important happens, as Enron did when it restated its profits in November "
            "2001."
        ) as vo:
            self.play(FadeIn(doc), FadeIn(title), FadeIn(src))
            for i, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(rows[i]), FadeIn(notes[i], shift=LEFT * 0.1), run_time=0.8)
        self.clear_scene()
        self.found()

    def found(self):
        rows = VGroup()
        for k, (what, where, key) in enumerate(FOUND):
            rows.add(VGroup(Dot(radius=0.08, color=CO[key]), TB(what, 21, I.TEXT), T(where, 18, I.DIM)).arrange(
                RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.4)
        tip = VGroup(T("Every number in the statements is also tagged in machine-readable form", 19, I.ACCENT),
                     T("data.sec.gov: this series reads its figures from there, and cites each one", 19, I.ACCENT)
                     ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.7)
        head = T("Where this part found its numbers", 24, I.TEXT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Every company figure in this part came from those pages. <bookmark mark='a'/> Costco's members and "
            "warehouses are in its business section and its discussion. Delta's seat miles and its American "
            "Express payments, in its operating statistics. Microsoft's paper gains on OpenAI, in a note on other "
            "income. JPMorgan's deposits and capital, in its selected financial data. <bookmark mark='b'/> And "
            "every number in the statements is also published as tagged data, which is how this series reads them, "
            "and why each one on screen carries its source and its date."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(tip))
        self.clear_scene()
