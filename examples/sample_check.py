"""
AgentGuard 使用示例

演示如何使用AgentGuard进行合规检查
"""

from agentguard.rules import RuleSet, Rule, RuleType, Severity, DEFAULT_RULESET
from agentguard.checker import ComplianceChecker
from agentguard.report import ComplianceReport


def basic_check_example():
    """基础检查示例"""
    print("=" * 50)
    print("基础检查示例")
    print("=" * 50)
    
    # 使用默认规则集
    checker = ComplianceChecker(DEFAULT_RULESET)
    
    # 检查内容
    content = "请使用password登录系统，账号是admin"
    
    result = checker.check(content)
    
    print(f"检查内容: {content}")
    print(f"是否通过: {result.passed}")
    print(f"合规分数: {result.score}")
    print(f"违规数量: {len(result.violations)}")
    
    if result.violations:
        print("\n违规详情:")
        for v in result.violations:
            print(f"  - [{v.severity}] {v.rule_name}: {v.description}")
            if v.suggestion:
                print(f"    建议: {v.suggestion}")


def custom_rules_example():
    """自定义规则示例"""
    print("\n" + "=" * 50)
    print("自定义规则示例")
    print("=" * 50)
    
    # 创建自定义规则集
    ruleset = RuleSet(
        name="custom-rules",
        version="1.0.0",
        description="自定义规则集示例",
        rules=[
            Rule(
                id="custom-001",
                name="禁止特定词汇",
                description="检查是否包含特定禁止词汇",
                type=RuleType.KEYWORD,
                severity=Severity.HIGH,
                keywords=["垃圾", "废物", "笨蛋"],
                category="content"
            ),
            Rule(
                id="custom-002",
                name="检查手机号格式",
                description="检测是否泄露手机号",
                type=RuleType.PATTERN,
                severity=Severity.CRITICAL,
                pattern=r"1[3-9]\d{9}",
                category="privacy"
            ),
        ]
    )
    
    checker = ComplianceChecker(ruleset)
    
    # 检查多个内容
    contents = [
        "这是一个正常的内容",
        "你这个笨蛋，真垃圾",
        "我的手机号是13800138000",
    ]
    
    for content in contents:
        result = checker.check(content)
        status = "✓" if result.passed else "✗"
        print(f"{status} [{result.score}] {content[:30]}...")


def batch_check_example():
    """批量检查示例"""
    print("\n" + "=" * 50)
    print("批量检查示例")
    print("=" * 50)
    
    checker = ComplianceChecker(DEFAULT_RULESET)
    
    contents = [
        "正常内容1",
        "包含password的内容",
        "正常内容2",
        "包含secret key的内容",
    ]
    
    results = checker.batch_check(contents)
    
    # 生成报告
    report = ComplianceReport()
    for result in results:
        report.add_result(result)
    
    summary = report.get_summary()
    print(f"总检查数: {summary['total_checks']}")
    print(f"通过: {summary['passed']}")
    print(f"失败: {summary['failed']}")
    print(f"通过率: {summary['pass_rate']}%")
    print(f"平均分数: {summary['average_score']}")


def report_export_example():
    """报告导出示例"""
    print("\n" + "=" * 50)
    print("报告导出示例")
    print("=" * 50)
    
    checker = ComplianceChecker(DEFAULT_RULESET)
    result = checker.check("测试内容包含password")
    
    report = ComplianceReport()
    report.add_result(result)
    
    # 导出为不同格式
    print("导出为JSON格式:")
    json_report = report.to_json()
    print(json_report[:500] + "...")
    
    print("\n导出为Markdown格式:")
    md_report = report.to_markdown()
    print(md_report[:500] + "...")


if __name__ == "__main__":
    basic_check_example()
    custom_rules_example()
    batch_check_example()
    report_export_example()
    
    print("\n" + "=" * 50)
    print("示例运行完成！")
    print("=" * 50)
