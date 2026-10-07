#!/usr/bin/env python3
"""Consistency cases for the agent plugin: the bundled checker is the
reference hook, the bundled landing reference is the landing guidance, and
every manifest carries the release version and points at this plugin.
Run: python3 test_plugin.py"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REFERENCE_HOOK = os.path.join(ROOT, "tooling", "commit-msg-hook", "commit-msg")
BUNDLED_HOOK = os.path.join(HERE, "skills", "grounded-commits", "scripts", "commit-msg")
PLUGIN_MANIFESTS = [os.path.join(HERE, ".claude-plugin", "plugin.json"),
                    os.path.join(HERE, ".codex-plugin", "plugin.json")]
CLAUDE_MARKETPLACE = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
CODEX_MARKETPLACE = os.path.join(ROOT, ".agents", "plugins", "marketplace.json")
LANDING_REFERENCE = os.path.join(HERE, "skills", "grounded-pull-requests", "references", "landing.md")
LANDING_GUIDANCE = os.path.join(ROOT, "guidance", "landing.md")


def load(path):
    with open(path) as handle:
        return json.load(handle)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def release_version():
    with open(os.path.join(ROOT, "VERSION")) as handle:
        return handle.read().strip()


def case_bundled_hook_matches_reference():
    return read_bytes(BUNDLED_HOOK) == read_bytes(REFERENCE_HOOK) and os.access(BUNDLED_HOOK, os.X_OK)


def case_landing_reference_matches_guidance():
    return read_bytes(LANDING_REFERENCE) == read_bytes(LANDING_GUIDANCE)


def case_manifests_carry_release_version():
    return all(load(path)["version"] == release_version() for path in PLUGIN_MANIFESTS)


def case_manifests_share_name():
    return {load(path)["name"] for path in PLUGIN_MANIFESTS} == {"grounded-commits"}


def case_marketplaces_point_at_plugin():
    claude = load(CLAUDE_MARKETPLACE)["plugins"]
    codex = load(CODEX_MARKETPLACE)["plugins"]
    expected = os.path.relpath(HERE, ROOT)
    return ([(p["name"], os.path.normpath(p["source"])) for p in claude] == [("grounded-commits", expected)]
            and [(p["name"], os.path.normpath(p["source"]["path"])) for p in codex] == [("grounded-commits", expected)])


CASES = [
    ("bundled checker is the reference hook, executable", case_bundled_hook_matches_reference),
    ("bundled landing reference is the landing guidance", case_landing_reference_matches_guidance),
    ("plugin manifests carry the VERSION release", case_manifests_carry_release_version),
    ("plugin manifests share one name", case_manifests_share_name),
    ("both marketplaces list this plugin", case_marketplaces_point_at_plugin),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn())
        except Exception as error:  # a crash is a failure with its reason
            ok, name = False, f"{name} ({type(error).__name__}: {error})"
        failures += not ok
        print(("ok   " if ok else "FAIL ") + name)
    print(f"\n{len(CASES) - failures} of {len(CASES)} plugin cases pass")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
