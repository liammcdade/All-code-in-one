#!/usr/bin/env python3
"""
Comprehensive Code Tester - Tests every Python file in the project

This script automatically discovers and tests all Python files in the project,
checking for syntax errors, import issues, missing dependencies, and more.
"""

import ast
import importlib
import importlib.util
import os
import sys
import subprocess
import traceback
from pathlib import Path
import time
from typing import List, Dict, Tuple, Set
import json

        # ...existing code...
class LauncherTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_results = []
        self.errors = []
        self.all_python_files = []

    def discover_python_files(self):
        """Discover all Python files in the project recursively."""
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden and cache dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for f in files:
                if f.endswith('.py') and not f.startswith('.'):
                    python_files.append(os.path.join(root, f))
        self.all_python_files = sorted(python_files)
        return self.all_python_files

    def test_all_files(self):
        """Test all discovered Python files."""
        print("\n🔍 TESTING ALL PYTHON FILES IN CODEBASE...")
        print("-" * 80)
        total_files = 0
        passed_files = 0
        failed_files = 0
        self.discover_python_files()
        for file_path in self.all_python_files:
            total_files += 1
            rel_path = os.path.relpath(file_path, self.project_root)
            print(f"\n🔧 Testing: {rel_path}")
            # Test 1: File existence
            exists = os.path.exists(file_path)
            if not exists:
                print(f"   ❌ File not found!")
                failed_files += 1
                self.errors.append(f"File not found: {rel_path}")
                continue
            print(f"   ✅ File exists")
            # Test 2: Syntax check
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, file_path, 'exec')
                print(f"   ✅ Syntax OK")
                syntax_ok = True
            except SyntaxError as e:
                print(f"   ❌ Syntax error: {e}")
                failed_files += 1
                self.errors.append(f"Syntax error in {rel_path}: {e}")
                syntax_ok = False
                continue
            except Exception as e:
                print(f"   ❌ Error: {e}")
                failed_files += 1
                self.errors.append(f"Error in {rel_path}: {e}")
                syntax_ok = False
                continue
            # Test 3: Import test (skip for __main__ scripts)
            if not rel_path.endswith('main.py'):
                try:
                    spec = importlib.util.spec_from_file_location("test_module", file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"   ✅ Import OK")
                except ImportError as e:
                    print(f"   ⚠️  Import error: {e}")
                    self.errors.append(f"Import error in {rel_path}: {e}")
                except Exception as e:
                    print(f"   ⚠️  Import error: {e}")
                    self.errors.append(f"Import error in {rel_path}: {e}")
            # Test 4: Execution test (for main scripts)
            if rel_path.endswith('main.py'):
                try:
                    result = subprocess.run(
                        [sys.executable, file_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        print(f"   ✅ Execution OK")
                    else:
                        print(f"   ⚠️  Execution failed: {result.stderr}")
                        self.errors.append(f"Execution failed in {rel_path}: {result.stderr}")
                except subprocess.TimeoutExpired:
                    print(f"   ⚠️  Execution timeout")
                    self.errors.append(f"Execution timeout in {rel_path}")
                except Exception as e:
                    print(f"   ⚠️  Execution error: {e}")
                    self.errors.append(f"Execution error in {rel_path}: {e}")
            passed_files += 1 if syntax_ok else 0
            self.test_results.append({
                'file': rel_path,
                'exists': exists,
                'syntax_ok': syntax_ok,
                'status': 'PASS' if syntax_ok else 'FAIL'
            })
        return total_files, passed_files, failed_files
        # ...existing code...
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

    # ...existing code...

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
    import importlib.util
    tester = LauncherTester()
    print("=" * 80)
    print("🧪 COMPREHENSIVE CODEBASE TESTER")
    print("=" * 80)
    total_files, passed_files, failed_files = tester.test_all_files()
    print("\n" + "=" * 80)
    print("📊 TEST REPORT")
    print("=" * 80)
    print(f"\n📈 SUMMARY:")
    print(f"   Total files tested: {total_files}")
    print(f"   Passed: {passed_files}")
    print(f"   Failed: {failed_files}")
    print(f"   Success rate: {(passed_files/total_files)*100:.1f}%")
    if tester.errors:
        print(f"\n❌ ERRORS FOUND:")
        for error in tester.errors:
            print(f"   • {error}")
    else:
        print("\n✅ No errors found. All files passed!")

if __name__ == "__main__":
    main()