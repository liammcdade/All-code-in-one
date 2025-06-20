def to_uppercase(input_text):
  """Converts the input text to uppercase.

  Args:
    input_text: The string to be converted.

  Returns:
    The uppercase version of the input string.
  """
  return input_text.upper()

def to_lowercase(input_text):
  """Converts the input text to lowercase.

  Args:
    input_text: The string to be converted.

  Returns:
    The lowercase version of the input string.
  """
  return input_text.lower()

def to_titlecase(input_text):
  """Converts the input text to title case.

  Args:
    input_text: The string to be converted.

  Returns:
    The title case version of the input string.
  """
  return input_text.title()

if __name__ == "__main__":
  text = input("Enter text: ")

  print("Choose conversion:")
  print("1. Uppercase")
  print("2. Lowercase")
  print("3. Title Case")

  choice = input("Enter choice (1-3): ")

  if choice == '1':
    result = to_uppercase(text)
    print(f"Result: {result}")
  elif choice == '2':
    result = to_lowercase(text)
    print(f"Result: {result}")
  elif choice == '3':
    result = to_titlecase(text)
    print(f"Result: {result}")
  else:
    print("Invalid choice.")
