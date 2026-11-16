from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Pay(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"Pay, \ and what money crowds out", r"Does paying for performance get performance?")
        self.safelite()
        self.daycare()

    def safelite(self):
        rows_section(self, r"Paying by the windshield", [
            (r"1990s: \ an American auto-glass company moved its installers from hourly wages to pay per windshield "
             r"installed, \ with a guaranteed minimum", WHITE),
            (r"Edward Lazear's analysis of the company's records: \ output per worker rose by about 44\%", GOOD),
            (r"about half came from the same workers working harder, \ and about half from who joined and stayed: \ "
             r"incentives sort people as well as move them", MODEL),
            (r"where output is easy to count and quality easy to check, \ piece rates work; \ where it is not, \ "
             r"they reward the wrong things (chapter ten's narrow targets)", PERSON),
        ], "Does paying for performance get performance? <bookmark mark='a'/> In the nineteen nineties an American "
           "auto-glass company moved its installers from hourly wages to pay per windshield, with a guaranteed "
           "minimum. <bookmark mark='b'/> Edward Lazear analysed the company's records. Output per worker rose by "
           "about forty-four percent. <bookmark mark='c'/> About half came from the same workers working harder, and "
           "about half from who joined and who stayed. Incentives sort people as well as move them. "
           "<bookmark mark='d'/> Where output is easy to count and quality easy to check, piece rates work. Where "
           "it isn't, they reward the wrong things.", tag=published_tag(r"Lazear (2000)"))

    def daycare(self):
        rows_section(self, r"A fine is a price", [
            (r"Israel, \ late 1990s: \ ten daycare centres; \ in six, \ a small fine for parents who picked up their "
             r"children late", WHITE),
            (r"late pick-ups did not fall: \ they rose, \ to roughly twice the earlier level", AUTH),
            (r"when the fine was removed, \ lateness stayed high", PERSON),
            (r"Uri Gneezy and Aldo Rustichini's reading: \ the fine turned a social obligation into a price, \ and a "
             r"cheap one; \ money crowded out the norm", MODEL),
            (r"one striking field experiment, \ widely cited, \ not replicated at scale: \ the Ledger says so", YOU),
        ], "Money can also crowd out what it replaces. <bookmark mark='a'/> In Israel in the late nineteen nineties, "
           "ten daycare centres were studied, and six of them introduced a small fine for parents who picked up their "
           "children late. <bookmark mark='b'/> Late pick-ups didn't fall. They rose, to roughly twice the earlier "
           "level. <bookmark mark='c'/> And when the fine was removed, lateness stayed high. <bookmark mark='d'/> Uri "
           "Gneezy and Aldo Rustichini's reading: the fine turned a social obligation into a price, and a cheap one. "
           "Money crowded out the norm. <bookmark mark='e'/> It's one striking field experiment, widely cited, and "
           "not replicated at scale. The Ledger says so.", tag=published_tag(r"Gneezy \& Rustichini (2000)"))
