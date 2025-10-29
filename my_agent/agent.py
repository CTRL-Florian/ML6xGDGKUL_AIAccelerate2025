"""
This file is where you will implement your agent.
The `root_agent` is used to evaluate your agent's performance.
"""


from google.adk.agents import llm_agent
from my_agent.tools import web_search  
from my_agent.tools import file_reader 


root_agent = llm_agent.Agent(
    model='gemini-2.5-flash-lite',
    name='agent',
    description="A helpful assistant that can answer questions.",
    #instruction="You are a helpful assistant that answers questions directly and concisely.",
    instruction="""
...
**Core Directives:**

1. ... (Prioritize Explicit Commands)
2. ... (Reason Step-by-Step)
3. ... (Use Tools When Necessary - web_search)
4. ... (Process Text Literally)

# --- 修改这一条规则 ---
5.  **Handle File-Based Questions:**
    * If the user's question mentions an attached file (e.g., "summary.pdf", "data.json", "report.csv", "sheet.xlsx"), you **MUST** use the `read_file` tool to get the file's content.
    * This tool can read: `.txt`, `.pdf`, `.json`, `.csv`, and `.xlsx`.
    * Pass **only the filename** as the argument.
    * **CRITICAL:** If the file is an image (like `.png` or `.jpg`), this tool will fail. You must report that you need a *different* tool for image analysis.

Execute the user's request based on these directives.
""",
    tools=[web_search,
        file_reader.read_file],
    sub_agents=[],
)