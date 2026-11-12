"""Run a lab from the command line: ``python -m videos.quant.labs 10 [--show]`` (see the package docstring)."""

from __future__ import annotations

import argparse
import time

from videos.quant import labs


def main() -> None:
    ap = argparse.ArgumentParser(description=labs.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parts", nargs="*", type=int, help="part numbers (1-43)")
    ap.add_argument("--all", action="store_true", help="run every lab")
    ap.add_argument("--list", action="store_true", help="list the labs and exit")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--show", action="store_true", help="open the figure in a window")
    ap.add_argument("--out", default=str(labs.ROOT / "renders" / "labs"), help="where figures are saved")
    args = ap.parse_args()
    parts = list(range(1, labs.N_PARTS + 1)) if (args.all or args.list) else args.parts
    if not parts:
        ap.error("give a part number, --all or --list")
    for part in parts:
        module = labs.load(part)
        if args.list:
            print(f"{part:>2}  {module.TITLE}")
            continue
        start = time.time()
        lab = module.run(seed=args.seed)
        print(f"Lab {part} · {module.TITLE}\n{module.GOAL}\n")
        print(lab.table())
        if args.show:
            import matplotlib.pyplot as plt

            plt.show()
        path = labs.save(lab, f"{args.out}/lab{part:02d}.png")
        print(f"\nfigure: {path}   ({time.time() - start:.1f} s)\n")
        if module.TASKS:
            print("Now change it:")
            for task in module.TASKS:
                print(f"  - {task}")
            print()


if __name__ == "__main__":
    main()
