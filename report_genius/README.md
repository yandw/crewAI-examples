# Report Genius: AI 报告生成协作系统

## 简介

Report Genius 是一个多 Agent 协作项目，展示了如何使用 CrewAI 框架自动创建全面的报告。CrewAI 协调自主 AI Agent，使它们能够协作并高效执行复杂任务，从而生成各种主题的高质量报告。

## CrewAI 框架

CrewAI 旨在促进角色扮演 AI Agent 之间的协作。在这个示例中，这些 Agent 共同合作创建全面的报告，确保彻底的研究、准确的分析和专业的呈现。

## 设置和安装

1. **克隆仓库**: 将此仓库克隆到您的本地机器。

2. **配置环境**: 
   - 复制 `.env.example` 到 `.env`
   - 配置 AI 模型 API（选择以下一种方式）:
     - **使用 OpenAI API**: 添加您的 OpenAI API 密钥: `OPENAI_API_KEY=your-api-key`
     - **使用 Azure OpenAI API**: 配置以下环境变量:
       ```
       AZURE_OPENAI_API_KEY=your-azure-openai-api-key
       AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
       AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
       AZURE_OPENAI_MODEL_NAME=gpt-4o
       AZURE_OPENAI_API_VERSION=2025-01-01-preview
       ```
   - 可选添加 Serper API 密钥用于网络搜索: `SERPER_API_KEY=your-serper-api-key`

3. **安装依赖**: 
   ```bash
   pip install -e .
   ```
   或者如果您使用 Poetry:
   ```bash
   poetry install
   ```

**注意**: 此项目默认使用 GPT-4。您应该拥有 GPT-4 API 的访问权限（通过 OpenAI 或 Azure OpenAI）才能有效运行它。

**免责声明**: 使用 GPT-4 将产生 API 费用。您可以在 `src/report_genius/crew.py` 中修改模型以使用不同的模型，但结果可能会有所不同。

## 运行项目

您可以通过两种方式运行 Report Genius:

### 1. 交互模式

运行主脚本并按照提示输入您的报告详情:

```bash
python run.py
```

您将被要求提供:
- 报告主题
- 报告类型（研究、分析、市场、技术等）
- 目标受众
- 期望长度
- 任何特殊要求

### 2. 使用示例脚本

对于快速演示，运行示例脚本:

```bash
python examples/generate_report.py
```

这将生成一份关于"医疗保健中的人工智能"的示例报告。



## 项目结构

- **`src/report_genius/main.py`**: 交互模式的入口点。
- **`src/report_genius/crew.py`**: Report Genius 团队的核心实现。
- **`src/report_genius/config/`**: 配置目录
  - **`agents.yaml`**: 定义 Agent（研究员、分析师、作家、编辑）。
  - **`tasks.yaml`**: 定义每个 Agent 的任务。
- **`src/report_genius/tools/`**: 包含工具实现
  - **`web_search_tool.py`**: 网络搜索工具。
- **`examples/`**: 包含演示使用方法的示例脚本。

## 自定义

您可以通过以下方式自定义 Report Genius:

1. **修改 Agent**: 编辑 `src/report_genius/config/agents.yaml` 以更改 Agent 角色、目标或背景故事。
2. **调整任务**: 编辑 `src/report_genius/config/tasks.yaml` 以修改任务描述或预期输出。
3. **添加工具**: 在 `src/report_genius/tools/` 目录中创建新工具，并更新 `crew.py` 中的 `tools` 列表。

## 许可证

本项目基于 MIT 许可证发布。

## 测试API连接

在运行完整项目之前，请确保您的API密钥已正确设置在.env文件中，并且有足够的API额度。

您可以通过运行以下命令来测试项目是否能正常工作：

```bash
python run.py
```

如果您看到交互式提示，说明您的环境配置正确。