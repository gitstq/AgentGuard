"""
AgentGuard Rules Module

规则定义与管理模块
"""

from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import yaml
import json


class RuleType(str, Enum):
    """规则类型枚举"""
    PATTERN = "pattern"           # 正则匹配规则
    KEYWORD = "keyword"           # 关键词规则
    LENGTH = "length"             # 长度限制规则
    CUSTOM = "custom"             # 自定义函数规则
    SAFETY = "safety"             # 安全检查规则
    CONTENT = "content"           # 内容质量规则


class Severity(str, Enum):
    """严重程度枚举"""
    CRITICAL = "critical"         # 严重违规
    HIGH = "high"                 # 高风险
    MEDIUM = "medium"            # 中等风险
    LOW = "low"                   # 低风险
    INFO = "info"                 # 信息提示


class Rule(BaseModel):
    """单个规则定义"""
    id: str = Field(..., description="规则唯一标识")
    name: str = Field(..., description="规则名称")
    description: str = Field(..., description="规则描述")
    type: RuleType = Field(..., description="规则类型")
    severity: Severity = Field(default=Severity.MEDIUM, description="严重程度")
    
    # 规则配置
    pattern: Optional[str] = Field(None, description="正则表达式模式")
    keywords: Optional[List[str]] = Field(None, description="关键词列表")
    min_length: Optional[int] = Field(None, description="最小长度")
    max_length: Optional[int] = Field(None, description="最大长度")
    allowed_values: Optional[List[str]] = Field(None, description="允许的值列表")
    blocked_values: Optional[List[str]] = Field(None, description="禁止的值列表")
    
    # 自定义函数配置
    custom_function: Optional[str] = Field(None, description="自定义检查函数名")
    
    # 规则元数据
    enabled: bool = Field(default=True, description="是否启用")
    tags: List[str] = Field(default_factory=list, description="规则标签")
    category: Optional[str] = Field(None, description="规则分类")
    
    @field_validator('severity', mode='before')
    @classmethod
    def validate_severity(cls, v):
        if isinstance(v, str):
            return Severity(v.lower())
        return v
    
    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, str):
            return RuleType(v.lower())
        return v
    
    def matches(self, content: str) -> bool:
        """检查内容是否匹配此规则"""
        if not self.enabled:
            return False
        
        if self.type == RuleType.PATTERN and self.pattern:
            import re
            return bool(re.search(self.pattern, content, re.IGNORECASE))
        
        elif self.type == RuleType.KEYWORD and self.keywords:
            content_lower = content.lower()
            return any(kw.lower() in content_lower for kw in self.keywords)
        
        elif self.type == RuleType.LENGTH:
            length = len(content)
            if self.min_length and length < self.min_length:
                return True
            if self.max_length and length > self.max_length:
                return True
            return False
        
        elif self.type == RuleType.CONTENT:
            if self.blocked_values:
                return any(bv.lower() in content.lower() for bv in self.blocked_values)
        
        return False
    
    def check(self, content: str) -> Dict[str, Any]:
        """执行规则检查并返回结果"""
        is_violation = self.matches(content)
        
        return {
            "rule_id": self.id,
            "rule_name": self.name,
            "violated": is_violation,
            "severity": self.severity.value,
            "description": self.description,
            "type": self.type.value,
        }


class RuleSet(BaseModel):
    """规则集合定义"""
    name: str = Field(..., description="规则集名称")
    version: str = Field(default="1.0.0", description="规则集版本")
    description: str = Field(default="", description="规则集描述")
    rules: List[Rule] = Field(default_factory=list, description="规则列表")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    def add_rule(self, rule: Rule) -> None:
        """添加规则到规则集"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_id: str) -> bool:
        """从规则集中移除规则"""
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                self.rules.pop(i)
                return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """获取指定规则"""
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None
    
    def get_enabled_rules(self) -> List[Rule]:
        """获取所有启用的规则"""
        return [r for r in self.rules if r.enabled]
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """获取指定分类的规则"""
        return [r for r in self.rules if r.category == category]
    
    def get_rules_by_severity(self, severity: Severity) -> List[Rule]:
        """获取指定严重程度的规则"""
        return [r for r in self.rules if r.severity == severity]
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "RuleSet":
        """从YAML文件加载规则集"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_path: str) -> "RuleSet":
        """从JSON文件加载规则集"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
    
    def to_yaml(self, yaml_path: str) -> None:
        """保存规则集到YAML文件"""
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.model_dump(), f, allow_unicode=True, default_flow_style=False)
    
    def to_json(self, json_path: str) -> None:
        """保存规则集到JSON文件"""
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.model_dump(), f, ensure_ascii=False, indent=2)


# 内置规则模板
DEFAULT_RULESET = RuleSet(
    name="default",
    version="1.0.0",
    description="默认规则集，包含基础安全检查",
    rules=[
        # 安全类规则
        Rule(
            id="safety-001",
            name="禁止敏感信息泄露",
            description="检查是否包含敏感信息如密码、密钥等",
            type=RuleType.KEYWORD,
            severity=Severity.CRITICAL,
            keywords=["password", "secret", "api_key", "token", "密钥", "密码"],
            tags=["安全", "隐私"],
            category="safety"
        ),
        Rule(
            id="safety-002",
            name="禁止恶意代码模式",
            description="检测常见的恶意代码模式",
            type=RuleType.PATTERN,
            severity=Severity.CRITICAL,
            pattern=r"(eval|exec|__import__|subprocess)\s*\(",
            tags=["安全", "代码"],
            category="safety"
        ),
        Rule(
            id="safety-003",
            name="禁止SQL注入模式",
            description="检测潜在的SQL注入风险",
            type=RuleType.PATTERN,
            severity=Severity.HIGH,
            pattern=r"(SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\+\s*|['\"].*['\"].*\+",
            tags=["安全", "数据库"],
            category="safety"
        ),
        
        # 内容质量规则
        Rule(
            id="quality-001",
            name="最小响应长度检查",
            description="确保响应内容达到最小长度",
            type=RuleType.LENGTH,
            severity=Severity.LOW,
            min_length=10,
            tags=["质量"],
            category="quality"
        ),
        Rule(
            id="quality-002",
            name="最大响应长度检查",
            description="确保响应内容不超过最大长度",
            type=RuleType.LENGTH,
            severity=Severity.LOW,
            max_length=10000,
            tags=["质量"],
            category="quality"
        ),
        
        # 合规性规则
        Rule(
            id="compliance-001",
            name="禁止歧视性语言",
            description="检测是否包含歧视性或偏见性语言",
            type=RuleType.KEYWORD,
            severity=Severity.HIGH,
            keywords=["歧视", "偏见"],
            tags=["合规", "道德"],
            category="compliance"
        ),
        Rule(
            id="compliance-002",
            name="禁止虚假信息",
            description="检测潜在的虚假或误导性信息",
            type=RuleType.PATTERN,
            severity=Severity.MEDIUM,
            pattern=r"(绝对|100%|保证|一定|肯定).*(没有问题|没问题|可以|行)",
            tags=["合规", "准确性"],
            category="compliance"
        ),
    ]
)
