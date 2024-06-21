"""I/O module for the program."""


def validate(input):
    """Validates input for positive integers."""
    if not isinstance(input, int):
        raise TypeError("Input must be an integer.")
    if input < 1:
        raise ValueError("Input should be greater than zero.")
    return input


def output_stdout(output):
    """Outputs to stdout."""
    if not isinstance(output, dict):
        raise TypeError("Output must be a dictionary.")
    if "name" not in output:
        raise KeyError("Name not found.")
    print(output["name"])
