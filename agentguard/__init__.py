"""
AgentGuard - AI Agent Behavior Compliance Guardian

轻量级AI Agent行为准则管理与合规检查工具
"""

__version__ = "1.0.0"
__author__ = "AgentGuard Team"
__license__ = "MIT"

from .checker import ComplianceChecker
from .rules import Rule, RuleSet
from .report import ComplianceReport

__all__ = [
    "ComplianceChecker",
    "Rule",
    "RuleSet", 
    "ComplianceReport",
]
