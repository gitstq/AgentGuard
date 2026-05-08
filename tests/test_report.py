"""
Tests for report module
"""

import pytest
import json
from datetime import datetime
from agentguard.report import ComplianceReport, ReportFormat
from agentguard.checker import CheckResult, Violation
from agentguard.rules import Severity


class TestComplianceReport:
    """测试ComplianceReport类"""
    
    def test_report_creation(self):
        """测试报告创建"""
        report = ComplianceReport()
        assert report.results == []
        assert report.report_name == "AgentGuard Compliance Report"
    
    def test_add_result(self):
        """测试添加结果"""
        report = ComplianceReport()
        result = CheckResult(
            content="测试",
            passed=True,
            score=100.0
        )
        
        report.add_result(result)
        assert len(report.results) == 1
    
    def test_get_summary(self):
        """测试获取摘要"""
        report = ComplianceReport()
        
        # 添加通过的结果
        report.add_result(CheckResult(content="1", passed=True, score=100.0))
        # 添加失败的结果
        report.add_result(CheckResult(
            content="2",
            passed=False,
            score=70.0,
            violations=[
                Violation("1", "规则", Severity.HIGH.value, "描述", "type")
            ]
        ))
        
        summary = report.get_summary()
        
        assert summary["total_checks"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1
        assert summary["pass_rate"] == 50.0
        assert summary["average_score"] == 85.0
    
    def test_to_json(self):
        """测试JSON导出"""
        report = ComplianceReport()
        report.add_result(CheckResult(content="测试", passed=True, score=100.0))
        
        json_str = report.to_json()
        data = json.loads(json_str)
        
        assert data["report_name"] == "AgentGuard Compliance Report"
        assert "summary" in data
        assert "results" in data
    
    def test_to_markdown(self):
        """测试Markdown导出"""
        report = ComplianceReport()
        report.add_result(CheckResult(content="测试", passed=True, score=100.0))
        
        md = report.to_markdown()
        
        assert "# AgentGuard Compliance Report" in md
        assert "📊 Summary" in md
        assert "📋 Detailed Results" in md
    
    def test_to_html(self):
        """测试HTML导出"""
        report = ComplianceReport()
        report.add_result(CheckResult(content="测试", passed=True, score=100.0))
        
        html = report.to_html()
        
        assert "<!DOCTYPE html>" in html
        assert "AgentGuard Compliance Report" in html
        assert "<html" in html
