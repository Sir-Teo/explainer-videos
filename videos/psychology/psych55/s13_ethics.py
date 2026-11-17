from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Ethics(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Ethics and limits", r"Who decides which way to steer?", scale=("society",))
        self.autonomy()
        self.frame()

    def autonomy(self):
        chips_section(self, r"Autonomy, \ transparency and sludge", [
            (r"libertarian paternalism", r"Thaler and Sunstein's defence: \ steer, \ but leave every option open and "
                                         r"cheap to choose", MODEL),
            (r"transparency", r"a nudge that would fail if disclosed is closer to manipulation; \ most defaults survive "
                              r"disclosure", GOOD),
            (r"sludge", r"friction that steers people against their interest: \ cancellations by phone only, \ "
                        r"rebates that need a form and a stamp (Part 52's dark patterns)", AUTH),
            (r"who benefits", r"the same tool serves a pension saver or a subscription seller", PERSON),
        ], "Who decides which way to steer? <bookmark mark='a'/> Thaler and Sunstein's defence was libertarian "
           "paternalism: steer, but leave every option open and cheap to choose. <bookmark mark='b'/> Transparency is "
           "one test. A nudge that would fail if disclosed is closer to manipulation, and most defaults survive "
           "disclosure. <bookmark mark='c'/> Sludge is the reverse: friction that steers people against their own "
           "interest, like cancellations by phone only, or rebates that need a form and a stamp. Those are Part 52's "
           "dark patterns. <bookmark mark='d'/> And who benefits: the same tool serves a pension saver or a "
           "subscription seller.")

    def frame(self):
        rows_section(self, r"The individual frame and the system", [
            (r"Chater and Loewenstein, \ 2023: \ behavioural science focused on nudging individuals, \ and so helped "
             r"frame problems like obesity, \ pensions and carbon as personal failings", WHITE),
            (r"their argument: \ the largest changes come from rules, \ prices and products, \ the system frame, \ "
             r"and nudges can distract from them", AUTH),
            (r"their critics: \ the two frames are complements; \ psychology also designs better rules", MODEL),
            (r"for a practitioner: \ ask whether the problem is the person's choice, \ or the choices they are given",
             YOU),
        ], "There's a larger criticism. <bookmark mark='a'/> In 2023 Nick Chater and George Loewenstein argued that "
           "behavioural science focused on nudging individuals, and so helped frame problems like obesity, pensions "
           "and carbon as personal failings. <bookmark mark='b'/> The largest changes, they argued, come from rules, "
           "prices and products, the system frame, and nudges can distract from them. <bookmark mark='c'/> Their "
           "critics replied that the two frames are complements, and that psychology also designs better rules. "
           "<bookmark mark='d'/> For a practitioner the question is whether the problem is the person's choice, or "
           "the choices they're given.", tag=published_tag(r"Chater \& Loewenstein (2023)"))
