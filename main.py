from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = "kb/laptop_rules.json"

def collect_initial_facts():

    facts = []

    budget = input("What is your budget? (low/medium/high): ").strip().lower()

    while budget not in ["low", "medium", "high"]:
        budget = input("Please enter low, medium, or high: ").strip().lower()

    facts.append("budget_" + budget)

    questions = {
        "portable": "Is portability important?",
        "long_battery": "Do you need long battery life?",
        "gaming": "Will you use the laptop for gaming?",
        "creative_work": "Will you do creative work?",
        "office_only": "Will you mainly use office applications?",
        "needs_ai_accel": "Do you need AI acceleration?",
        "large_screen": "Do you prefer a large screen?",
        "travel_often": "Do you travel often?"
    }

    for fact, question in questions.items():
        answer = input(question + " (y/n): ").strip().lower()

        if answer.startswith("y"):
            facts.append(fact)

    os_choice = input(
        "Preferred OS? (windows/macos/linux): "
    ).strip().lower()

    if os_choice in ["windows", "macos", "linux"]:
        facts.append("pref_os_" + os_choice)

    return facts

def main():
    rules = load_rules(KB_PATH)

    engine = ForwardChainingEngine(rules)

    facts = collect_initial_facts()

    engine.assert_facts(facts)

    
    engine.run()

    results = engine.conclusions()

    print("\n=== Laptop Advisor Results ===")

    print("\nRecommendations:")
    if results["recommendations"]:
        for recommendation in results["recommendations"]:
            print("-", recommendation)
    else:
        print("No specific laptop recommendation found.")

    print("\nSuggested Specifications:")
    if results["specs"]:
        for spec in results["specs"]:
            print("-", spec)
    else:
        print("No additional specifications found.")

    print("\nRules Fired:")
    for step in engine.trace:
        print("-", step["rule"], "->", step["consequent"])

if __name__ == "__main__":
    main()
