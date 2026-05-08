"""
AgentGuard Checker Module

合规检查引擎模块
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re

from .rules import Rule, RuleSet, RuleType, Severity


@dataclass
class Violation:
    """违规记录"""
    rule_id: str
    rule_name: str
    severity: str
    description: str
    type: str
    position: Optional[int] = None
    matched_text: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class CheckResult:
    """检查结果"""
    content: str
    passed: bool
    violations: List[Violation] = field(default_factory=list)
    score: float = 100.0
    check_time: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    
    def get_critical_violations(self) -> List[Violation]:
        """获取严重违规"""
        return [v for v in self.violations if v.severity == Severity.CRITICAL.value]
    
    def get_high_violations(self) -> List[Violation]:
        """获取高风险违规"""
        return [v for v in self.violations if v.severity == Severity.HIGH.value]
    
    def get_violations_by_severity(self, severity: Severity) -> List[Violation]:
        """获取指定严重程度的违规"""
        return [v for v in self.violations if v.severity == severity.value]


class ComplianceChecker:
    """合规检查器"""
    
    def __init__(self, ruleset: Optional[RuleSet] = None):
        """
        初始化检查器
        
        Args:
            ruleset: 规则集，如果不提供则使用默认规则集
        """
        self.ruleset = ruleset or RuleSet(name="default", rules=[])
        self.custom_checkers: Dict[str, Callable] = {}
    
    def add_custom_checker(self, name: str, checker_func: Callable) -> None:
        """
        添加自定义检查函数
        
        Args:
            name: 检查器名称
            checker_func: 检查函数，接收content参数，返回bool表示是否违规
        """
        self.custom_checkers[name] = checker_func
    
    def check(self, content: str, rules: Optional[List[Rule]] = None) -> CheckResult:
        """
        执行合规检查
        
        Args:
            content: 要检查的内容
            rules: 要应用的规则列表，如果不提供则使用规则集中的所有启用规则
        
        Returns:
            CheckResult: 检查结果
        """
        import time
        start_time = time.time()
        
        rules_to_check = rules or self.ruleset.get_enabled_rules()
        violations: List[Violation] = []
        
        for rule in rules_to_check:
            violation = self._check_rule(content, rule)
            if violation:
                violations.append(violation)
        
        # 计算合规分数
        score = self._calculate_score(content, violations)
        
        # 判断是否通过检查
        passed = not any(
            v.severity in [Severity.CRITICAL.value, Severity.HIGH.value] 
            for v in violations
        )
        
        duration = (time.time() - start_time) * 1000
        
        return CheckResult(
            content=content,
            passed=passed,
            violations=violations,
            score=score,
            duration_ms=duration
        )
    
    def _check_rule(self, content: str, rule: Rule) -> Optional[Violation]:
        """检查单个规则"""
        if not rule.enabled:
            return None
        
        is_violation = False
        matched_text = None
        position = None
        
        if rule.type == RuleType.PATTERN and rule.pattern:
            match = re.search(rule.pattern, content, re.IGNORECASE)
            if match:
                is_violation = True
                matched_text = match.group()
                position = match.start()
        
        elif rule.type == RuleType.KEYWORD and rule.keywords:
            content_lower = content.lower()
            for keyword in rule.keywords:
                if keyword.lower() in content_lower:
                    is_violation = True
                    # 找到匹配位置
                    pos = content_lower.find(keyword.lower())
                    if position is None or pos < position:
                        position = pos
                        matched_text = content[pos:pos + len(keyword)]
        
        elif rule.type == RuleType.LENGTH:
            length = len(content)
            if rule.min_length and length < rule.min_length:
                is_violation = True
                matched_text = f"长度 {length} < 最小 {rule.min_length}"
            elif rule.max_length and length > rule.max_length:
                is_violation = True
                matched_text = f"长度 {length} > 最大 {rule.max_length}"
        
        elif rule.type == RuleType.CONTENT:
            if rule.blocked_values:
                for blocked in rule.blocked_values:
                    if blocked.lower() in content.lower():
                        is_violation = True
                        pos = content.lower().find(blocked.lower())
                        if position is None or pos < position:
                            position = pos
                            matched_text = blocked
        
        elif rule.type == RuleType.CUSTOM and rule.custom_function:
            if rule.custom_function in self.custom_checkers:
                is_violation = self.custom_checkers[rule.custom_function](content)
        
        if is_violation:
            return Violation(
                rule_id=rule.id,
                rule_name=rule.name,
                severity=rule.severity.value,
                description=rule.description,
                type=rule.type.value,
                position=position,
                matched_text=matched_text,
                suggestion=self._generate_suggestion(rule)
            )
        
        return None
    
    def _calculate_score(self, content: str, violations: List[Violation]) -> float:
        """计算合规分数"""
        if not violations:
            return 100.0
        
        # 根据违规严重程度扣分
        severity_weights = {
            Severity.CRITICAL.value: 30,
            Severity.HIGH.value: 15,
            Severity.MEDIUM.value: 5,
            Severity.LOW.value: 2,
            Severity.INFO.value: 0
        }
        
        total_penalty = sum(
            severity_weights.get(v.severity, 5) 
            for v in violations
        )
        
        score = max(0, 100 - total_penalty)
        return round(score, 2)
    
    def _generate_suggestion(self, rule: Rule) -> Optional[str]:
        """生成改进建议"""
        suggestions = {
            "safety-001": "请移除或替换敏感信息，使用占位符如***或[REDACTED]",
            "safety-002": "避免使用eval/exec等危险函数，考虑使用更安全的替代方案",
            "safety-003": "使用参数化查询或ORM来防止SQL注入",
            "quality-001": "请提供更详细的响应内容",
            "quality-002": "响应内容过长，请精简或分段输出",
            "compliance-001": "请使用中立、包容的语言",
            "compliance-002": "避免使用绝对化的表述，使用更谨慎的措辞",
        }
        return suggestions.get(rule.id, "请检查并修正此问题")
    
    def batch_check(self, contents: List[str]) -> List[CheckResult]:
        """批量检查多个内容"""
        return [self.check(content) for content in contents]
    
    def check_with_rules(self, content: str, rule_ids: List[str]) -> CheckResult:
        """使用指定规则检查内容"""
        rules = [
            self.ruleset.get_rule(rid) 
            for rid in rule_ids 
            if self.ruleset.get_rule(rid)
        ]
        return self.check(content, rules)
    
    def check_by_category(self, content: str, category: str) -> CheckResult:
        """按分类检查内容"""
        rules = self.ruleset.get_rules_by_category(category)
        return self.check(content, rules)
    
    def get_rules_summary(self) -> Dict[str, Any]:
        """获取规则集摘要"""
        rules = self.ruleset.rules
        return {
            "total_rules": len(rules),
            "enabled_rules": len([r for r in rules if r.enabled]),
            "by_severity": {
                sev.value: len([r for r in rules if r.severity == sev])
                for sev in Severity
            },
            "by_category": {
                cat: len([r for r in rules if r.category == cat])
                for cat in set(r.category for r in rules if r.category)
            }
        }
