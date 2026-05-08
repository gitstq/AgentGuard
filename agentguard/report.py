"""
AgentGuard Report Module

报告生成模块
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

from .checker import CheckResult, Violation
from .rules import Severity


class ReportFormat(str, Enum):
    """报告格式枚举"""
    CONSOLE = "console"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"
    YAML = "yaml"


@dataclass
class ComplianceReport:
    """合规报告"""
    results: List[CheckResult] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    report_name: str = "AgentGuard Compliance Report"
    version: str = "1.0.0"
    
    def add_result(self, result: CheckResult) -> None:
        """添加检查结果"""
        self.results.append(result)
    
    def get_summary(self) -> Dict[str, Any]:
        """获取报告摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        total_violations = sum(len(r.violations) for r in self.results)
        critical = sum(
            len([v for v in r.violations if v.severity == Severity.CRITICAL.value])
            for r in self.results
        )
        high = sum(
            len([v for v in r.violations if v.severity == Severity.HIGH.value])
            for r in self.results
        )
        
        avg_score = sum(r.score for r in self.results) / total if total > 0 else 0
        
        return {
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 2) if total > 0 else 0,
            "total_violations": total_violations,
            "critical_violations": critical,
            "high_violations": high,
            "average_score": round(avg_score, 2),
            "generated_at": self.generated_at.isoformat(),
        }
    
    def print_console(self, console: Optional[Console] = None) -> None:
        """打印控制台报告"""
        console = console or Console()
        
        # 标题
        console.print(Panel.fit(
            f"[bold blue]{self.report_name}[/bold blue]\n"
            f"[dim]Version {self.version} | Generated at {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}[/dim]",
            border_style="blue"
        ))
        
        # 摘要
        summary = self.get_summary()
        summary_table = Table(title="📊 Summary", show_header=False)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Total Checks", str(summary["total_checks"]))
        summary_table.add_row("Passed", f"[green]{summary['passed']}[/green]")
        summary_table.add_row("Failed", f"[red]{summary['failed']}[/red]")
        summary_table.add_row("Pass Rate", f"{summary['pass_rate']}%")
        summary_table.add_row("Average Score", f"{summary['average_score']}/100")
        summary_table.add_row("Total Violations", str(summary["total_violations"]))
        summary_table.add_row("Critical", f"[red]{summary['critical_violations']}[/red]")
        summary_table.add_row("High", f"[orange3]{summary['high_violations']}[/orange3]")
        
        console.print(summary_table)
        console.print()
        
        # 详细结果
        if self.results:
            console.print("[bold]📋 Detailed Results:[/bold]\n")
            
            for i, result in enumerate(self.results, 1):
                status = "[green]✓ PASS[/green]" if result.passed else "[red]✗ FAIL[/red]"
                score_color = "green" if result.score >= 80 else "yellow" if result.score >= 60 else "red"
                
                console.print(f"[bold]Check #{i}[/bold] {status} | Score: [{score_color}]{result.score}[/{score_color}]")
                
                if result.violations:
                    violation_tree = Tree("[dim]Violations:[/dim]")
                    for v in result.violations:
                        severity_color = {
                            Severity.CRITICAL.value: "red",
                            Severity.HIGH.value: "orange3",
                            Severity.MEDIUM.value: "yellow",
                            Severity.LOW.value: "blue",
                            Severity.INFO.value: "dim",
                        }.get(v.severity, "white")
                        
                        v_text = f"[{severity_color}]{v.severity.upper()}[/{severity_color}] {v.rule_name}"
                        if v.matched_text:
                            v_text += f" [dim](matched: {v.matched_text[:50]}...)[/dim]"
                        violation_tree.add(v_text)
                    console.print(violation_tree)
                
                console.print()
    
    def to_json(self) -> str:
        """导出为JSON格式"""
        data = {
            "report_name": self.report_name,
            "version": self.version,
            "generated_at": self.generated_at.isoformat(),
            "summary": self.get_summary(),
            "results": [
                {
                    "passed": r.passed,
                    "score": r.score,
                    "check_time": r.check_time.isoformat(),
                    "duration_ms": r.duration_ms,
                    "violations": [
                        {
                            "rule_id": v.rule_id,
                            "rule_name": v.rule_name,
                            "severity": v.severity,
                            "description": v.description,
                            "type": v.type,
                            "position": v.position,
                            "matched_text": v.matched_text,
                            "suggestion": v.suggestion,
                        }
                        for v in r.violations
                    ]
                }
                for r in self.results
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def to_markdown(self) -> str:
        """导出为Markdown格式"""
        summary = self.get_summary()
        
        md = f"""# {self.report_name}

**Version:** {self.version}  
**Generated:** {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Checks | {summary['total_checks']} |
| Passed | {summary['passed']} ✅ |
| Failed | {summary['failed']} ❌ |
| Pass Rate | {summary['pass_rate']}% |
| Average Score | {summary['average_score']}/100 |
| Total Violations | {summary['total_violations']} |
| Critical | {summary['critical_violations']} 🔴 |
| High | {summary['high_violations']} 🟠 |

## 📋 Detailed Results

"""
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result.passed else "❌ FAIL"
            md += f"### Check #{i} - {status} (Score: {result.score}/100)\n\n"
            
            if result.violations:
                md += "**Violations:**\n\n"
                for v in result.violations:
                    emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(v.severity, "⚪")
                    md += f"- {emoji} **{v.severity.upper()}**: {v.rule_name}\n"
                    md += f"  - Description: {v.description}\n"
                    if v.suggestion:
                        md += f"  - Suggestion: {v.suggestion}\n"
                    md += "\n"
            else:
                md += "✅ No violations found.\n\n"
        
        return md
    
    def to_html(self) -> str:
        """导出为HTML格式"""
        summary = self.get_summary()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.report_name}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .summary {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .metric {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .metric-label {{ color: #666; margin-top: 5px; }}
        .result {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .result-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .violation {{ padding: 10px; margin: 10px 0; border-left: 4px solid #dc3545; background: #fff5f5; border-radius: 4px; }}
        .severity-critical {{ border-left-color: #dc3545; }}
        .severity-high {{ border-left-color: #fd7e14; }}
        .severity-medium {{ border-left-color: #ffc107; }}
        .severity-low {{ border-left-color: #17a2b8; }}
        .score {{ font-size: 1.5em; font-weight: bold; }}
        .score-good {{ color: #28a745; }}
        .score-warning {{ color: #ffc107; }}
        .score-bad {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ {self.report_name}</h1>
        <p>Version {self.version} | Generated at {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <div class="summary-grid">
            <div class="metric">
                <div class="metric-value">{summary['total_checks']}</div>
                <div class="metric-label">Total Checks</div>
            </div>
            <div class="metric">
                <div class="metric-value" style="color: #28a745;">{summary['passed']}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value" style="color: #dc3545;">{summary['failed']}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['pass_rate']}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{summary['average_score']}</div>
                <div class="metric-label">Average Score</div>
            </div>
            <div class="metric">
                <div class="metric-value" style="color: #dc3545;">{summary['critical_violations']}</div>
                <div class="metric-label">Critical Issues</div>
            </div>
        </div>
    </div>
"""
        
        for i, result in enumerate(self.results, 1):
            status_class = "pass" if result.passed else "fail"
            status_text = "✅ PASS" if result.passed else "❌ FAIL"
            score_class = "score-good" if result.score >= 80 else "score-warning" if result.score >= 60 else "score-bad"
            
            html += f"""
    <div class="result">
        <div class="result-header">
            <h3>Check #{i}</h3>
            <div>
                <span class="{status_class}">{status_text}</span>
                <span class="score {score_class}">{result.score}/100</span>
            </div>
        </div>
"""
            
            if result.violations:
                for v in result.violations:
                    html += f"""
        <div class="violation severity-{v.severity}">
            <strong>{v.severity.upper()}</strong>: {v.rule_name}<br>
            <small>{v.description}</small>
        </div>
"""
            else:
                html += "<p>✅ No violations found.</p>"
            
            html += "</div>"
        
        html += """
</body>
</html>"""
        
        return html
    
    def export(self, format: ReportFormat, output_path: Optional[str] = None) -> str:
        """
        导出报告
        
        Args:
            format: 导出格式
            output_path: 输出文件路径，如果不提供则返回内容
        
        Returns:
            报告内容
        """
        if format == ReportFormat.CONSOLE:
            self.print_console()
            return ""
        
        elif format == ReportFormat.JSON:
            content = self.to_json()
        
        elif format == ReportFormat.MARKDOWN:
            content = self.to_markdown()
        
        elif format == ReportFormat.HTML:
            content = self.to_html()
        
        else:
            content = self.to_json()
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return content
