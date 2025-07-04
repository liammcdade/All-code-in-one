from module_one import Greeter, utility_function

# Using the Greeter class
my_greeter = Greeter("Alice")
my_greeter.greet()

# Using the utility function
if utility_function():
    print("Utility worked!")

# A variable that might be confused with another_var
another_variable = 200

def use_greeter_again(name, polite=False):
    """Uses Greeter again, possibly politely."""
    g = Greeter(name)
    if polite:
        g.default_greeting = "Good day"
    g.greet()
