from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ digital runs, \ narrow banks, \ stablecoins", r"Are runs faster now, \ and can "
             r"money be made unrunnable?", "Chapter fifteen. Frontier: digital runs, narrow banks, stablecoins.",
             lit={1933: r"the Chicago Plan", 2023: r"digital runs"}, scale=("firm", "nation"), horizon=("an hour",))
        self.speed()
        self.weekend()
        self.narrow()
        self.open_()

    def speed(self):
        s = load("svb")
        rows = VGroup(
            label(rf"Silicon Valley Bank: \ \${s['withdrawn_mar9'] / 1e9:.0f} billion in a day, \ "
                  rf"\${s['requested_mar10'] / 1e9:.0f} billion more queued overnight", font_size=23, color=RUN),
            label(r"a run used to need a queue on the pavement; \ now it needs a phone", font_size=23, color=GREY_A),
            label(r"and a crowd that talks: \ start-up founders, \ their investors, \ on social media", font_size=23,
                  color=DEPOSIT),
            label(r"Cookson and coauthors, \ 2023: \ banks most discussed on Twitter before the run lost more of "
                  r"their stock-market value", font_size=21, color=E.ACCENT),
            label(r"beyond what their losses and uninsured deposits predict", font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Cookson, \ Fox, \ Gil-Bazo, \ Imbet and Schiller, \ ``Social media as a bank run "
                            r"catalyst'' (2023)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier begins with speed. <bookmark mark='a'/> Silicon Valley Bank lost "
            f"{s['withdrawn_mar9'] / 1e9:.0f} billion dollars in one day, and was asked for "
            f"{s['requested_mar10'] / 1e9:.0f} billion more overnight. <bookmark mark='b'/> A run used to need a "
            "queue on the pavement. Now it needs a phone. <bookmark mark='c'/> And a crowd that talks: the bank's "
            "depositors were start-up founders and their investors, many of them connected on social media. "
            "<bookmark mark='d'/> Anthony Cookson and his coauthors found that banks that had been discussed most "
            "on Twitter before the run lost more of their stock-market value during it, <bookmark mark='e'/> beyond "
            "what their unrealized losses and uninsured deposits would predict. Diamond and Dybvig's depositors "
            "coordinate on a sunspot; these ones could watch each other do it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def weekend(self):
        rows = VGroup(
            label(r"Sunday 12 March 2023", font_size=28, color=E.ACCENT),
            label(r"every depositor of Silicon Valley Bank and Signature Bank, \ insured or not, \ is protected",
                  font_size=22, color=CB),
            label(r"the Fed's new lending programme: \ loans for up to a year against Treasuries and agency bonds, \ "
                  r"valued at par", font_size=22, color=CB),
            label(r"beyond Bagehot: \ his collateral was good in ordinary times; \ these bonds had lost value "
                  r"because rates rose", font_size=21, color=HOLD),
            label(r"the run stopped; \ the question of what it promised for next time did not", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Treasury, \ Federal Reserve and FDIC, \ joint statement, \ 12 March 2023; \ the Bank "
                            r"Term Funding Program", corner=DR, font_size=12)
        with self.voiceover(
            "The response came on Sunday the twelfth of March. <bookmark mark='a'/> The Treasury, the Federal "
            "Reserve and the FDIC announced that every depositor of Silicon Valley Bank and of Signature Bank, "
            "insured or not, would be paid in full. <bookmark mark='b'/> And the Federal Reserve opened a new "
            "programme lending to banks for up to a year against Treasury and agency bonds, valued not at their "
            "market price but at par. <bookmark mark='c'/> That goes beyond Bagehot. He asked for collateral that "
            "would be good in ordinary times, valued as it would be without the panic. These bonds had lost value "
            "because interest rates had risen, not because of the panic. <bookmark mark='d'/> The run "
            "stopped. What the weekend promised for the next run, every uninsured depositor could work out."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def narrow(self):
        rows = VGroup(
            label(r"narrow banking: \ make money unrunnable", font_size=28, color=E.ACCENT),
            label(r"the Chicago Plan, \ 1933, \ and Irving Fisher's \emph{100\% Money}, \ 1935: \ deposits backed "
                  r"one for one by reserves", font_size=21, color=CB),
            label(r"lending would be financed by equity and long-term debt, \ which cannot run", font_size=21,
                  color=LOAN),
            label(r"the objection: \ the maturity transformation would move to the shadows \ (chapter 9)",
                  font_size=21, color=HOLD),
            label(r"a stablecoin is a narrow bank outside the law of banks: \ March 2023, \ USDC held \$3.3 billion "
                  r"at Silicon Valley Bank, \ and fell to about 88 cents", font_size=20, color=RUN),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Fisher, \emph{100\% Money} (1935); \ Circle's statements, \ 10--13 March 2023",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Could money be made unrunnable? <bookmark mark='a'/> That is the idea of narrow banking. "
            "<bookmark mark='b'/> In 1933 a group of Chicago economists proposed it, and in 1935 Irving Fisher made "
            "the case in a book called One Hundred Percent Money: back every deposit one for one with reserves at "
            "the central bank. <bookmark mark='c'/> Lending would then be financed by equity and long-term debt, "
            "which cannot run. <bookmark mark='d'/> The objection has always been that the maturity transformation "
            "would not disappear. It would move outside the banks, into the shadows of chapter nine. "
            "<bookmark mark='e'/> A stablecoin backed by Treasury bills is a narrow bank outside the law of banks, "
            "and it can still be run. On Friday the tenth of March 2023, Circle disclosed that three point three "
            "billion dollars of the reserves behind its coin, USDC, were at Silicon Valley Bank. Over the weekend "
            "the coin fell to about eighty-eight cents, and recovered its dollar only when the depositors were "
            "protected."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        rows = VGroup(
            label(r"open questions", font_size=30, color=E.ACCENT),
            label(r"should deposit insurance cover business accounts in full?", font_size=24, color=DEPOSIT),
            label(r"if runs take hours, \ must the lender of last resort be open all night?", font_size=24,
                  color=CB),
            label(r"how much capital, \ and should bonds be valued at market prices in it?", font_size=24,
                  color=EQUITY),
            label(r"can stablecoins and tokenized deposits be made safe without becoming banks?", font_size=24,
                  color=BOND),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        with self.voiceover(
            "The questions still open. <bookmark mark='a'/> Should deposit insurance cover companies' payroll "
            "accounts in full, since in practice it did? <bookmark mark='b'/> If a run can take hours, must the "
            "lender of last resort be ready at any hour, with collateral already pledged? "
            "<bookmark mark='c'/> How much capital should banks hold, and should the bonds they plan to keep be "
            "counted at market prices? <bookmark mark='d'/> And can stablecoins and tokenized deposits be made safe "
            "without becoming banks, with everything that comes with that?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
