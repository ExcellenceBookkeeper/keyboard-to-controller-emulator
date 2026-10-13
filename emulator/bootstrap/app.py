"""Application entrypoint.

Wires the service bus, starts the Win32 input adapter, and blocks on the
tray. This is the only module allowed to construct adapters directly —
everything else receives them via DI from here.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

import structlog

from emulator.adapters.vigem_adapter import ViGEmAdapter
from emulator.adapters.win32_input import Win32InputAdapter
from emulator.config.loader import load_config
from emulator.services.bus import ServiceBus
from emulator.services.mapping_service import MappingService
from emulator.services.profile_service import ProfileService
from emulator.services.telemetry_service import TelemetryService


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stderr)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
    )


async def _run(profile_name: str) -> int:
    log = structlog.get_logger("k2c.bootstrap")
    config = load_config()
    profile_service = ProfileService(config.profile_dir)
    profile = profile_service.load(profile_name)

    vigem = ViGEmAdapter()
    await vigem.start()

    bus = ServiceBus()
    mapping = MappingService(profile, vigem)
    telemetry = TelemetryService()
    bus.register(mapping)
    bus.register(telemetry)

    win32 = Win32InputAdapter(bus)
    await win32.start()

    log.info("emulator.running", profile=profile.name, pad=vigem.pad_kind)
    try:
        await bus.run_forever()
    finally:
        await win32.stop()
        await vigem.stop()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="k2c", description="keyboard-to-controller-emulator")
    parser.add_argument("--profile", default="default", help="profile name to load")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    try:
        return asyncio.run(_run(args.profile))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())