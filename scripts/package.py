#!/usr/bin/env python3
"""Validate and package public plugin assets using only the Python standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://api.callcompany.ai/api/mcp"
SHARED = (
    "README.md", "LICENSE", "assets/README.md", "assets/logo.png",
    "skills/callcompany/SKILL.md",
)
PACKAGES = {
    "chatgpt": SHARED + ("plugin.json", "mcp.json"),
    "claude": SHARED + (".claude-plugin/plugin.json", ".mcp.json"),
}


def read_bytes(relative):
    path = ROOT / relative
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError(f"Symlinks are not allowed: {relative}")
    if not path.is_file() or not path.resolve().is_relative_to(ROOT):
        raise ValueError(f"Missing or unsafe package file: {relative}")
    return path.read_bytes()


def read_json(relative):
    return json.loads(read_bytes(relative))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate():
    manifest = read_json("plugin.json")
    claude = read_json(".claude-plugin/plugin.json")
    require(manifest["name"] == claude["name"] == "callcompany", "Plugin names must agree")
    require(manifest["version"] == claude["version"], "Plugin versions must agree")
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Use a semantic version")
    require(manifest["license"] == claude["license"] == "ISC", "Preserve the package license")
    marketplace = read_json(".claude-plugin/marketplace.json")
    require([(p["name"], p["source"]) for p in marketplace["plugins"]] ==
            [("callcompany", ".")], "Marketplace must select this root plugin")
    portable = read_json("mcp.json")["mcpServers"]
    require(portable == {"callcompany": {
        "type": "streamable-http", "url": MCP_URL,
    }}, "Portable MCP must use production OAuth without credentials")
    require(read_json(".mcp.json") == {"mcpServers": {"callcompany": {
        "type": "http", "url": MCP_URL,
    }}}, "Claude MCP must use production OAuth without credentials")
    extension = manifest["extensions"]["com.openai"]
    ui = extension["interface"]
    for key, limit in [("displayName", 30), ("shortDescription", 30),
                       ("longDescription", 4000), ("developerName", 80)]:
        require(0 < len(ui[key]) <= limit, f"Invalid {key}")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(ui[key].startswith("https://"), f"HTTPS required: {key}")
    for key in ("composerIcon", "logo"):
        require(ui[key] == "./assets/logo.png", f"Unexpected asset: {key}")
    require(len(ui["defaultPrompt"]) <= 3 and all(len(p) <= 128 for p in ui["defaultPrompt"]),
            "Invalid starter prompts")
    cases = extension["review"]["test_cases"]
    require(len(cases["positive"]) == 5 and len(cases["negative"]) == 3, "Need 5 positive / 3 negative cases")
    for case in cases["positive"] + cases["negative"]:
        require(all(isinstance(case.get(k), str) and case[k].strip()
                    for k in ("description", "prompt", "expected_behavior")),
                "Review scenarios must state expected behavior")
    for case in cases["positive"]:
        require(isinstance(case.get("tools_triggered"), str) and case["tools_triggered"].strip(),
                "Positive tools_triggered must be a nonempty string")
    png = read_bytes("assets/logo.png")
    require(png[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", png[16:24]) == (512, 512),
            "Expected 512x512 PNG logo")
    for relative in sorted(set().union(*PACKAGES.values())):
        content = read_bytes(relative)
        if relative.endswith((".json", ".md")):
            text = content.decode("utf-8")
            require(not re.search(r"-----BEGIN .*PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9_-]{20,}", text),
                    f"Potential credential in {relative}")
    require(len(read_bytes("README.md").split()) >= 40, "Missing plugin documentation")
    return manifest["version"]


def build(output):
    version = validate()
    output.mkdir(parents=True, exist_ok=True)
    for platform, files in PACKAGES.items():
        destination = output / f"callcompany-{platform}.zip"
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative in sorted(files):
                entry = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, read_bytes(relative), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        print(f"{destination.name} v{version} sha256:{digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without creating archives")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if args.check:
        print(f"Package checks passed: {validate()}")
    else:
        build(args.out)
