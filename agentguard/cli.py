"""
AgentGuard CLI Module

命令行接口模块
"""

from typing import List, Optional
from pathlib import Path
import sys

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from . import __version__
from .rules import RuleSet, Rule, RuleType, Severity, DEFAULT_RULESET
from .checker import ComplianceChecker
from .report import ComplianceReport, ReportFormat


app = typer.Typer(
    name="agentguard",
    help="🛡️ AgentGuard - AI Agent Behavior Compliance Guardian",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool):
    """版本回调"""
    if value:
        console.print(f"[bold blue]AgentGuard[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="显示版本信息"
    ),
):
    """AgentGuard - AI Agent行为准则管理与合规检查工具"""
    pass


@app.command("check")
def check_content(
    content: str = typer.Argument(..., help="要检查的内容或文件路径"),
    rules_file: Optional[Path] = typer.Option(
        None, "--rules", "-r",
        help="规则集文件路径 (YAML/JSON)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="输出报告文件路径"
    ),
    format: ReportFormat = typer.Option(
        ReportFormat.CONSOLE, "--format", "-f",
        help="报告输出格式"
    ),
    category: Optional[str] = typer.Option(
        None, "--category", "-c",
        help="只检查指定分类的规则"
    ),
    strict: bool = typer.Option(
        False, "--strict",
        help="严格模式：任何违规都视为失败"
    ),
):
    """检查内容合规性"""
    # 加载规则集
    if rules_file:
        if rules_file.suffix in ['.yaml', '.yml']:
            ruleset = RuleSet.from_yaml(str(rules_file))
        elif rules_file.suffix == '.json':
            ruleset = RuleSet.from_json(str(rules_file))
        else:
            console.print("[red]错误：不支持的规则文件格式，请使用YAML或JSON[/red]")
            raise typer.Exit(1)
    else:
        ruleset = DEFAULT_RULESET
        console.print("[dim]使用默认规则集[/dim]")
    
    # 读取内容
    content_path = Path(content)
    if content_path.exists():
        with open(content_path, 'r', encoding='utf-8') as f:
            check_content_text = f.read()
        console.print(f"[dim]从文件加载内容: {content}[/dim]")
    else:
        check_content_text = content
    
    # 执行检查
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在检查合规性...", total=None)
        
        checker = ComplianceChecker(ruleset)
        
        if category:
            result = checker.check_by_category(check_content_text, category)
        else:
            result = checker.check(check_content_text)
        
        progress.update(task, completed=True)
    
    # 生成报告
    report = ComplianceReport()
    report.add_result(result)
    
    # 输出结果
    if output:
        report.export(format, str(output))
        console.print(f"[green]报告已保存至: {output}[/green]")
    else:
        if format == ReportFormat.CONSOLE:
            report.print_console(console)
        else:
            content = report.export(format)
            console.print(content)
    
    # 退出码
    if strict:
        if result.violations:
            raise typer.Exit(1)
    else:
        if not result.passed:
            raise typer.Exit(1)


@app.command("rules")
def manage_rules(
    action: str = typer.Argument(..., help="操作: list, show, create, validate"),
    rules_file: Optional[Path] = typer.Option(
        None, "--file", "-f",
        help="规则集文件路径"
    ),
    rule_id: Optional[str] = typer.Option(
        None, "--id", "-i",
        help="规则ID"
    ),
):
    """管理规则集"""
    if action == "list":
        ruleset = DEFAULT_RULESET
        if rules_file and rules_file.exists():
            if rules_file.suffix in ['.yaml', '.yml']:
                ruleset = RuleSet.from_yaml(str(rules_file))
            elif rules_file.suffix == '.json':
                ruleset = RuleSet.from_json(str(rules_file))
        
        console.print(Panel.fit(
            f"[bold]规则集: {ruleset.name}[/bold]\n"
            f"[dim]版本: {ruleset.version} | 共 {len(ruleset.rules)} 条规则[/dim]"
        ))
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("名称")
        table.add_column("类型")
        table.add_column("严重程度")
        table.add_column("分类")
        table.add_column("状态")
        
        for rule in ruleset.rules:
            status = "[green]启用[/green]" if rule.enabled else "[red]禁用[/red]"
            severity_color = {
                Severity.CRITICAL.value: "red",
                Severity.HIGH.value: "orange3",
                Severity.MEDIUM.value: "yellow",
                Severity.LOW.value: "blue",
                Severity.INFO.value: "dim",
            }.get(rule.severity.value, "white")
            
            table.add_row(
                rule.id,
                rule.name,
                rule.type.value,
                f"[{severity_color}]{rule.severity.value}[/{severity_color}]",
                rule.category or "-",
                status
            )
        
        console.print(table)
    
    elif action == "show":
        if not rule_id:
            console.print("[red]错误：请提供规则ID (--id)[/red]")
            raise typer.Exit(1)
        
        ruleset = DEFAULT_RULESET
        if rules_file and rules_file.exists():
            if rules_file.suffix in ['.yaml', '.yml']:
                ruleset = RuleSet.from_yaml(str(rules_file))
            elif rules_file.suffix == '.json':
                ruleset = RuleSet.from_json(str(rules_file))
        
        rule = ruleset.get_rule(rule_id)
        if rule:
            console.print(Panel.fit(
                f"[bold]{rule.name}[/bold]\n"
                f"[dim]ID: {rule.id} | 类型: {rule.type.value} | 严重程度: {rule.severity.value}[/dim]\n\n"
                f"{rule.description}\n\n"
                f"[dim]分类: {rule.category or '无'} | 标签: {', '.join(rule.tags) if rule.tags else '无'}[/dim]"
            ))
        else:
            console.print(f"[red]未找到规则: {rule_id}[/red]")
            raise typer.Exit(1)
    
    elif action == "create":
        # 创建示例规则文件
        example_ruleset = RuleSet(
            name="my-ruleset",
            version="1.0.0",
            description="我的自定义规则集",
            rules=[
                Rule(
                    id="example-001",
                    name="示例规则",
                    description="这是一个示例规则",
                    type=RuleType.KEYWORD,
                    severity=Severity.MEDIUM,
                    keywords=["示例", "测试"],
                    category="example"
                )
            ]
        )
        
        output_file = rules_file or Path("rules.yaml")
        example_ruleset.to_yaml(str(output_file))
        console.print(f"[green]示例规则集已创建: {output_file}[/green]")
    
    elif action == "validate":
        if not rules_file:
            console.print("[red]错误：请提供规则文件路径 (--file)[/red]")
            raise typer.Exit(1)
        
        try:
            if rules_file.suffix in ['.yaml', '.yml']:
                RuleSet.from_yaml(str(rules_file))
            elif rules_file.suffix == '.json':
                RuleSet.from_json(str(rules_file))
            else:
                console.print("[red]错误：不支持的文件格式[/red]")
                raise typer.Exit(1)
            
            console.print(f"[green]✓ 规则文件验证通过: {rules_file}[/green]")
        except Exception as e:
            console.print(f"[red]✗ 规则文件验证失败: {e}[/red]")
            raise typer.Exit(1)


@app.command("batch")
def batch_check(
    input_dir: Path = typer.Argument(..., help="输入目录，包含要检查的文件"),
    rules_file: Optional[Path] = typer.Option(
        None, "--rules", "-r",
        help="规则集文件路径"
    ),
    output: Path = typer.Option(
        Path("report.html"), "--output", "-o",
        help="输出报告文件路径"
    ),
    pattern: str = typer.Option(
        "*.txt", "--pattern", "-p",
        help="文件匹配模式"
    ),
):
    """批量检查目录中的文件"""
    if not input_dir.exists():
        console.print(f"[red]错误：目录不存在: {input_dir}[/red]")
        raise typer.Exit(1)
    
    # 加载规则集
    if rules_file:
        if rules_file.suffix in ['.yaml', '.yml']:
            ruleset = RuleSet.from_yaml(str(rules_file))
        elif rules_file.suffix == '.json':
            ruleset = RuleSet.from_json(str(rules_file))
        else:
            console.print("[red]错误：不支持的规则文件格式[/red]")
            raise typer.Exit(1)
    else:
        ruleset = DEFAULT_RULESET
    
    # 查找文件
    files = list(input_dir.glob(pattern))
    if not files:
        console.print(f"[yellow]未找到匹配的文件: {pattern}[/yellow]")
        raise typer.Exit(0)
    
    console.print(f"[dim]找到 {len(files)} 个文件待检查[/dim]")
    
    # 批量检查
    checker = ComplianceChecker(ruleset)
    report = ComplianceReport()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("批量检查中...", total=len(files))
        
        for file_path in files:
            progress.update(task, description=f"检查: {file_path.name}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = checker.check(content)
                report.add_result(result)
            except Exception as e:
                console.print(f"[yellow]警告：无法读取文件 {file_path}: {e}[/yellow]")
            
            progress.advance(task)
    
    # 导出报告
    format = ReportFormat.HTML if output.suffix == '.html' else ReportFormat.MARKDOWN if output.suffix == '.md' else ReportFormat.JSON
    report.export(format, str(output))
    
    # 显示摘要
    summary = report.get_summary()
    console.print(f"\n[bold]检查完成！[/bold]")
    console.print(f"总文件数: {summary['total_checks']}")
    console.print(f"通过: [green]{summary['passed']}[/green]")
    console.print(f"失败: [red]{summary['failed']}[/red]")
    console.print(f"平均分数: {summary['average_score']}")
    console.print(f"\n[green]报告已保存: {output}[/green]")


@app.command("init")
def init_project(
    project_dir: Path = typer.Argument(
        Path("."), help="项目目录"
    ),
):
    """初始化AgentGuard项目"""
    project_dir = project_dir.resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建目录结构
    (project_dir / "rules").mkdir(exist_ok=True)
    (project_dir / "reports").mkdir(exist_ok=True)
    (project_dir / "examples").mkdir(exist_ok=True)
    
    # 创建默认规则集
    DEFAULT_RULESET.to_yaml(str(project_dir / "rules" / "default.yaml"))
    
    # 创建示例文件
    example_content = """这是一个示例文本文件。
用于演示AgentGuard的合规检查功能。
您可以修改此文件来测试不同的规则。
"""
    with open(project_dir / "examples" / "sample.txt", 'w', encoding='utf-8') as f:
        f.write(example_content)
    
    # 创建配置文件
    config_content = """# AgentGuard 配置文件

# 默认规则集
default_ruleset: rules/default.yaml

# 检查配置
strict_mode: false
max_content_length: 100000

# 报告配置
report_format: console
save_reports: true
report_dir: reports
"""
    with open(project_dir / "agentguard.yaml", 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    console.print(Panel.fit(
        f"[bold green]✓ AgentGuard项目初始化完成！[/bold green]\n\n"
        f"项目目录: [blue]{project_dir}[/blue]\n\n"
        f"已创建:\n"
        f"  • rules/default.yaml - 默认规则集\n"
        f"  • examples/sample.txt - 示例文件\n"
        f"  • agentguard.yaml - 配置文件\n\n"
        f"快速开始:\n"
        f"  [dim]agentguard check examples/sample.txt[/dim]\n"
        f"  [dim]agentguard rules list[/dim]"
    ))


def main():
    """CLI入口点"""
    app()


if __name__ == "__main__":
    main()
