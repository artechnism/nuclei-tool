from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class NucleiSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class NucleiFinding:
    template_id: str
    name: str
    severity: str
    matched_at: str

@dataclass
class NucleiResult:
    success: bool
    findings: List[NucleiFinding] = field(default_factory=list)
    error: Optional[str] = None