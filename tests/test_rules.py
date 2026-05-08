"""
Tests for rules module
"""

import pytest
from agentguard.rules import Rule, RuleSet, RuleType, Severity, DEFAULT_RULESET


class TestRule:
    """测试Rule类"""
    
    def test_rule_creation(self):
        """测试规则创建"""
        rule = Rule(
            id="test-001",
            name="测试规则",
            description="这是一个测试规则",
            type=RuleType.KEYWORD,
            severity=Severity.HIGH,
            keywords=["测试", "test"]
        )
        
        assert rule.id == "test-001"
        assert rule.name == "测试规则"
        assert rule.enabled is True
    
    def test_keyword_matching(self):
        """测试关键词匹配"""
        rule = Rule(
            id="test-002",
            name="关键词规则",
            description="测试关键词匹配",
            type=RuleType.KEYWORD,
            keywords=["密码", "password"]
        )
        
        assert rule.matches("这里包含密码信息") is True
        assert rule.matches("请输入password") is True
        assert rule.matches("正常内容") is False
    
    def test_pattern_matching(self):
        """测试正则匹配"""
        rule = Rule(
            id="test-003",
            name="正则规则",
            description="测试正则匹配",
            type=RuleType.PATTERN,
            pattern=r"\d{4}-\d{2}-\d{2}"
        )
        
        assert rule.matches("日期是2024-01-15") is True
        assert rule.matches("没有日期") is False
    
    def test_length_matching(self):
        """测试长度匹配"""
        rule = Rule(
            id="test-004",
            name="长度规则",
            description="测试长度限制",
            type=RuleType.LENGTH,
            min_length=10,
            max_length=100
        )
        
        assert rule.matches("太短") is True  # 长度 < 10
        assert rule.matches("这是一个非常长的内容" * 10) is True  # 长度 > 100
        assert rule.matches("合适的长度内容") is False  # 10 <= 长度 <= 100
    
    def test_disabled_rule(self):
        """测试禁用规则"""
        rule = Rule(
            id="test-005",
            name="禁用规则",
            description="测试禁用状态",
            type=RuleType.KEYWORD,
            keywords=["测试"],
            enabled=False
        )
        
        assert rule.matches("包含测试") is False


class TestRuleSet:
    """测试RuleSet类"""
    
    def test_ruleset_creation(self):
        """测试规则集创建"""
        ruleset = RuleSet(
            name="测试规则集",
            version="1.0.0",
            description="测试用规则集"
        )
        
        assert ruleset.name == "测试规则集"
        assert len(ruleset.rules) == 0
    
    def test_add_remove_rule(self):
        """测试添加和移除规则"""
        ruleset = RuleSet(name="测试")
        rule = Rule(
            id="test-001",
            name="测试规则",
            description="测试",
            type=RuleType.KEYWORD
        )
        
        ruleset.add_rule(rule)
        assert len(ruleset.rules) == 1
        
        removed = ruleset.remove_rule("test-001")
        assert removed is True
        assert len(ruleset.rules) == 0
        
        removed = ruleset.remove_rule("not-exist")
        assert removed is False
    
    def test_get_rule(self):
        """测试获取规则"""
        ruleset = RuleSet(name="测试")
        rule = Rule(
            id="test-001",
            name="测试规则",
            description="测试",
            type=RuleType.KEYWORD
        )
        ruleset.add_rule(rule)
        
        found = ruleset.get_rule("test-001")
        assert found is not None
        assert found.name == "测试规则"
        
        not_found = ruleset.get_rule("not-exist")
        assert not_found is None
    
    def test_get_enabled_rules(self):
        """测试获取启用的规则"""
        ruleset = RuleSet(name="测试")
        ruleset.add_rule(Rule(
            id="enabled-001",
            name="启用规则",
            description="测试",
            type=RuleType.KEYWORD,
            enabled=True
        ))
        ruleset.add_rule(Rule(
            id="disabled-001",
            name="禁用规则",
            description="测试",
            type=RuleType.KEYWORD,
            enabled=False
        ))
        
        enabled = ruleset.get_enabled_rules()
        assert len(enabled) == 1
        assert enabled[0].id == "enabled-001"


class TestDefaultRuleSet:
    """测试默认规则集"""
    
    def test_default_ruleset_exists(self):
        """测试默认规则集存在"""
        assert DEFAULT_RULESET is not None
        assert len(DEFAULT_RULESET.rules) > 0
    
    def test_default_ruleset_has_safety_rules(self):
        """测试默认规则集包含安全规则"""
        safety_rules = DEFAULT_RULESET.get_rules_by_category("safety")
        assert len(safety_rules) > 0
    
    def test_default_ruleset_has_quality_rules(self):
        """测试默认规则集包含质量规则"""
        quality_rules = DEFAULT_RULESET.get_rules_by_category("quality")
        assert len(quality_rules) > 0
