"""
Tests for checker module
"""

import pytest
from agentguard.checker import ComplianceChecker, CheckResult
from agentguard.rules import Rule, RuleSet, RuleType, Severity, DEFAULT_RULESET


class TestComplianceChecker:
    """测试ComplianceChecker类"""
    
    def test_checker_creation(self):
        """测试检查器创建"""
        checker = ComplianceChecker()
        assert checker.ruleset is not None
        
        custom_ruleset = RuleSet(name="自定义", rules=[])
        checker = ComplianceChecker(custom_ruleset)
        assert checker.ruleset.name == "自定义"
    
    def test_check_with_no_violations(self):
        """测试无违规的检查"""
        checker = ComplianceChecker(DEFAULT_RULESET)
        result = checker.check("这是一个正常的文本内容，没有任何问题。")
        
        assert isinstance(result, CheckResult)
        assert result.passed is True
        assert len(result.violations) == 0
        assert result.score == 100.0
    
    def test_check_with_violations(self):
        """测试有违规的检查"""
        checker = ComplianceChecker(DEFAULT_RULESET)
        result = checker.check("这里的password是123456")
        
        assert result.passed is False  # 有CRITICAL违规
        assert len(result.violations) > 0
        assert result.score < 100.0
    
    def test_check_with_keyword_rule(self):
        """测试关键词规则检查"""
        ruleset = RuleSet(
            name="测试",
            rules=[
                Rule(
                    id="test-keyword",
                    name="关键词测试",
                    description="测试关键词",
                    type=RuleType.KEYWORD,
                    severity=Severity.HIGH,
                    keywords=["禁止词"]
                )
            ]
        )
        
        checker = ComplianceChecker(ruleset)
        
        result = checker.check("包含禁止词的内容")
        assert len(result.violations) == 1
        assert result.violations[0].rule_id == "test-keyword"
        
        result = checker.check("正常内容")
        assert len(result.violations) == 0
    
    def test_check_with_pattern_rule(self):
        """测试正则规则检查"""
        ruleset = RuleSet(
            name="测试",
            rules=[
                Rule(
                    id="test-pattern",
                    name="正则测试",
                    description="测试正则",
                    type=RuleType.PATTERN,
                    severity=Severity.MEDIUM,
                    pattern=r"\d{4}-\d{4}-\d{4}-\d{4}"
                )
            ]
        )
        
        checker = ComplianceChecker(ruleset)
        
        result = checker.check("卡号: 1234-5678-9012-3456")
        assert len(result.violations) == 1
        
        result = checker.check("没有卡号")
        assert len(result.violations) == 0
    
    def test_batch_check(self):
        """测试批量检查"""
        checker = ComplianceChecker(DEFAULT_RULESET)
        contents = [
            "正常内容",
            "包含password的内容",
            "另一个正常内容"
        ]
        
        results = checker.batch_check(contents)
        assert len(results) == 3
        assert results[0].passed is True
        assert results[1].passed is False
        assert results[2].passed is True
    
    def test_check_by_category(self):
        """测试按分类检查"""
        checker = ComplianceChecker(DEFAULT_RULESET)
        result = checker.check_by_category("包含password", "safety")
        
        # 只检查safety分类，应该有违规
        assert len(result.violations) > 0
    
    def test_rules_summary(self):
        """测试规则摘要"""
        checker = ComplianceChecker(DEFAULT_RULESET)
        summary = checker.get_rules_summary()
        
        assert "total_rules" in summary
        assert "enabled_rules" in summary
        assert "by_severity" in summary
        assert summary["total_rules"] > 0


class TestCheckResult:
    """测试CheckResult类"""
    
    def test_result_creation(self):
        """测试结果创建"""
        from agentguard.checker import Violation
        
        violation = Violation(
            rule_id="test-001",
            rule_name="测试规则",
            severity=Severity.HIGH.value,
            description="测试",
            type=RuleType.KEYWORD.value
        )
        
        result = CheckResult(
            content="测试内容",
            passed=False,
            violations=[violation],
            score=85.0
        )
        
        assert result.passed is False
        assert result.score == 85.0
        assert len(result.violations) == 1
    
    def test_get_violations_by_severity(self):
        """测试按严重程度获取违规"""
        from agentguard.checker import Violation
        from datetime import datetime
        
        violations = [
            Violation("1", "规则1", Severity.CRITICAL.value, "描述", "type"),
            Violation("2", "规则2", Severity.HIGH.value, "描述", "type"),
            Violation("3", "规则3", Severity.CRITICAL.value, "描述", "type"),
        ]
        
        result = CheckResult(
            content="测试",
            passed=False,
            violations=violations,
            score=50.0,
            check_time=datetime.now()
        )
        
        critical = result.get_critical_violations()
        assert len(critical) == 2
        
        high = result.get_high_violations()
        assert len(high) == 1
