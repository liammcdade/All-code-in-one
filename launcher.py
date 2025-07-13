#!/usr/bin/env python3
"""
Simple Launcher - Access all your tools and files from one place

This launcher provides easy access to all your tools, scripts, and analysis modules.
Just run this file and navigate through the menus to access any tool in your codebase.
"""

import os
import sys
import subprocess
from pathlib import Path
import time

class SimpleLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.running = True
        
        # Define all tools organized by category
        self.tools = {
            "DataNinja": {
                "DataNinja CLI": "python -m DataNinja",
                "Data Analyzer": "DataNinja/core/analyzer.py",
                "Data Cleaner": "DataNinja/core/cleaner.py",
                "Data Plotter": "DataNinja/core/plotter.py",
            },
            "Sports Analysis": {
                "Baseball": "sportsanalysis/baseball/baseball_analyzer.py",
                "Basketball": "sportsanalysis/basketball/basketball_analyzer.py",
                "Cricket": "sportsanalysis/cricket/cricket_analyzer.py",
                "Tennis": "sportsanalysis/tennis/tennis_analyzer.py",
                "Olympic": "sportsanalysis/olympic/olympic_analyzer.py",
                "Chess": "sportsanalysis/chess/main.py",
                "Snake AI": "sportsanalysis/snakeAI/main.py",
                "Tic-Tac-Toe": "sportsanalysis/TIK-TAK-TOES/main.py",
                "Premier League": "sportsanalysis/premier-league/25-26-season.py",
                "World Cup 2026": "sportsanalysis/worldcup26/main.py",
                "Women's Euros": "sportsanalysis/womens euros/main.py",
                "F1": "sportsanalysis/F1/Main.py",
                "NFL": "sportsanalysis/NFL/Main.py",
                "Playoffs": "sportsanalysis/playoffs/run-all.py",
            },
            "System Tools": {
                "All PC Tools": "streamyutilities/pc tools/pc_tools_combined.py",
                "Directory Analyzer": "streamyutilities/pc tools/analyze_directory_sizes.py",
                "File Renamer": "streamyutilities/pc tools/batch_rename_files.py",
                "Connectivity Check": "streamyutilities/pc tools/check_connectivity.py",
                "Cleanup Tool": "streamyutilities/pc tools/cleanup_temp_files.py",
                "Duplicate Finder": "streamyutilities/pc tools/find_duplicate_files.py",
                "Password Generator": "streamyutilities/pc tools/generate_password.py",
                "Image Resizer": "streamyutilities/pc tools/resize_images.py",
                "File Search": "streamyutilities/pc tools/search_in_files.py",
                "System Info": "streamyutilities/pc tools/system_info.py",
            },
            "Scripts": {
                "Check Dependencies": "scripts/checkdeps.py",
                "Generate Docs": "scripts/gendocs.py",
                "Plugin Loader": "scripts/plugin_loader.py",
            },
            "Science & Space": {
                "Exoplanet Analysis": "space/exoplanet/exoplanet-fill-in.py",
            },
            "Extra Tools": {
                "Emissions Analysis": "extra/analyze_emissions.py",
                "Cipher Solver": "extra/cphersolve.py",
                "Dev CLI": "extra/dev_cli.py",
                "File Monitor": "extra/monitor_all_files.py",
            },
            "Development": {
                "Sample Module 1": "sample_code/module_one.py",
                "Sample Module 2": "sample_code/module_two.py",
            }
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("🚀 SIMPLE LAUNCHER - All Your Tools in One Place")
        print("=" * 60)

    def print_menu(self, title, options):
        """Print a formatted menu."""
        print(f"\n📁 {title}")
        print("-" * 40)
        
        for i, (name, path) in enumerate(options.items(), 1):
            # Check if file exists and show status
            if path.startswith("python -m"):
                print(f"{i:2d}. {name}")
            else:
                full_path = self.project_root / path
                if full_path.exists():
                    print(f"{i:2d}. {name} ✅")
                else:
                    print(f"{i:2d}. {name} ❌")
        
        print(f"\n 0. Back to Main Menu")
        print(" q. Quit")

    def run_tool(self, tool_path):
        """Run a tool or script."""
        if tool_path.startswith("python -m"):
            # CLI command
            try:
                print(f"Running: {tool_path}")
                subprocess.run(tool_path.split(), check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
                return False
        else:
            # Python file
            full_path = self.project_root / tool_path
            if not full_path.exists():
                print(f"Error: File not found - {tool_path}")
                return False
            
            try:
                print(f"Running: {tool_path}")
                subprocess.run([sys.executable, str(full_path)], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error running {tool_path}: {e}")
                return False

    def show_category(self, category_name):
        """Show tools in a specific category."""
        tools = self.tools[category_name]
        
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu(category_name, tools)
            
            choice = input("\nSelect a tool (or 0/q): ").strip().lower()
            
            if choice == '0':
                break
            elif choice == 'q':
                self.running = False
                break
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(tools):
                    tool_names = list(tools.keys())
                    tool_name = tool_names[choice_num - 1]
                    tool_path = tools[tool_name]
                    
                    print(f"\n🚀 Running: {tool_name}")
                    success = self.run_tool(tool_path)
                    
                    if success:
                        print("✅ Tool completed successfully!")
                    else:
                        print("❌ Tool failed to run.")
                    
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid choice!")
                    time.sleep(1)
            else:
                print("❌ Invalid choice!")
                time.sleep(1)

    def show_quick_access(self):
        """Show quick access to popular tools."""
        quick_tools = {
            "DataNinja CLI": "python -m DataNinja",
            "Check Dependencies": "scripts/checkdeps.py",
            "All PC Tools": "streamyutilities/pc tools/pc_tools_combined.py",
            "Tennis Analyzer": "sportsanalysis/tennis/tennis_analyzer.py",
            "World Cup 2026": "sportsanalysis/worldcup26/main.py",
            "Emissions Analysis": "extra/analyze_emissions.py",
        }
        
        print("\n⚡ QUICK ACCESS - Popular Tools")
        print("-" * 40)
        
        for i, (name, path) in enumerate(quick_tools.items(), 1):
            if path.startswith("python -m"):
                print(f"{i:2d}. {name}")
            else:
                full_path = self.project_root / path
                if full_path.exists():
                    print(f"{i:2d}. {name} ✅")
                else:
                    print(f"{i:2d}. {name} ❌")
        
        print(f"\n 0. Back to Main Menu")
        print(" q. Quit")
        
        choice = input("\nSelect a tool: ").strip().lower()
        
        if choice == '0':
            return
        elif choice == 'q':
            self.running = False
            return
        elif choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(quick_tools):
                tool_names = list(quick_tools.keys())
                tool_name = tool_names[choice_num - 1]
                tool_path = quick_tools[tool_name]
                
                print(f"\n🚀 Running: {tool_name}")
                success = self.run_tool(tool_path)
                
                if success:
                    print("✅ Tool completed successfully!")
                else:
                    print("❌ Tool failed to run.")
                
                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice!")
                time.sleep(1)
        else:
            print("❌ Invalid choice!")
            time.sleep(1)

    def search_tools(self):
        """Search for tools by name."""
        search_term = input("\n🔍 Enter search term: ").strip().lower()
        
        if not search_term:
            return
        
        results = []
        
        # Search through all tools
        for category_name, tools in self.tools.items():
            for tool_name, tool_path in tools.items():
                if search_term in tool_name.lower() or search_term in category_name.lower():
                    results.append((category_name, tool_name, tool_path))
        
        if results:
            print(f"\n📋 Found {len(results)} results:")
            for i, (category, name, path) in enumerate(results, 1):
                if path.startswith("python -m"):
                    print(f"{i:2d}. {name} ({category})")
                else:
                    full_path = self.project_root / path
                    if full_path.exists():
                        print(f"{i:2d}. {name} ({category}) ✅")
                    else:
                        print(f"{i:2d}. {name} ({category}) ❌")
            
            choice = input("\nSelect result to run (or 0 to cancel): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(results):
                    category, name, path = results[choice_num - 1]
                    print(f"\n🚀 Running: {name}")
                    success = self.run_tool(path)
                    
                    if success:
                        print("✅ Tool completed successfully!")
                    else:
                        print("❌ Tool failed to run.")
                    
                    input("\nPress Enter to continue...")
                elif choice_num == 0:
                    return
                else:
                    print("❌ Invalid choice!")
                    time.sleep(1)
            else:
                print("❌ Invalid choice!")
                time.sleep(1)
        else:
            print(f"\n❌ No results found for '{search_term}'")
            time.sleep(2)

    def show_statistics(self):
        """Show project statistics."""
        total_tools = sum(len(tools) for tools in self.tools.values())
        total_categories = len(self.tools)
        
        # Count existing files
        existing_files = 0
        missing_files = 0
        
        for category, tools in self.tools.items():
            for tool_name, tool_path in tools.items():
                if not tool_path.startswith("python -m"):
                    full_path = self.project_root / tool_path
                    if full_path.exists():
                        existing_files += 1
                    else:
                        missing_files += 1
        
        print("\n📊 PROJECT STATISTICS")
        print("-" * 40)
        print(f"Categories: {total_categories}")
        print(f"Total Tools: {total_tools}")
        print(f"Existing Files: {existing_files}")
        print(f"Missing Files: {missing_files}")
        print(f"Success Rate: {(existing_files/total_tools)*100:.1f}%")
        print(f"Project Root: {self.project_root}")
        
        # Count Python files
        python_files = list(self.project_root.rglob("*.py"))
        print(f"Python Files: {len(python_files)}")
        
        print(f"\n📁 Tools by Category:")
        for category, tools in self.tools.items():
            existing = sum(1 for path in tools.values() 
                         if path.startswith("python -m") or (self.project_root / path).exists())
            print(f"  {category}: {len(tools)} tools ({existing} available)")
        
        input("\nPress Enter to continue...")

    def run(self):
        """Main run method."""
        try:
            while self.running:
                self.clear_screen()
                self.print_header()
                
                print("\n📋 MAIN MENU")
                print("-" * 40)
                
                # Show categories
                for i, category in enumerate(self.tools.keys(), 1):
                    tools = self.tools[category]
                    existing = sum(1 for path in tools.values() 
                                 if path.startswith("python -m") or (self.project_root / path).exists())
                    print(f"{i:2d}. {category} ({existing}/{len(tools)} tools)")
                
                print(f"\n⚡ Quick Access")
                print("🔍 Search Tools")
                print("📊 Statistics")
                print(" q. Quit")
                
                choice = input("\nSelect option: ").strip().lower()
                
                if choice == 'q':
                    self.running = False
                elif choice == 'quick access':
                    self.show_quick_access()
                elif choice == 'search tools':
                    self.search_tools()
                elif choice == 'statistics':
                    self.show_statistics()
                elif choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(self.tools):
                        category_name = list(self.tools.keys())[choice_num - 1]
                        self.show_category(category_name)
                    else:
                        print("❌ Invalid choice!")
                        time.sleep(1)
                else:
                    print("❌ Invalid choice!")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n👋 Launcher interrupted by user.")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            print("\n👋 Thank you for using Simple Launcher!")


def main():
    """Main entry point."""
    launcher = SimpleLauncher()
    launcher.run()


if __name__ == "__main__":
    main() 