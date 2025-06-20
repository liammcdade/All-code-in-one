```python
import sys
from DataNinja.cli import main as cli_main

if __name__ == "__main__":
    """
    Main entry point for running DataNinja as a module.

    This script is executed when you run: python -m DataNinja <args>
    It simply calls the main function from the cli.py module,
    passing along any command-line arguments.
    """
    # sys.argv[0] will be the path to __main__.py
    # cli_main expects arguments starting from the script name,
    # but argparse handles sys.argv directly, so we can just call it.
    # If cli_main was expecting only the arguments *after* the script name,
    # we would pass sys.argv[1:]. However, argparse's parse_args()
    # by default uses sys.argv[1:] if no args are passed to it.
    # So, calling cli_main() without arguments is correct here, as it will
    # pick up sys.argv internally.
    cli_main()
```
