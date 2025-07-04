# Report Genius 示例脚本

本目录包含使用 Report Genius 生成报告的示例脚本。

## 可用示例

### 1. 生成报告 (generate_report.py)

这个脚本演示了如何使用 Report Genius 生成一份关于人工智能在医疗领域的研究报告。

运行方式：

```bash
python examples/generate_report.py
```

### 2. 生成报告并保存到文件 (save_report_to_file.py)

这个脚本允许用户输入报告参数，生成报告并将其保存到本地文件中。

运行方式：

```bash
python examples/save_report_to_file.py
```

脚本会提示用户输入以下参数：
- 报告主题
- 报告类型
- 目标受众
- 报告长度
- 特殊要求

生成的报告将保存为 Markdown 文件，文件名包含主题和时间戳。

## 环境配置

在运行示例之前，请确保已正确配置环境变量。可以在项目根目录的 `.env` 文件中设置以下变量：

### 使用 OpenAI

```
OPENAI_API_KEY=your_openai_api_key
```

### 使用 Azure OpenAI

```
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_MODEL_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

## 注意事项

- 生成报告可能需要几分钟时间，取决于报告的复杂性和长度。
- 确保您的 API 密钥有足够的配额来处理请求。
- 生成的报告将以 Markdown 格式保存，可以使用任何支持 Markdown 的编辑器或查看器打开。