<div align="center">

# 🛡️ AgentGuard

**AI Agent Behavior Compliance Guardian**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-orange)](https://pypi.org/)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Introduction

**AgentGuard** is a lightweight AI Agent behavior compliance management and checking tool designed to help developers ensure that AI Agent outputs comply with predefined safety, quality, and compliance standards.

### 💡 Why AgentGuard?

In the era of rapid AI development, ensuring that AI Agents output safe, compliant, and high-quality content has become a critical challenge. AgentGuard provides a simple yet powerful solution:

- 🔒 **Security Protection** - Detect sensitive information leaks and malicious code
- 📊 **Quality Assurance** - Ensure output content meets quality standards
- ⚖️ **Compliance Checks** - Verify adherence to industry regulations and ethical standards
- 🚀 **Easy Integration** - Lightweight design, quick integration into existing workflows

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🛡️ **Multi-dimensional Rule Engine** | Supports keyword matching, regex patterns, length checks, and custom functions |
| 📋 **Rich Rule Templates** | Built-in security, quality, and compliance rule templates |
| 🎯 **Severity Grading** | Critical/High/Medium/Low/Info five-level severity classification |
| 📈 **Compliance Scoring** | Intelligent scoring system to quantify compliance levels |
| 🖥️ **Beautiful CLI Interface** | Terminal UI based on Rich library for excellent visual experience |
| 📄 **Multi-format Reports** | Supports Console/JSON/HTML/Markdown report export |
| 🔧 **CI/CD Integration** | Supports GitHub Actions and other automated pipelines |
| 🌍 **Multi-language Support** | Supports Chinese and English content checking |

---

## 🚀 Quick Start

### 📦 Installation

```bash
# Install via pip
pip install agentguard

# Or install from source
git clone https://github.com/gitstq/AgentGuard.git
cd AgentGuard
pip install -e .
```

### 🎯 Basic Usage

```bash
# Check single content
agentguard check "Content to check"

# Check file content
agentguard check path/to/file.txt

# Use custom rule set
agentguard check content.txt --rules my_rules.yaml

# Export HTML report
agentguard check content.txt --format html --output report.html
```

### 💻 Python API

```python
from agentguard import ComplianceChecker
from agentguard.rules import DEFAULT_RULESET

# Create checker
checker = ComplianceChecker(DEFAULT_RULESET)

# Check content
result = checker.check("Content to check")

print(f"Passed: {result.passed}")
print(f"Score: {result.score}")
print(f"Violations: {len(result.violations)}")

for v in result.violations:
    print(f"- [{v.severity}] {v.rule_name}")
```

---

## 📖 Detailed Usage Guide

### 🛠️ Rule Management

```bash
# List all rules
agentguard rules list

# View specific rule details
agentguard rules show --id safety-001

# Create custom rule set
agentguard rules create --file my_rules.yaml

# Validate rule file
agentguard rules validate --file my_rules.yaml
```

### 📊 Batch Check

```bash
# Batch check all files in directory
agentguard batch ./content_dir --pattern "*.txt" --output report.html
```

### 🏗️ Project Initialization

```bash
# Initialize AgentGuard project
agentguard init ./my_project
```

---

## 💡 Design Philosophy & Roadmap

### 🎯 Design Philosophy

AgentGuard follows the "lightweight, flexible, and easy to integrate" design philosophy:

- **Lightweight Core** - Only includes necessary functions, no bloat
- **Flexible Configuration** - Supports YAML/JSON rule definitions
- **Easy Integration** - Provides CLI and Python API
- **Extensible Architecture** - Supports custom rule types

### 🗺️ Roadmap

- [x] Core rule engine
- [x] CLI tool
- [x] Report generation
- [x] Built-in rule templates
- [ ] PyPI release
- [ ] Web UI dashboard
- [ ] Real-time monitoring
- [ ] Multi-model support

---

## 📦 Packaging & Deployment

### 📋 Requirements

- Python 3.9+
- Dependencies: typer, pydantic, pyyaml, rich, jsonschema

### 🔨 Build & Install

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build package
python -m build
```

---

## 🤝 Contributing

We welcome contributions of all kinds!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**AgentGuard** 是一款轻量级AI Agent行为准则管理与合规检查工具，旨在帮助开发者确保AI Agent的输出符合预定义的安全、质量和合规标准。

### 💡 为什么选择AgentGuard？

在AI快速发展的时代，确保AI Agent输出安全、合规、高质量的内容已成为关键挑战。AgentGuard提供了一个简单而强大的解决方案：

- 🔒 **安全防护** - 检测敏感信息泄露和恶意代码
- 📊 **质量保障** - 确保输出内容符合质量标准
- ⚖️ **合规检查** - 验证是否符合行业规范和道德标准
- 🚀 **易于集成** - 轻量级设计，快速集成到现有工作流

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🛡️ **多维度规则引擎** | 支持关键词匹配、正则表达式、长度检查、自定义函数 |
| 📋 **丰富的规则模板** | 内置安全、质量、合规等规则模板 |
| 🎯 **严重程度分级** | Critical/High/Medium/Low/Info 五级严重程度 |
| 📈 **合规评分** | 智能评分系统，量化合规水平 |
| 🖥️ **美观的CLI界面** | 基于Rich库的终端UI，视觉体验优秀 |
| 📄 **多格式报告** | 支持Console/JSON/HTML/Markdown报告导出 |
| 🔧 **CI/CD集成** | 支持GitHub Actions等自动化流水线 |
| 🌍 **多语言支持** | 支持中英文内容检查 |

---

## 🚀 快速开始

### 📦 安装

```bash
# 通过pip安装
pip install agentguard

# 或从源码安装
git clone https://github.com/gitstq/AgentGuard.git
cd AgentGuard
pip install -e .
```

### 🎯 基础使用

```bash
# 检查单个内容
agentguard check "要检查的内容"

# 检查文件内容
agentguard check path/to/file.txt

# 使用自定义规则集
agentguard check content.txt --rules my_rules.yaml

# 导出HTML报告
agentguard check content.txt --format html --output report.html
```

### 💻 Python API

```python
from agentguard import ComplianceChecker
from agentguard.rules import DEFAULT_RULESET

# 创建检查器
checker = ComplianceChecker(DEFAULT_RULESET)

# 检查内容
result = checker.check("要检查的内容")

print(f"是否通过: {result.passed}")
print(f"合规分数: {result.score}")
print(f"违规数量: {len(result.violations)}")

for v in result.violations:
    print(f"- [{v.severity}] {v.rule_name}")
```

---

## 📖 详细使用指南

### 🛠️ 规则管理

```bash
# 列出所有规则
agentguard rules list

# 查看特定规则详情
agentguard rules show --id safety-001

# 创建自定义规则集
agentguard rules create --file my_rules.yaml

# 验证规则文件
agentguard rules validate --file my_rules.yaml
```

### 📊 批量检查

```bash
# 批量检查目录下所有文件
agentguard batch ./content_dir --pattern "*.txt" --output report.html
```

### 🏗️ 项目初始化

```bash
# 初始化AgentGuard项目
agentguard init ./my_project
```

---

## 💡 设计思路与迭代规划

### 🎯 设计理念

AgentGuard遵循"轻量、灵活、易集成"的设计理念：

- **轻量核心** - 仅包含必要功能，无冗余
- **灵活配置** - 支持YAML/JSON规则定义
- **易于集成** - 提供CLI和Python API
- **可扩展架构** - 支持自定义规则类型

### 🗺️ 迭代计划

- [x] 核心规则引擎
- [x] CLI工具
- [x] 报告生成
- [x] 内置规则模板
- [ ] PyPI发布
- [ ] Web UI仪表盘
- [ ] 实时监控
- [ ] 多模型支持

---

## 📦 打包与部署

### 📋 环境要求

- Python 3.9+
- 依赖项: typer, pydantic, pyyaml, rich, jsonschema

### 🔨 构建与安装

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 构建包
python -m build
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献规范。

---

## 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**AgentGuard** 是一款輕量級AI Agent行為準則管理與合規檢查工具，旨在幫助開發者確保AI Agent的輸出符合預定義的安全、質量和合規標準。

### 💡 為什麼選擇AgentGuard？

在AI快速發展的時代，確保AI Agent輸出安全、合規、高質量的內容已成為關鍵挑戰。AgentGuard提供了一個簡單而強大的解決方案：

- 🔒 **安全防護** - 檢測敏感信息洩露和惡意代碼
- 📊 **質量保障** - 確保輸出內容符合質量標準
- ⚖️ **合規檢查** - 驗證是否符合行業規範和道德標準
- 🚀 **易於集成** - 輕量級設計，快速集成到現有工作流

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🛡️ **多維度規則引擎** | 支持關鍵詞匹配、正則表達式、長度檢查、自定義函數 |
| 📋 **豐富的規則模板** | 內置安全、質量、合規等規則模板 |
| 🎯 **嚴重程度分級** | Critical/High/Medium/Low/Info 五級嚴重程度 |
| 📈 **合規評分** | 智能評分系統，量化合規水平 |
| 🖥️ **美觀的CLI界面** | 基於Rich庫的終端UI，視覺體驗優秀 |
| 📄 **多格式報告** | 支持Console/JSON/HTML/Markdown報告導出 |
| 🔧 **CI/CD集成** | 支持GitHub Actions等自動化流水線 |
| 🌍 **多語言支持** | 支持中英文內容檢查 |

---

## 🚀 快速開始

### 📦 安裝

```bash
# 通過pip安裝
pip install agentguard

# 或從源碼安裝
git clone https://github.com/gitstq/AgentGuard.git
cd AgentGuard
pip install -e .
```

### 🎯 基礎使用

```bash
# 檢查單個內容
agentguard check "要檢查的內容"

# 檢查文件內容
agentguard check path/to/file.txt

# 使用自定義規則集
agentguard check content.txt --rules my_rules.yaml

# 導出HTML報告
agentguard check content.txt --format html --output report.html
```

### 💻 Python API

```python
from agentguard import ComplianceChecker
from agentguard.rules import DEFAULT_RULESET

# 創建檢查器
checker = ComplianceChecker(DEFAULT_RULESET)

# 檢查內容
result = checker.check("要檢查的內容")

print(f"是否通過: {result.passed}")
print(f"合規分數: {result.score}")
print(f"違規數量: {len(result.violations)}")

for v in result.violations:
    print(f"- [{v.severity}] {v.rule_name}")
```

---

## 📖 詳細使用指南

### 🛠️ 規則管理

```bash
# 列出所有規則
agentguard rules list

# 查看特定規則詳情
agentguard rules show --id safety-001

# 創建自定義規則集
agentguard rules create --file my_rules.yaml

# 驗證規則文件
agentguard rules validate --file my_rules.yaml
```

### 📊 批量檢查

```bash
# 批量檢查目錄下所有文件
agentguard batch ./content_dir --pattern "*.txt" --output report.html
```

### 🏗️ 專案初始化

```bash
# 初始化AgentGuard專案
agentguard init ./my_project
```

---

## 💡 設計思路與迭代規劃

### 🎯 設計理念

AgentGuard遵循"輕量、靈活、易集成"的設計理念：

- **輕量核心** - 僅包含必要功能，無冗餘
- **靈活配置** - 支持YAML/JSON規則定義
- **易於集成** - 提供CLI和Python API
- **可擴展架構** - 支持自定義規則類型

### 🗺️ 迭代計劃

- [x] 核心規則引擎
- [x] CLI工具
- [x] 報告生成
- [x] 內置規則模板
- [ ] PyPI發布
- [ ] Web UI儀表盤
- [ ] 實時監控
- [ ] 多模型支持

---

## 📦 打包與部署

### 📋 環境要求

- Python 3.9+
- 依賴項: typer, pydantic, pyyaml, rich, jsonschema

### 🔨 構建與安裝

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest

# 構建包
python -m build
```

---

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！

1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某個特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 創建 Pull Request

請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細的貢獻規範。

---

## 📄 開源協議

本專案採用 MIT 協議開源 - 詳見 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by AgentGuard Team**

⭐ Star this repo if you find it helpful!

</div>
