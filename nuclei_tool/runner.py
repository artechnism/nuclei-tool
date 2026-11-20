import asyncio
import json
from pathlib import Path
from .config import NUCLEI_PATH, NUCLEI_TEMPLATES
from .models import NucleiSeverity, NucleiFinding, NucleiResult

async def run_nuclei(
    target: str,
    severity: list[NucleiSeverity] | None = None,
    tags: list[str] | None = None,
    rate_limit: int = 100,
    concurrency: int = 10,
    timeout: int = 300  # Added timeout parameter (5 minutes)
) -> NucleiResult:
    nuclei = str(Path(NUCLEI_PATH).resolve())

    if not Path(nuclei).is_file():
        return NucleiResult(success=False, error=f"nuclei not found: {nuclei}")

    cmd = [
        nuclei, "-u", target, "-jsonl", "-silent", "-no-color",
        "-rate-limit", str(rate_limit),
        "-concurrency", str(concurrency),
    ]

    # Use project templates if they exist
    if Path(NUCLEI_TEMPLATES).is_dir():
        cmd += ["-t", str(Path(NUCLEI_TEMPLATES).resolve())]

    if severity:
        cmd += ["-severity", ",".join(s.value for s in severity)]
    if tags:
        cmd += ["-tags", ",".join(tags)]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    try:
        # Enforce timeout to prevent infinite hanging
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return NucleiResult(success=False, error=f"Scan timed out after {timeout} seconds.")

    if proc.returncode != 0:
        return NucleiResult(success=False, error=stderr.decode(errors="ignore"))

    findings = []
    for line in stdout.decode(errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        info = data.get("info", {})
        findings.append(NucleiFinding(
            template_id=data.get("template-id", ""),
            name=info.get("name", ""),
            severity=info.get("severity", ""),
            matched_at=data.get("matched-at", ""),
        ))
    return NucleiResult(success=True, findings=findings)