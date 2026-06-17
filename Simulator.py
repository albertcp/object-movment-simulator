#!/usr/bin/env python3
from __future__ import annotations

from controller.app import App
from logic.engine import SimulationEngine


def main() -> None:
    engine = SimulationEngine([])
    app = App(engine)
    app.run()


if __name__ == "__main__":
    main()
