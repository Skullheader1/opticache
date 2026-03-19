import sys

import questionary

if not sys.stdout.isatty():
    print(f"Please run this script in a terminal to use the interactive prompts.")
    print("Otherwise you can run the tests directly by running the individual test files (fifo.py, lru.py, lfu.py) and calling the run_test function with the desired parameters.")
    print("Example: `python fifo.py 10 100000` to run the FIFO test with 10 iterations and a load of 100000 items.")
    print("Exiting...")
    sys.exit(1)

optimization = questionary.select(
    "What optimization test do you want to run?",
    choices=[
        "FIFO (First In First Out)",
        "LRU (Least Recently Used)",
        "LFU (Least Frequently Used)",
    ]).ask()

iterations = questionary.select(
    "How many iterations do you want to run? Please note that more iterations will give more accurate results but will take much longer to run.",
    choices=[
        "1",
        "5",
        "10",
        "25",
        "50",
        "100",
        "250",
    ]).ask()

load = questionary.select(
    "How many items do you want to load into the cache? Please note that more items will give more accurate results but will take exponentially longer to run.",
    choices=[
        "1000",
        "5000",
        "10000",
        "50000",
        "100000",
        "500000",
        "1000000",
    ]).ask()

iterations = int(iterations)
load = int(load)

if optimization.startswith("FIFO"):
    from fifo import run_test
    print("Running FIFO test...")
    run_test(iterations, load)
elif optimization.startswith("LRU"):
    from lru import run_test
    print("Running LRU test...")
    run_test(iterations, load)
elif optimization.startswith("LFU"):
    from lfu import run_test
    print("Running LFU test...")
    run_test(iterations, load)