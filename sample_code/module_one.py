# This is a module-level comment for module_one
class Greeter:
    """
    A simple class to greet people.
    It stores a greeting message.
    """
    # Class variable comment
    default_greeting = "Hello"

    def __init__(self, name):
        # Comment for __init__
        self.name = name  # Inline comment for name

    def greet(self, loud=False):
        """Greets the person."""
        message = f"{self.default_greeting}, {self.name}!"
        if loud:
            message = message.upper()
        print(message)
        return message

# A standalone function
def utility_function():
    """A simple utility function."""
    # Comment inside utility_function
    print("Utility function called.")
    return True

another_var = 100
