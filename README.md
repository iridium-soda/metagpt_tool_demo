# metagpt_tool_demo
A simple demo to show how metagpt uses agents, memories and tools.

![Design framework](https://ooo.0x0.ooo/2024/07/22/ORtOnp.png)

## Install

Before running this demo, you should have:

- Python>=3.9 and <3.12
- Conda & Miniconda
- A reliable LLM api source


```shell
conda create -n tool_demo python=3.10 && conda activate tool_demo
pip install metagpt
```

Initialize LLM API configs refering the [guidance](https://docs.deepwisdom.ai/main/zh/guide/get_started/configuration/llm_api_configuration.html)

