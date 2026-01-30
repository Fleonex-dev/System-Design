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
# ==========================================
# 🎓 COURSE CONFIGURATION
# ==========================================
COURSE = [
    {
        "id": "01",
        "title": "🐍 Python Essentials",
        "path": "01_python_essentials",
        "lessons": [
            {
                "title": "⚡ Concurrency Deep Dive (Sub-Module)",
                "type": "submodule",
                "path": "concurrency", # Relative to parent path
                "lessons": [
                    {"file": "00_intro_threading.py", "title": "0A. Threading Basics (Lifecycle)"},
                    {"file": "00_intro_multiprocessing.py", "title": "0B. Multiprocessing Basics (Isolation)"},
                    {"file": "00_intro_async.py", "title": "0C. Async Basics (Coroutines)"},
                    {"file": "01_threads_vs_processes.py", "title": "1. Threads vs Processes (The GIL)"},
                    {"file": "02_async_io.py", "title": "2. AsyncIO (Event Loop)"},
                    {"file": "03_race_conditions.py", "title": "3. Race Conditions (Async Locks)"},
                    {"file": "04_producer_consumer.py", "title": "4. Producer-Consumer (Queues)"},
                    {"file": "05_build_event_loop.py", "title": "5. Build an Event Loop (Internals)"},
                    {"file": "06_cpu_offloading.py", "title": "6. CPU Offloading (ProcessPool)"},
                    {"file": "07_structured_concurrency.py", "title": "7. Structured Concurrency (TaskGroup)"},
                ]
            },
            {
                "title": "🚦 Thread Safety (OS Threads)",
                "type": "submodule",
                "path": "thread_safety",
                "lessons": [
                    {"file": "01_race_condition_threading.py", "title": "Race Condition (Bytecode Proof)"},
                    {"file": "02_primitives.py", "title": "Primitives (Lock, RLock, Semaphore)"},
                    {"file": "03_deadlocks.py", "title": "Deadocks (Dining Philosophers)"},
                ]
            },
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
            {"file": "00_oop_primer.py", "title": "0. OOP Primer (Interfaces & Polymorphism)"},
            {
                "title": "📐 Design Patterns (Deep Dive)",
                "type": "submodule",
                "path": "design_patterns",
                "lessons": [
                    {"file": "01_adapter_facade.py", "title": "Adapter & Facade (Wrappers)"},
                    {"file": "02_composite_pattern.py", "title": "Composite (Trees)"},
                    {"file": "03_singleton_thread_safe.py", "title": "Singleton (Thread Safe)"},
                ]
            },
            {"file": "01_solid_agents.py", "title": "1. SOLID Principles"},
            {"file": "02_factory.py", "title": "2. Factory Pattern"},
            {"file": "03_strategy.py", "title": "3. Strategy Pattern"},
            {"file": "04_observer.py", "title": "4. Observer Pattern"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "03",
        "title": "☁️ High Level Design (HLD)",
        "path": "03_hld_concepts",
        "lessons": [
            {"file": "00_scaling_101.py", "title": "0. Scaling 101 (Vertical vs Horizontal)"},
            {
                "title": "💾 Distributed Data (Interviews)",
                "type": "submodule",
                "path": "distributed_data",
                "lessons": [
                    {"file": "01_replication_lag.py", "title": "Replication Lag (Consistency)"},
                    {"file": "03_cap_theorem.py", "title": "CAP Theorem Simulation"},
                    {"file": "04_distributed_locking.py", "title": "Distributed Locks (Redis)"},
                ]
            },
            {
                "title": "🔩 Database Internals",
                "type": "submodule",
                "path": "database_internals",
                "lessons": [
                    {"file": "01_acid_transactions.py", "title": "ACID (Atomicity & Isolation)"},
                ]
            },
            {"file": "01_llm_load_balancing.py", "title": "1. Load Balancing"},
            {"file": "02_semantic_caching.py", "title": "2. Semantic Caching"},
            {"file": "03_consistent_hashing.py", "title": "3. Consistent Hashing"},
            {"file": "04_distributed_id.py", "title": "4. Distributed IDs"},
            {"file": "challenge_solution.py", "title": "🏆 Capstone Challenge Solution"}
        ]
    },
    {
        "id": "04",
        "title": "🧠 Advanced AI Architecture",
        "path": "04_advanced_ai_arch",
        "lessons": [
            {"file": "00_what_is_a_vector.py", "title": "0A. What is a Vector? (Embeddings)"},
            {"file": "00_llm_mechanics.py", "title": "0B. LLM Mechanics (Probabilities)"},
            {
                "title": "✂️ RAG Deep Dive (Chunking/Vectors)",
                "type": "submodule",
                "path": "rag_deep_dive",
                "lessons": [
                    {"file": "01_chunking_strategies.py", "title": "Chunking Strategies"},
                    {"file": "02_vector_indexing.py", "title": "Vector Indexing (HNSW)"},
                ]
            },
            {
                "title": "📉 AI Optimization",
                "type": "submodule",
                "path": "optimization",
                "lessons": [
                    {"file": "01_quantization.py", "title": "Quantization (FP32->INT8)"},
                    {"file": "03_inference_optimization.py", "title": "Speculative Decoding (Moved)"},
                ]
            },
            {"file": "01_rag_pipeline_optimization.py", "title": "RAG Optimization"},
            {"file": "02_agent_orchestrator.py", "title": "Agent Orchestration"},
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
            {
                "title": "🧱 Common Components",
                "type": "submodule",
                "path": "common_components",
                "lessons": [
                    {"file": "01_notification_service.py", "title": "Notification System (Pub/Sub)"},
                    {"file": "02_distributed_scheduler.py", "title": "Distributed Scheduler (Cron)"},
                ]
            },
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
        # Use python from env
        env = os.environ.copy()
        subprocess.run([sys.executable, script_name], cwd=path, env=env)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    console.print("\n[dim]Execution Finished. Press Enter...[/dim]")
    input()

def view_code(path, script_name):
    full_path = os.path.join(path, script_name)
    if not os.path.exists(full_path):
        console.print(f"[red]File not found: {full_path}[/red]")
        return
        
    with open(full_path, "r") as f:
        code = f.read()
    
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    console.print("\n[dim]Press Enter to return...[/dim]")
    input()

def lesson_menu(base_path, lesson):
    while True:
        render_header()
        console.print(f"[bold green]Lesson:[/bold green] {lesson['title']}\n")
        
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
            run_script(base_path, lesson['file'])
        elif action == "📄 View Code":
            view_code(base_path, lesson['file'])

def submodule_menu(base_path, submodule):
    sub_path = os.path.join(base_path, submodule['path'])
    while True:
        render_header()
        console.print(f"[bold magenta]Sub-Module:[/bold magenta] {submodule['title']}\n")
        
        choices = [l['title'] for l in submodule['lessons']] + ["🔙 Back"]
        
        selection = questionary.select(
            "Select a Lesson:",
            choices=choices
        ).ask()
        
        if selection == "🔙 Back":
            break
            
        # Find lesson
        lesson = next(l for l in submodule['lessons'] if l['title'] == selection)
        lesson_menu(sub_path, lesson)

def module_menu(module):
    while True:
        render_header()
        console.print(f"[bold yellow]Module:[/bold yellow] {module['title']}\n")
        
        choices = ["📖 Read Teacher Guide (README)"] + \
                  [l['title'] for l in module['lessons']] + \
                  ["🔙 Back to Main Menu"]
                  
        selection = questionary.select(
            "Select a Topic:",
            choices=choices
        ).ask()
        
        if selection == "🔙 Back to Main Menu":
            break
        elif selection == "📖 Read Teacher Guide (README)":
            show_readme(module['path'])
        else:
            # Find lesson object
            item = next(l for l in module['lessons'] if l['title'] == selection)
            
            if item.get("type") == "submodule":
                submodule_menu(module['path'], item)
            else:
                lesson_menu(module['path'], item)


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
