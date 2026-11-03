from dataclasses import dataclass
from typing import List, Set, Dict, Any

@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""

class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Store initial facts into the working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """Return True if all antecedents are true and consequent not yet known."""
        return(
            all(fact in self.facts for fact in rule.antecedents)
            and rule.consequent not in self.facts
        )

    def run(self) -> None:
        """Run the forward chaining inference engine."""
        while True:
           available_rules = [
            rule for rule in self.rules
            if self.can_fire(rule)
           ]
           if not available_rules:
               break
           rule = max(available_rules, key=lambda r: r.priority)

           self.facts.add(rule.consequent)

           self.trace.append({
               "rule": rule.name,
                      "consequent": rule.consequent
           })

    def conclusions(self) -> Dict[str, List[str]]:
        """Separate recommendations, specs, and other facts."""
        
        return{
        "recommendations": sorted(
            fact for fact in self.facts
            if fact.startswith("recommend:")
        ),
        "specs": sorted(
            fact for fact in self.facts
            if fact.startswith("spec:")
        ),
        "other_facts": sorted(
            fact for fact in self.facts
            if not fact.startswith(("recommend:", "spec:"))
        )
    }
