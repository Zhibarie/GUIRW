"""
rwGUI — Rusted Warfare Mod Studio (Flask backend)  v8  — server-side import.
Optimised imports, PEP 8 layout, dotenv support.
"""

# ── Standard library ──────────────────────────
import base64
import io
import json
import os
import re
import uuid
import zipfile

# ── Third-party ───────────────────────────────
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_file,
)

# ── Load .env before reading env vars ─────────
load_dotenv()

# ── Application ───────────────────────────────
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 150 * 1024 * 1024  # 150 MB

# ── Local imports ─────────────────────────────
from constants import SECTIONS_DATA  # noqa: E402

# ── Constants ─────────────────────────────────
GEMINI_URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.0-flash:generateContent"
)

# ── Import parser constants ──────────────────
_MULTI_PREFIXES = [
    (re.compile(r"^turret_", re.I), "turrets"),
    (re.compile(r"^projectile_", re.I), "projectiles"),
    (re.compile(r"^action_", re.I), "actions"),
    (re.compile(r"^hiddenAction_", re.I), "hiddenActions"),
    (re.compile(r"^animation_", re.I), "animations"),
    (re.compile(r"^canBuild_", re.I), "canBuilds"),
    (re.compile(r"^leg_", re.I), "legs"),
    (re.compile(r"^arm_", re.I), "arms"),
    (re.compile(r"^attachment_", re.I), "attachments"),
    (re.compile(r"^effect_", re.I), "effects"),
    (re.compile(r"^placementRule_", re.I), "placementRules"),
    (re.compile(r"^global_resource_", re.I), "globalResources"),
    (re.compile(r"^resource_", re.I), "resources"),
    (re.compile(r"^decal_", re.I), "decals"),
    (re.compile(r"^comment_", re.I), "comments"),
    (re.compile(r"^template_", re.I), "templates"),
]
_SIMPLE_SECS = {"core", "graphics", "attack", "movement", "ai"}
_INI_EXTS = {".ini", ".copyfrom", ".template"}
_ASSET_MIMES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp",
    ".ogg": "audio/ogg", ".wav": "audio/wav", ".mp3": "audio/mpeg",
}
_MOD_FIELDS = [
    "title", "description", "tags", "minVersion",
    "id", "requiredMods", "requiredModsMessage",
]

MAX_UNITS = 300
MAX_ASSETS = 80


# ═══════════════════════════════════════════════
#  Parser helpers
# ═══════════════════════════════════════════════

def _parse_ini(text):
    """Parse RW .ini text -> {section: {key: value}}."""
    sections: dict[str, dict[str, str]] = {}
    cur = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ";", "//")):
            continue
        if line.startswith("[") and line.endswith("]"):
            cur = line[1:-1].strip()
            sections.setdefault(cur, {})
            continue
        if cur and ":" in line:
            ci = line.index(":")
            k = line[:ci].strip()
            v = line[ci + 1 :].strip()
            if k:
                sections[cur][k] = v
    return sections


def _create_unit(uid: str, name: str) -> dict:
    """Return a blank unit dict with sensible defaults."""
    return {
        "id": uid,
        "filename": name if name.endswith(".ini") else name + ".ini",
        "core": {
            "name": name, "maxHp": 100, "mass": 100, "radius": 15,
            "isBio": False, "isBuilder": False,
        },
        "graphics": {"image": "unit.png", "total_frames": 1},
        "attack": {
            "canAttack": False, "canAttackFlyingUnits": False,
            "canAttackLandUnits": False, "canAttackUnderwaterUnits": False,
            "maxAttackRange": 150,
        },
        "movement": {"movementType": "LAND", "moveSpeed": 1.0},
        "ai": {
            "buildPriority": 0.1, "useAsBuilder": False,
            "useAsTransport": False,
        },
        "turrets": [], "projectiles": [], "actions": [],
        "hiddenActions": [], "animations": [], "canBuilds": [], "legs": [],
        "arms": [],
        "attachments": [], "effects": [], "placementRules": [],
        "globalResources": [], "resources": [], "decals": [],
        "comments": [], "templates": [],
    }


def _sections_to_unit(sections: dict, filename: str) -> dict:
    """Convert parsed INI sections into a unit object."""
    base = re.sub(r"\.(ini|copyfrom|template)$", "", filename, flags=re.I)
    unit = _create_unit("unit_" + uuid.uuid4().hex[:12], base)
    for sec, fields in sections.items():
        lower = sec.lower()
        if lower in _SIMPLE_SECS:
            unit[lower].update(fields)
            continue
        for pat, key in _MULTI_PREFIXES:
            if pat.match(sec):
                parts = re.split(r"[_\s]+", sec, maxsplit=1)
                id_part = parts[1] if len(parts) > 1 else str(len(unit[key]) + 1)
                unit[key].append({"id": id_part, **fields})
                break
    core_name = unit.get("core", {}).get("name")
    if core_name:
        unit["filename"] = (
            core_name if core_name.endswith(".ini") else core_name + ".ini"
        )
    return unit


def _sections_to_mod_info(sections: dict) -> dict | None:
    """Extract mod-info fields from parsed sections."""
    mod_sec = sections.get("mod") or sections.get("Mod") or sections.get("MOD")
    if not mod_sec:
        return None
    info = {k: mod_sec[k] for k in _MOD_FIELDS if k in mod_sec}
    return info or None


def _asset_b64(data: bytes, ext: str) -> str:
    """Return a base-64 data-URL for an asset."""
    mime = _ASSET_MIMES.get(ext, "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


# ═══════════════════════════════════════════════
#  Routes
# ═══════════════════════════════════════════════

@app.route("/")
def index():
    """Render the main editor SPA."""
    return render_template(
        "index.html",
        sections_data=json.dumps(SECTIONS_DATA),
    )


@app.route("/api/import", methods=["POST"])
def import_mod():
    """
    Server-side import — Python handles all parsing off the browser
    main thread. Accepts multipart form data and returns JSON with
    parsed units, mod-info, warnings, and base64-encoded assets.
    """
    mode = request.form.get("mode", "zip")
    warnings: list[str] = []
    units: list[dict] = []
    mod_info: dict | None = None
    assets: dict[str, str] = {}

    # ── ZIP / RWMOD ─────────────────────────────────────────────────
    if mode == "zip":
        f = request.files.get("file")
        if not f:
            return jsonify({"error": "No file uploaded"}), 400
        ext = os.path.splitext(f.filename)[1].lower()
        if ext not in (".zip", ".rwmod"):
            return jsonify(
                {"error": "Only .zip and .rwmod files are supported"}
            ), 400

        try:
            with zipfile.ZipFile(io.BytesIO(f.read())) as zf:
                names = zf.namelist()

                # mod-info.txt
                mi_names = [n for n in names if n.lower().endswith("mod-info.txt")]
                if mi_names:
                    text = zf.read(mi_names[0]).decode("utf-8", errors="replace")
                    mod_info = _sections_to_mod_info(_parse_ini(text))

                # unit .ini files
                ini_names = [
                    n for n in names
                    if not n.endswith("/")
                    and os.path.splitext(n)[1].lower() in _INI_EXTS
                    and "mod-info" not in n.lower()
                ]
                if len(ini_names) > MAX_UNITS:
                    warnings.append(
                        f"{len(ini_names)} unit files found "
                        f"— only first {MAX_UNITS} imported."
                    )
                    ini_names = ini_names[:MAX_UNITS]

                err_files: list[str] = []
                for name in ini_names:
                    try:
                        text = zf.read(name).decode("utf-8", errors="replace")
                        fname = name.split("/")[-1]
                        units.append(_sections_to_unit(_parse_ini(text), fname))
                    except Exception:
                        err_files.append(name.split("/")[-1])
                if err_files:
                    sample = ", ".join(err_files[:3]) + (
                        " …" if len(err_files) > 3 else ""
                    )
                    warnings.append(
                        f"Skipped {len(err_files)} file(s) "
                        f"with parse errors: {sample}"
                    )

                # assets
                asset_names = [
                    n for n in names
                    if not n.endswith("/")
                    and os.path.splitext(n)[1].lower() in _ASSET_MIMES
                ]
                if len(asset_names) > MAX_ASSETS:
                    warnings.append(
                        f"{len(asset_names)} assets found "
                        f"— only first {MAX_ASSETS} loaded."
                    )
                    asset_names = asset_names[:MAX_ASSETS]

                for name in asset_names:
                    try:
                        fname = name.split("/")[-1]
                        ext2 = os.path.splitext(fname)[1].lower()
                        assets[fname] = _asset_b64(zf.read(name), ext2)
                    except Exception:
                        pass

        except zipfile.BadZipFile:
            return jsonify({"error": "Invalid or corrupted ZIP file"}), 400

    # ── INI files / Folder scan ───────────────────────────────────────
    elif mode in ("ini", "folder"):
        all_files = request.files.getlist("files[]")

        ini_files = [
            f for f in all_files
            if os.path.splitext(f.filename)[1].lower() in _INI_EXTS
            or f.filename.split("/")[-1].lower() == "mod-info.txt"
        ]
        if len(ini_files) > MAX_UNITS:
            warnings.append(
                f"{len(ini_files)} files selected "
                f"— only first {MAX_UNITS} parsed."
            )
            ini_files = ini_files[:MAX_UNITS]

        err_files = []
        for f in ini_files:
            try:
                text = f.read().decode("utf-8", errors="replace")
                sections = _parse_ini(text)
                fname = f.filename.split("/")[-1]
                if "mod-info" in fname.lower() or "mod" in sections:
                    mi = _sections_to_mod_info(sections)
                    if mi:
                        mod_info = mi
                else:
                    units.append(_sections_to_unit(sections, fname))
            except Exception:
                err_files.append(f.filename)
        if err_files:
            warnings.append(f"Skipped {len(err_files)} unreadable file(s).")

        # assets
        asset_files = [
            f for f in all_files
            if os.path.splitext(f.filename)[1].lower() in _ASSET_MIMES
        ]
        if len(asset_files) > MAX_ASSETS:
            warnings.append(
                f"{len(asset_files)} assets — only first {MAX_ASSETS} loaded."
            )
            asset_files = asset_files[:MAX_ASSETS]

        for f in asset_files:
            try:
                ext2 = os.path.splitext(f.filename)[1].lower()
                fname = f.filename.split("/")[-1]
                assets[fname] = _asset_b64(f.read(), ext2)
            except Exception:
                pass

    else:
        return jsonify({"error": f"Unknown mode: {mode}"}), 400

    return jsonify({
        "units": units,
        "modInfo": mod_info,
        "warnings": warnings,
        "assetCount": len(assets),
        "assets": assets,
    })


@app.route("/api/ai-suggest", methods=["POST"])
def ai_suggest():
    """Proxy a prompt to Gemini and return a LogicBoolean expression."""
    body = request.get_json(silent=True) or {}
    prompt = body.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return jsonify(
            {"error": "GEMINI_API_KEY not configured on server"}
        ), 500

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={api_key}",
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "You are a Rusted Warfare modding expert. "
                                    "Output ONLY a valid LogicBoolean expression "
                                    "— no explanation, no markdown, no code "
                                    "fences — for this condition:\n\n"
                                    f"{prompt}"
                                )
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 150,
                },
            },
            timeout=15,
        )
        resp.raise_for_status()
        text = (
            resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        )
        return jsonify({"result": text})

    except requests.Timeout:
        return jsonify({"error": "AI request timed out"}), 504
    except requests.RequestException as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/export-zip", methods=["POST"])
def export_zip():
    """Build a .zip from the current project state and send it."""
    body = request.get_json(silent=True) or {}
    units = body.get("units", [])
    mod_info = body.get("modInfo", {})
    units_ini = body.get("unitsIni", {})
    mod_info_ini = body.get("modInfoIni", "")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mod-info.txt", mod_info_ini)
        for unit in units:
            fname = unit.get("filename", "unit.ini")
            zf.writestr(fname, units_ini.get(fname, ""))
    buf.seek(0)

    safe_name = (mod_info.get("title") or "mod").replace(" ", "_")
    return send_file(
        buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{safe_name}.zip",
    )


# ═══════════════════════════════════════════════
#  Entry-point
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True, port=5000)
