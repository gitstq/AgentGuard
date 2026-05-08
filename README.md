# AgentGuard

AI Agent Behavior Compliance Guardian - 轻量级AI Agent行为准则管理与合规检查工具

## 项目方案设计

### 核心功能
1. **行为准则定义** - 使用YAML/JSON定义Agent行为规则
2. **实时合规检查** - 检查Agent输出是否符合预定义规则
3. **违规报告生成** - 生成详细的合规性报告
4. **规则库管理** - 内置常见行业规则模板
5. **CI/CD集成** - 支持GitHub Actions等流水线集成

### 技术栈
- Python 3.9+
- Pydantic (数据验证)
- Typer (CLI框架)
- PyYAML (配置解析)
- Rich (终端美化)

### 项目结构
```
agentguard/
├── agentguard/          # 核心源码
│   ├── __init__.py
│   ├── cli.py           # CLI入口
│   ├── checker.py       # 合规检查引擎
│   ├── rules.py         # 规则定义
│   ├── report.py        # 报告生成
│   └── templates/       # 规则模板
├── tests/               # 测试用例
├── docs/                # 文档
├── examples/            # 示例
├── pyproject.toml       # 项目配置
├── requirements.txt     # 依赖
└── README.md            # 说明文档
```

### 差异化亮点
1. 轻量级设计，零依赖部署
2. 支持自定义规则DSL
3. 多维度评分机制
4. 与parlant互补而非竞争
