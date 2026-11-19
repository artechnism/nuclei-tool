import asyncio
import json
from typing import List
from .config import NUCLEI_PATH
from .models import NucleiSeverity, NucleiFinding, NucleiResult

async def run_nuclei(
    target: str,
    severity: List[NucleiSeverity] | None = None,
    tags: List[str] | None = None,
    rate_limit: int = 100,
    concurrency: int = 10,
) -> NucleiResult:
    cmd = [NUCLEI_PATH, "-u", target, "-jsonl", "-silent",
           "-rate-limit", str(rate_limit), "-concurrency", str(concurrency)]

    if severity:
        cmd += ["-severity", ",".join(s.value for s in severity)]
    if tags:
        cmd += ["-tags", ",".join(tags)]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

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