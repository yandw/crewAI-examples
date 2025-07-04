import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from crewai import Agent, Task, Crew, Process, LLM
from langchain_openai import ChatOpenAI
from .tools.web_search_tool import WebSearchTool

class ReportGeniusCrew:
    """用于生成综合报告的AI团队"""
    
    
    def __init__(self, topic: Optional[str] = None, report_type: Optional[str] = None, 
                 audience: Optional[str] = None, length: Optional[str] = None, 
                 special_requirements: Optional[str] = None, language: str = "中文"):
        # Store report parameters
        self.topic = topic
        self.report_type = report_type
        self.audience = audience
        self.length = length
        self.special_requirements = special_requirements or "None"
        self.language = language  # 添加语言参数，默认为中文
        
        # Initialize the language model
        # Check if using Azure OpenAI or regular OpenAI
        if os.environ.get("AZURE_OPENAI_API_KEY"):
            # 设置LiteLLM需要的环境变量
            os.environ['AZURE_API_KEY'] = os.environ.get("AZURE_OPENAI_API_KEY", "")
            os.environ['AZURE_API_BASE'] = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
            os.environ['AZURE_API_VERSION'] = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
            
            # 使用CrewAI的LLM类连接Azure OpenAI，优化参数以加快响应
            model_name = os.environ.get("AZURE_OPENAI_MODEL_NAME", "gpt-4o")
            self.llm = LLM(
                model=f"azure/{model_name}", 
                temperature=0.3,  # 降低温度以减少创造性，加快响应
                max_tokens=500,   # 限制输出长度
                request_timeout=30  # 设置请求超时时间
            )
        else:
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.7,
                api_key=os.environ.get("OPENAI_API_KEY")
            )
        
        # Initialize tools
        self.tools = [WebSearchTool()]
        
        # Load agents and tasks from config files
        self.agents_config = self._load_config("agents.yaml")
        self.tasks_config = self._load_config("tasks.yaml")
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """从YAML文件加载配置"""
        config_path = Path(__file__).parent / "config" / filename
        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    
    def _create_agents(self) -> Dict[str, Agent]:
        """根据配置创建代理"""
        agents: Dict[str, Agent] = {}
        
        for agent_id, config in self.agents_config.items():
            agent = Agent(
                role=config["role"],
                goal=config["goal"],
                backstory=config["backstory"],
                verbose=True,  # 设置为True以显示Agent执行过程
                allow_delegation=False,  # 禁用委派以减少交互
                tools=self.tools,
                llm=self.llm
            )
            agents[agent_id] = agent
        
        return agents
    
    def _create_tasks(self, agents: Dict[str, Agent]) -> List[Task]:
        """根据配置创建任务"""
        tasks: List[Task] = []
        
        for task_config in self.tasks_config:
            agent = agents[task_config["agent"]]
            
            # 使用报告详情格式化任务描述和预期输出
            description = task_config["description"]
            expected_output = task_config["expected_output"]
            
            # 只有当主题存在且描述中包含格式化占位符时才进行格式化
            if self.topic and "{topic}" in description:
                try:
                    description = description.format(
                        topic=self.topic,
                        report_type=self.report_type,
                        audience=self.audience,
                        length=self.length,
                        special_requirements=self.special_requirements
                    )
                    # 添加语言要求
                    description += f"\n请使用{self.language}撰写。"
                    
                    expected_output = expected_output.format(
                        topic=self.topic,
                        report_type=self.report_type,
                        audience=self.audience,
                        length=self.length,
                        special_requirements=self.special_requirements
                    )
                    # 添加语言要求
                    expected_output += f"\n必须使用{self.language}。"
                except KeyError as e:
                    print(f"格式化任务时出错: {e}")
            
            task = Task(
                description=description,
                expected_output=expected_output,
                agent=agent,
                tools=self.tools,
                async_execution=task_config.get("async_execution", False),
                output_file=task_config.get("output_file", None)
            )
            tasks.append(task)
        
        return tasks
    
    def crew(self) -> Crew:
        """创建并返回AI团队"""
        agents = self._create_agents()
        tasks = self._create_tasks(agents)
        
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True,  # 设置为True以显示Crew执行过程
            process=Process.sequential,
            max_rpm=20,  # 限制每分钟请求数
            memory=False  # 禁用记忆功能以减少处理时间
        )
        
        return crew
        
    def run(self, inputs: Optional[Dict[str, str]] = None) -> str:
        """使用给定的输入运行AI团队
        
        参数:
            inputs: 包含报告参数的字典
            
        返回:
            生成的报告字符串
        """
        # Update parameters if inputs are provided
        if inputs:
            self.topic = inputs.get("topic", self.topic)
            self.report_type = inputs.get("report_type", self.report_type)
            self.audience = inputs.get("audience", self.audience)
            self.length = inputs.get("length", self.length)
            self.special_requirements = inputs.get("special_requirements", self.special_requirements) or "None"
            self.language = inputs.get("language", self.language)  # 添加语言参数更新
        
        # Create and run the crew
        result = self.crew().kickoff()
        return result