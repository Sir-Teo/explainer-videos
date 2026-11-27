"""Act III, Making (Parts 15-21)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=15, level="U", widget="fab", prereq=(4, 5, 6),
        question="Why do the most advanced chips come from so few factories?",
        story="The part opens with Gordon Moore's article of April 1965 (the components on the most economical chip "
              "doubling every year, 65,000 by 1975) and with Hsinchu in 1987, where TSMC set out to make other "
              "companies' chips and design none of its own; in 2025 it made 12,682 products for 534 customers. The "
              "viewer chooses between building a $20bn fab and booking a foundry at $17,000 a wafer: at 5,000 wafers a "
              "month a good die costs $29 from the foundry and $183 from a half-empty fab still learning its process, "
              "and owning first pays at about 32,000. A chip is a loop of film, resist, light and etch repeated layer on "
              "layer; a 300 mm wafer holds about 640 dies of 100 mm2, and random defects make an 800 mm2 die yield half "
              "as often. TSMC spends a third to a half of its revenue on fabs every year, used about 88% of its capacity "
              "in 2025 and earned about $8,100 a wafer. The industry split into fabless designers (Nvidia, from $6.9bn "
              "to $215.9bn of revenue without a fab) and foundries, while Intel's foundry lost $10.3bn in 2025; ASML is "
              "the only maker of EUV machines. America's chip output rose about 5,089 times since 1972 as the real price "
              "fell 98%. Memory swings from loss to boom (Micron, from a $2.3bn quarterly operating loss to $43.8bn of "
              "operating profit in a quarter); the analog makers ride cars and factories. High-performance computing rose "
              "from 43% to 68% of TSMC's revenue; its three 2-3 nm fabs are all in Taiwan; America subsidizes fabs at "
              "home and restricts who may buy. WSTS forecast $975bn for 2026 and sales passed $1.22 trillion by "
              "September; the series calls more than $1.8 trillion for the year (65%).",
        handoff="Part 16, electronics, follows the chips into the devices, and asks why the company that builds the device "
                "keeps the least of it.",
        outside="Percentages, logarithms and exponentials; Part 4's fixed and variable costs; Part 5's moats; Part 6's cycle.",
        objectives={
            "U": ["Explain how a chip is made, and why a fab costs the same whether it is full or empty.",
                  "Explain the split between fabless designers, foundries and integrated makers, and why it happened.",
                  "Explain why the most advanced chips come from a few fabs, one foundry and one maker of machines."],
            "M": ["Compute gross dies on a wafer, the yield at a defect density and the cost of a good die.",
                  "Compute a fab's cost per wafer at a given loading and the volume at which owning beats booking.",
                  "Compute a doubling time from two counts, and what operating leverage does to a memory maker's profit."],
            "D": ["Score two forecasts (Moore's of 1965 and WSTS's of December 2025) and say which assumption failed.",
                  "Judge how much of the 2026 boom is price and how much volume, and what would end it."],
            "I": ["Read a foundry's revenue by node and platform, its utilization and its capital spending in a 20-F.",
                  "Place a chip company on the map: foundry, fabless, integrated, memory, equipment, design software."],
        },
        results=[
            ("Gross dies", r"N = \frac{\pi r^2}{A} - \frac{\pi d}{\sqrt{2A}}"),
            ("Yield", r"Y = e^{-A D}"),
            ("Cost of a good die", r"c = \frac{F/(12v) + c_w}{N\,Y}"),
            ("Doubling time", r"T = \frac{t_1 - t_0}{\log_2(n_1/n_0)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, "s09_intermission", 8, 9, 10, 11), I=(12,), D=(13,),
        also=(("The Register's rows for Part 15", "explainer/industry/data/rows_p15.py"),
              ("Dies, yield, the learning curve, the fab and Run it", "explainer/industry/works/fab.py"),
              ("TSMC's fabs", "explainer/industry/data/tables.py"),
              ("FRED, Our World in Data, the SEC's foreign filers and the companies' accounts",
               "explainer/industry/data/SOURCES.md")),
    ),
]
