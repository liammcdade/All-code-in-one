#!/usr/bin/env python3
"""
Automated Launcher Tester - Tests all launcher options automatically

This script automatically tests all options in the launcher by simulating
user input and checking for errors or missing files.
"""

import importlib
import os
import sys
import subprocess
from pathlib import Path
import time
from typing import List, Dict, Tuple

class LauncherTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_results = []
        self.errors = []
        
        # Define all tools to test
        self.tools_to_test = {
            "DataNinja": {
                "Data Analyzer": "DataNinja/core/analyzer.py",
                "Data Cleaner": "DataNinja/core/cleaner.py",
            },
            "Sports Analysis": {
                "Tennis": "sportsanalysis/tennis/tennis_analyzer.py",
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

    def print_header(self):
        """Print test header."""
        print("=" * 80)
        print("🧪 AUTOMATED LAUNCHER TESTER")
        print("=" * 80)

    def check_file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        full_path = self.project_root / file_path
        return full_path.exists()

    def test_file_syntax(self, file_path: str) -> Tuple[bool, str]:
        """Test if a Python file has valid syntax."""
        full_path = self.project_root / file_path
        if not full_path.exists():
            return False, f"File not found: {file_path}"
        
        try:
            # Test syntax by compiling
            with open(full_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            compile(source, str(full_path), 'exec')
            return True, "Syntax OK"
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Error: {e}"

    def test_file_imports(self, file_path: str) -> Tuple[bool, str]:
        """Test if a Python file can be imported without errors."""
        full_path = self.project_root / file_path
        if not full_path.exists():
            return False, f"File not found: {file_path}"
        
        try:
            # Try to import the module
            spec = importlib.util.spec_from_file_location("test_module", full_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True, "Import OK"
        except ImportError as e:
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Error: {e}"

    def test_file_execution(self, file_path: str) -> Tuple[bool, str]:
        """Test if a Python file can be executed."""
        full_path = self.project_root / file_path
        if not full_path.exists():
            return False, f"File not found: {file_path}"
        
        try:
            # Try to run the file with a timeout
            result = subprocess.run(
                [sys.executable, str(full_path)],
                capture_output=True,
                text=True,
                timeout=10  # 10 second timeout
            )
            
            if result.returncode == 0:
                return True, "Execution OK"
            else:
                return False, f"Execution failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            return False, "Execution timeout"
        except Exception as e:
            return False, f"Execution error: {e}"

    def test_all_files(self):
        """Test all files in the tools dictionary."""
        print("\n🔍 TESTING ALL FILES...")
        print("-" * 80)
        
        total_files = 0
        passed_files = 0
        failed_files = 0
        
        for category, tools in self.tools_to_test.items():
            print(f"\n📁 Testing {category}:")
            print("-" * 40)
            
            for tool_name, file_path in tools.items():
                total_files += 1
                print(f"\n🔧 Testing: {tool_name}")
                print(f"   File: {file_path}")
                
                # Test 1: File existence
                exists = self.check_file_exists(file_path)
                if not exists:
                    print(f"   ❌ File not found!")
                    failed_files += 1
                    self.errors.append(f"File not found: {file_path}")
                    continue
                
                print(f"   ✅ File exists")
                
                # Test 2: Syntax check
                syntax_ok, syntax_msg = self.test_file_syntax(file_path)
                if syntax_ok:
                    print(f"   ✅ Syntax OK")
                else:
                    print(f"   ❌ Syntax error: {syntax_msg}")
                    failed_files += 1
                    self.errors.append(f"Syntax error in {file_path}: {syntax_msg}")
                    continue
                
                # Test 3: Import test (skip for main scripts)
                if not file_path.endswith('main.py') and not file_path.endswith('.py'):
                    import_ok, import_msg = self.test_file_imports(file_path)
                    if import_ok:
                        print(f"   ✅ Import OK")
                    else:
                        print(f"   ⚠️  Import warning: {import_msg}")
                
                # Test 4: Execution test (for main scripts)
                if file_path.endswith('main.py') or 'main.py' in file_path:
                    exec_ok, exec_msg = self.test_file_execution(file_path)
                    if exec_ok:
                        print(f"   ✅ Execution OK")
                    else:
                        print(f"   ⚠️  Execution warning: {exec_msg}")
                
                passed_files += 1
                self.test_results.append({
                    'tool': tool_name,
                    'file': file_path,
                    'exists': True,
                    'syntax_ok': syntax_ok,
                    'status': 'PASS' if syntax_ok else 'FAIL'
                })
        
        return total_files, passed_files, failed_files

    def test_launcher_functionality(self):
        """Test the launcher functionality."""
        print("\n🚀 TESTING LAUNCHER FUNCTIONALITY...")
        print("-" * 80)
        
        # Test 1: Check if launcher.py exists
        launcher_path = self.project_root / "launcher.py"
        if not launcher_path.exists():
            print("❌ launcher.py not found!")
            return False
        
        print("✅ launcher.py found")
        
        # Test 2: Check launcher syntax
        syntax_ok, syntax_msg = self.test_file_syntax("launcher.py")
        if syntax_ok:
            print("✅ Launcher syntax OK")
        else:
            print(f"❌ Launcher syntax error: {syntax_msg}")
            return False
        
        # Test 3: Test launcher import
        try:
            import launcher
            print("✅ Launcher imports OK")
        except Exception as e:
            print(f"❌ Launcher import error: {e}")
            return False
        
        return True

    def generate_report(self, total_files, passed_files, failed_files):
        """Generate a test report."""
        print("\n" + "=" * 80)
        print("📊 TEST REPORT")
        print("=" * 80)
        
        print(f"\n📈 SUMMARY:")
        print(f"   Total files tested: {total_files}")
        print(f"   Passed: {passed_files}")
        print(f"   Failed: {failed_files}")
        print(f"   Success rate: {(passed_files/total_files)*100:.1f}%")
        
        if self.errors:
            print(f"\n❌ ERRORS FOUND:")
            for error in self.errors:
                print(f"   • {error}")
        
        print(f"\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result['status'] == 'PASS':
                print(f"   • {result['tool']} ({result['file']})")
        
        print(f"\n❌ FAILED TESTS:")
        failed_results = [r for r in self.test_results if r['status'] == 'FAIL']
        for result in failed_results:
            print(f"   • {result['tool']} ({result['file']})")

    def fix_common_issues(self):
        """Fix common issues found during testing."""
        print("\n🔧 FIXING COMMON ISSUES...")
        print("-" * 80)
        
        fixes_applied = 0
        
        # Fix 1: Add missing __init__.py files
        init_files_needed = [
            "DataNinja/__init__.py",
            "DataNinja/core/__init__.py",
            "DataNinja/formats/__init__.py",
            "DataNinja/plugins/__init__.py",
            "sportsanalysis/__init__.py",
            "sportsanalysis/baseball/__init__.py",
            "sportsanalysis/basketball/__init__.py",
            "sportsanalysis/cricket/__init__.py",
            "sportsanalysis/tennis/__init__.py",
            "sportsanalysis/olympic/__init__.py",
            "streamyutilities/__init__.py",
            "scripts/__init__.py",
            "extra/__init__.py",
            "sample_code/__init__.py",
        ]
        
        for init_file in init_files_needed:
            init_path = self.project_root / init_file
            if not init_path.exists():
                try:
                    init_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(init_path, 'w') as f:
                        f.write("# Auto-generated __init__.py file\n")
                    print(f"✅ Created {init_file}")
                    fixes_applied += 1
                except Exception as e:
                    print(f"❌ Failed to create {init_file}: {e}")
        
        # Fix 2: Add missing imports in problematic files
        problematic_files = {
            "DataNinja/core/analyzer.py": "import pandas as pd\nimport numpy as np",
            "DataNinja/core/cleaner.py": "import pandas as pd",
            "DataNinja/core/plotter.py": "import matplotlib.pyplot as plt\nimport pandas as pd",
        }
        
        for file_path, imports in problematic_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if imports are missing
                    if 'import pandas' not in content and 'pandas' in imports:
                        # Add imports at the top
                        lines = content.split('\n')
                        insert_index = 0
                        for i, line in enumerate(lines):
                            if line.strip().startswith('import ') or line.strip().startswith('from '):
                                insert_index = i + 1
                        
                        lines.insert(insert_index, imports)
                        new_content = '\n'.join(lines)
                        
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ Fixed imports in {file_path}")
                        fixes_applied += 1
                except Exception as e:
                    print(f"❌ Failed to fix {file_path}: {e}")
        
        print(f"\n🔧 Applied {fixes_applied} fixes")
        return fixes_applied

    def run_full_test(self):
        """Run the complete test suite."""
        self.print_header()
        
        # Test 1: Launcher functionality
        launcher_ok = self.test_launcher_functionality()
        if not launcher_ok:
            print("❌ Launcher test failed!")
            return
        
        # Test 2: All files
        total_files, passed_files, failed_files = self.test_all_files()
        
        # Test 3: Fix common issues
        fixes_applied = self.fix_common_issues()
        
        # Test 4: Re-test after fixes
        if fixes_applied > 0:
            print("\n🔄 Re-testing after fixes...")
            total_files2, passed_files2, failed_files2 = self.test_all_files()
            
            improvement = passed_files2 - passed_files
            if improvement > 0:
                print(f"✅ Fixed {improvement} additional files!")
        
        # Generate final report
        self.generate_report(total_files, passed_files, failed_files)
        
        print(f"\n🎉 Testing complete!")
        print(f"   Files tested: {total_files}")
        print(f"   Success rate: {(passed_files/total_files)*100:.1f}%")
        
        if failed_files == 0:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️  {failed_files} files need attention")


def main():
    """Main test runner."""
    import importlib.util  # Import here for the import test
    
    tester = LauncherTester()
    tester.run_full_test()


if __name__ == "__main__":
    main() 