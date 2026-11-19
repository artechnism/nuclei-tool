import asyncio
from nuclei_tool.runner import run_nuclei
from nuclei_tool.models import NucleiSeverity

async def main():
    result = await run_nuclei(
        target="http://localhost:3000",
        severity=[NucleiSeverity.HIGH, NucleiSeverity.CRITICAL],
        tags=["xss"],
    )
    if not result.success:
        print("Error:", result.error)
        return
    print(f"Findings: {len(result.findings)}")
    for f in result.findings:
        print(f"[{f.severity}] {f.name} @ {f.matched_at}")

if __name__ == "__main__":
    asyncio.run(main())