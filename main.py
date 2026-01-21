import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import track
from git import Repo
from diamond_agent import RefactorAgent

console = Console()

def scan_repositories():
    console.print("[bold blue]Starting DiamondCLI...[/bold blue]")
    agent = RefactorAgent()
    # Look for folders in ../ (parent dir)
    parent_dir = Path("..")
    
    # Identify git repositories
    repos = []
    if parent_dir.exists():
        for d in parent_dir.iterdir():
            if d.is_dir() and (d / ".git").exists():
                repos.append(d)
    
    console.print(f"[green]Found {len(repos)} repositories.[/green]")

    for repo_path in repos:
        console.print(f"\n[bold magenta]Scanning repository: {repo_path.name}[/bold magenta]")
        
        try:
            repo = Repo(repo_path)
            
            # Check if dirty, maybe skip or proceed with caution. 
            # Prompt doesn't specify handling dirty state, but let's be safe-ish?
            # Instructions: "Check out a new branch diamond-auto"
            
            # Save current branch to return later
            original_branch = repo.active_branch
            branch_name = "diamond-auto"
            
            # Checkout new branch 'diamond-auto'
            # If it exists, checkout it. If not, create it.
            if branch_name in repo.heads:
                repo.heads[branch_name].checkout()
            else:
                repo.create_head(branch_name).checkout()
            
            console.print(f"Checked out branch: {branch_name}")

            files_changed = False

            # Propagate CI/CD Workflow
            workflow_src = Path(".github/workflows/diamond_guard.yml")
            if workflow_src.exists():
                workflow_dest_dir = repo_path / ".github" / "workflows"
                workflow_dest_dir.mkdir(parents=True, exist_ok=True)
                workflow_dest = workflow_dest_dir / "diamond_guard.yml"
                workflow_content = workflow_src.read_text(encoding="utf-8")
                
                # Check if file needs update
                if not workflow_dest.exists() or workflow_dest.read_text(encoding="utf-8") != workflow_content:
                    workflow_dest.write_text(workflow_content, encoding="utf-8")
                    repo.index.add([str(workflow_dest.absolute())])
                    files_changed = True
                    console.print("[cyan]Propagated CI/CD workflow.[/cyan]")

            # Collect source files
            files_to_refactor = []
            extensions = [".ts", ".tsx", ".py"]
            
            for ext in extensions:
                # rglob for recursive search
                files_to_refactor.extend(repo_path.rglob(f"*{ext}"))
            
            # Filter out ignored dirs like node_modules, venv, .git
            # (Simple heuristic)
            filtered_files = []
            for f in files_to_refactor:
                parts = f.parts
                if "node_modules" in parts or "venv" in parts or ".git" in parts or "__pycache__" in parts:
                    continue
                filtered_files.append(f)
            
            if not filtered_files:
                console.print("No source files found to refactor.")
                repo.heads[original_branch.name].checkout()
                continue

            # files_changed already initialized
            
            # Loop through source files
            for file_path in track(filtered_files, description=f"Refactoring {repo_path.name}"):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    language = file_path.suffix[1:] # py, ts, etc.
                    
                    # Call RefactorAgent
                    new_code = agent.refactor_code(content, language)
                    
                    # Overwrite file if changed
                    if new_code.strip() != content.strip():
                        file_path.write_text(new_code, encoding="utf-8")
                        # Git add
                        repo.index.add([str(file_path.absolute())])
                        files_changed = True
                except Exception as e:
                    console.print(f"[red]Error processing {file_path.name}: {e}[/red]")

            # Git commit & Push
            if files_changed:
                repo.index.commit("Diamond Standard Refactor")
                console.print("[green]Committed changes.[/green]")
                
                # Push
                try:
                    # set_upstream=True equivalent
                    origin = repo.remote(name='origin')
                    origin.push(branch_name, set_upstream=True)
                    console.print("[green]Pushed to origin.[/green]")
                    
                    # Create PR
                    # Using gh cli via subprocess
                    console.print("Creating PR...")
                    pr_cmd = [
                        "gh", "pr", "create",
                        "--title", "Diamond Standard Refactor",
                        "--body", "Automated refactor applied by DiamondCLI.",
                        "--head", branch_name,
                        "--base", original_branch.name
                    ]
                    result = subprocess.run(pr_cmd, cwd=str(repo_path), capture_output=True, text=True)
                    if result.returncode == 0:
                        console.print(f"[bold green]PR Created: {result.stdout.strip()}[/bold green]")
                    else:
                        console.print(f"[red]PR Creation Failed: {result.stderr.strip()}[/red]")

                except Exception as push_error:
                    console.print(f"[red]Push failed: {push_error}[/red]")
            else:
                console.print("No changes were made.")

            # Return to original branch (optional, but good practice)
            # repo.heads[original_branch.name].checkout()

        except Exception as e:
            console.print(f"[red]Error handling repo {repo_path.name}: {e}[/red]")

if __name__ == "__main__":
    scan_repositories()
