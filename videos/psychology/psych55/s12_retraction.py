from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Retraction(VoiceoverScene):
    def construct(self):
        card_section(self, 11, r"A nudge that never was", r"What happens when a celebrated nudge was never real?",
                     scale=("society",))
        self.story()
        self.overload()

    def story(self):
        rows_section(self, r"Signing at the top", [
            (r"2012: \ a paper reported that signing an honesty pledge at the top of a form, \ not the bottom, \ "
             r"reduced cheating, \ including in an insurer's mileage reports", WHITE),
            (r"it was cited in government guidance and copied into forms", MODEL),
            (r"2020: \ the original authors and others ran a large replication: \ no effect", AUTH),
            (r"2021: \ analysts showed the mileage data were fabricated (Part 50's chapter on fraud); \ the paper was "
             r"retracted", AUTH),
            (r"the field's safeguards worked eventually: \ a replication and open data", GOOD),
        ], "What happens when a celebrated nudge was never real? <bookmark mark='a'/> In 2012 a paper reported that "
           "signing an honesty pledge at the top of a form, rather than the bottom, reduced cheating, including in an "
           "insurer's mileage reports. <bookmark mark='b'/> It was cited in government guidance and copied into "
           "forms. <bookmark mark='c'/> In 2020 the original authors and others ran a large replication, and found no "
           "effect. <bookmark mark='d'/> In 2021 analysts showed that the mileage data were fabricated, as Part 50 "
           "described, and the paper was retracted. <bookmark mark='e'/> The field's safeguards did work, "
           "eventually: a replication, and open data.", tag=published_tag(r"Kristal et al.\ (2020)"))

    def overload(self):
        rows_section(self, r"Too many jams?", [
            (r"Iyengar and Lepper, \ 2000: \ shoppers offered 24 jams stopped more often but bought far less often "
             r"than those offered 6", WHITE),
            (r"choice overload became a design rule: \ fewer options sell more", MODEL),
            (r"Scheibehenne and colleagues' 2010 meta-analysis: \ an average effect near zero, \ with wide variation",
             AUTH),
            (r"Chernev and colleagues: \ overload appears when choosers lack preferences, \ options are hard to "
             r"compare, \ or the decision is complex: \ conditions, \ not a law", PERSON),
        ], "Another famous result has been contested rather than retracted. <bookmark mark='a'/> In 2000 Sheena "
           "Iyengar and Mark Lepper found that shoppers offered twenty-four jams stopped more often, but bought far "
           "less often, than those offered six. <bookmark mark='b'/> Choice overload became a design rule: fewer "
           "options sell more. <bookmark mark='c'/> But in 2010 Benjamin Scheibehenne and colleagues' meta-analysis "
           "found an average effect near zero, with wide variation. <bookmark mark='d'/> Alexander Chernev and "
           "colleagues found that overload appears when choosers lack clear preferences, when options are hard to "
           "compare, or when the decision is complex. Conditions, not a law.",
           tag=published_tag(r"Iyengar \& Lepper (2000)"))
