import asyncio
import typer
from rich.console import Console
from rich.table import Table
from typing import List, Optional

from nuclei_tool.runner import run_nuclei
from nuclei_tool.models import NucleiSeverity
from nuclei_tool.database import init_db, save_scan, get_past_scans

app = typer.Typer(help="Custom Nuclei Scanner Tool")
console = Console()

@app.command()
def scan(
    target: str = typer.Argument(..., help="Target URL to scan"),
    severity: Optional[List[str]] = typer.Option(None, "--severity", "-s", help="Severity levels (e.g., high, critical)"),
    tags: Optional[List[str]] = typer.Option(None, "--tags", "-t", help="Template tags"),
    rate_limit: int = typer.Option(100, "--rate-limit", help="Rate limit in requests per second"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save results to database")
):
    """Run a Nuclei scan against a target."""
    console.print(f"[bold blue]Starting scan on:[/bold blue] {target}")
    
    # Convert strings to Enum
    sev_enum = None
    if severity:
        try:
            sev_enum = [NucleiSeverity(s.lower()) for s in severity]
        except ValueError:
            console.print("[bold red]Error:[/bold red] Invalid severity level.")
            raise typer.Exit(1)

    # Execute scan
    with console.status("[bold green]Scanning...[/bold green]"):
        result = asyncio.run(run_nuclei(
            target=target,
            severity=sev_enum,
            tags=tags,
            rate_limit=rate_limit
        ))

    if not result.success:
        console.print(f"[bold red]Scan failed:[/bold red] {result.error}")
        raise typer.Exit(1)

    # Display results
    if not result.findings:
        console.print("[bold yellow]No vulnerabilities found.[/bold yellow]")
    else:
        table = Table(title=f"Findings for {target}")
        table.add_column("Severity", style="cyan")
        table.add_column("Template Name", style="magenta")
        table.add_column("Template ID", style="green")
        table.add_column("Matched At", style="yellow")

        for f in result.findings:
            color = "red" if f.severity in ["critical", "high"] else "yellow" if f.severity == "medium" else "green"
            table.add_row(
                f"[{color}]{f.severity}[/{color}]",
                f.name,
                f.template_id,
                f.matched_at
            )
        
        console.print(table)

    # Save to database
    if save:
        save_scan(target, result.findings)
        console.print("[bold green]✓ Results saved to database.[/bold green]")

@app.command()
def history():
    """Display previous scan history."""
    scans = get_past_scans()
    if not scans:
        console.print("[yellow]No scan history found.[/yellow]")
        return

    table = Table(title="Scan History")
    table.add_column("ID", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Date", style="green")

    for scan_id, target, scan_date in scans:
        table.add_row(str(scan_id), target, scan_date)

    console.print(table)

if __name__ == "__main__":
    init_db() # Ensure database exists
    app()