#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from instagram.crew import Instagram

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
        'current_date': datetime.now().strftime("%Y-%m-%d"),
        'instagram_description': input('Enter the page description here: '),
        'topic_of_the_week': input('Enter the topic of the week here: '),
    }

    crew_instance = Instagram().crew()
    output = crew_instance.kickoff(inputs=inputs)

    # ✅ Debugging: Print output to check if it's generating correctly
    print("\n--- OUTPUT DEBUG ---")
    print(output)
    print("---------------------\n")

if __name__ == "__main__":
    run()
