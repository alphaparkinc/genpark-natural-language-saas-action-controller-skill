"""Example usage for Natural Language SaaS Action Controller."""
from client import NaturalLanguageSaaSController

if __name__ == "__main__":
    res = NaturalLanguageSaaSController.parse_intent(
        "Please upgrade the team subscription plan",
        {"tier": "enterprise_plus"}
    )
    print("Dispatch Status:", res["status"])
    print("Target Endpoint:", res["endpoint"])
    print("Payload:", res["payload"])
