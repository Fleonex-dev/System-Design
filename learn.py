import sys
import os
import subprocess
import json
import time
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
import questionary

# ==========================================
# 🎓 COURSE CONFIGURATION
# ==========================================
COURSE = [
    {
        "id": "01",
        "title": "🐍 Python Essentials",
        "path": "01_python_essentials",
        "lessons": [
            {"file": "01_concurrency.py", "title": "Concurrency (Async vs Sync)"},
            {"file": "02_typing.py", "title": "Typing (Pydantic vs Dicts)"},
            {"file": "03_generators.py", "title": "Generators (Stream vs List)"},
            {"file": "04_context_managers.py", "title": "Context Managers (Safety)"},
            {"file": "05_decorators.py", "title": "Decorators (Clean Code)"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "02",
        "title": "🧩 Low Level Design (LLD)",
        "path": "02_lld_principles",
        "lessons": [
            {"file": "01_solid_agents.py", "title": "SOLID Principles"},
            {"file": "02_factory.py", "title": "Factory Pattern"},
            {"file": "03_strategy.py", "title": "Strategy Pattern"},
            {"file": "04_observer.py", "title": "Observer Pattern"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "03",
        "title": "☁️ High Level Design (HLD)",
        "path": "03_hld_concepts",
        "lessons": [
            {"file": "01_llm_load_balancing.py", "title": "Load Balancing"},
            {"file": "02_semantic_caching.py", "title": "Semantic Caching"},
            {"file": "03_consistent_hashing.py", "title": "Consistent Hashing"},
            {"file": "04_distributed_id.py", "title": "Distributed IDs"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "04",
        "title": "🧠 Advanced AI Architecture",
        "path": "04_advanced_ai_arch",
        "lessons": [
            {"file": "01_rag_pipeline_optimization.py", "title": "RAG Optimization"},
            {"file": "02_agent_orchestrator.py", "title": "Agent Orchestration"},
            {"file": "03_inference_optimization.py", "title": "Speculative Decoding"},
            {"file": "04_mixture_of_experts.py", "title": "Mixture of Experts"},
            {"file": "05_reasoning_search.py", "title": "Reasoning (Tree of Thoughts)"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "05",
        "title": "💼 Interview Prep",
        "path": "05_interview_prep",
        "lessons": [
            {"file": "Q1_RateLimiter/optimal.py", "title": "Q1: Rate Limiter"},
            {"file": "Q2_URLShortener/optimal.py", "title": "Q2: URL Shortener"},
            {"file": "Q3_WebCrawler/optimal.py", "title": "Q3: Web Crawler"}
        ]
    }
]

# ==========================================
# 🛠️ ENGINE
# ==========================================
console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_header():
    clear()
    console.print(Panel.fit(
        "[bold cyan]🤖 AI System Design Course[/bold cyan]\n"
        "[dim]Use Arrow Keys to Navigate • Ctrl+C to Exit[/dim]",
        border_style="cyan"
    ))

def show_readme(path):
    readme_path = os.path.join(path, "README.md")
    if not os.path.exists(readme_path):
        console.print(f"[red]No README found at {readme_path}[/red]")
        input("Press Enter...")
        return

    with open(readme_path, "r") as f:
        md = Markdown(f.read())
    
    console.print(md)
    console.print("\n[dim]Press Enter to return...[/dim]")
    input()

def run_script(path, script_name):
    full_path = os.path.join(path, script_name)
    if not os.path.exists(full_path):
        console.print(f"[red]File not found: {full_path}[/red]")
        input("Press Enter...")
        return

    console.print(f"[green]🚀 Running {script_name}...[/green]\n")
    try:
        # Run and stream output
        subprocess.run([sys.executable, script_name], cwd=path)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    console.print("\n[dim]Execution Finished. Press Enter...[/dim]")
    input()

def view_code(path, script_name):
    full_path = os.path.join(path, script_name)
    with open(full_path, "r") as f:
        code = f.read()
    
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    console.print("\n[dim]Press Enter to return...[/dim]")
    input()

def lesson_menu(module, lesson):
    while True:
        render_header()
        console.print(f"[bold yellow]Module:[/bold yellow] {module['title']}")
        console.print(f"[bold green]Lesson:[/bold green] {lesson['title']}\n")
        
        # Determine "Bad" counterpart name (usually lesson filename is '01_x.py', bad might be inside or implied)
        # For this repo, 'bad' is usually the SAME file's first half or a separate function.
        # But wait, our curriculum put 'run_the_screwup' inside the SAME file.
        # So we just run the file.
        
        action = questionary.select(
            "What do you want to do?",
            choices=[
                "🚀 Run Script (See Bad vs Good)",
                "📄 View Code",
                "🔙 Back"
            ]
        ).ask()
        
        if action == "🔙 Back":
            break
        elif action == "🚀 Run Script (See Bad vs Good)":
            run_script(module['path'], lesson['file'])
        elif action == "📄 View Code":
            view_code(module['path'], lesson['file'])

def module_menu(module):
    while True:
        render_header()
        console.print(f"[bold yellow]Module:[/bold yellow] {module['title']}\n")
        
        choices = ["📖 Read Teacher Guide (README)"] + \
                  [f"{l['title']}" for l in module['lessons']] + \
                  ["🔙 Back to Main Menu"]
                  
        selection = questionary.select(
            "Select a Lesson:",
            choices=choices
        ).ask()
        
        if selection == "🔙 Back to Main Menu":
            break
        elif selection == "📖 Read Teacher Guide (README)":
            show_readme(module['path'])
        else:
            # Find lesson object
            lesson = next(l for l in module['lessons'] if l['title'] == selection)
            lesson_menu(module, lesson)

def main_menu():
    while True:
        render_header()
        
        choices = [m['title'] for m in COURSE] + ["❌ Exit"]
        
        selection = questionary.select(
            "Select a Module to Start:",
            choices=choices
        ).ask()
        
        if selection == "❌ Exit":
            console.print("[cyan]Happy Coding! Goodbye! 👋[/cyan]")
            sys.exit(0)
            
        # Find module object
        module = next(m for m in COURSE if m['title'] == selection)
        module_menu(module)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/red]")
        sys.exit(0)
