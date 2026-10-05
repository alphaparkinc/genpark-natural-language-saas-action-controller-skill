"""Natural Language SaaS Action Controller.
100% Python Standard Library.
"""

class NaturalLanguageSaaSController:
    """Translates intent phrases into deterministic SaaS API schema payloads."""
    
    SUPPORTED_ACTIONS = {
        "invite_user": {"endpoint": "/v1/users/invite", "required": ["email", "role"]},
        "update_subscription": {"endpoint": "/v1/billing/subscription", "required": ["tier"]},
        "revoke_token": {"endpoint": "/v1/auth/tokens/revoke", "required": ["token_id"]},
        "export_audit_log": {"endpoint": "/v1/compliance/export", "required": ["time_range"]}
    }
    
    @classmethod
    def parse_intent(cls, intent_str: str, entities: dict) -> dict:
        intent_lower = intent_str.lower()
        matched_action = None
        
        if "invite" in intent_lower or "add user" in intent_lower:
            matched_action = "invite_user"
        elif "subscription" in intent_lower or "upgrade plan" in intent_lower:
            matched_action = "update_subscription"
        elif "revoke" in intent_lower or "delete key" in intent_lower:
            matched_action = "revoke_token"
        elif "audit" in intent_lower or "export log" in intent_lower:
            matched_action = "export_audit_log"
        else:
            return {"status": "UNSUPPORTED", "message": "No recognized deterministic SaaS intent"}
            
        schema = cls.SUPPORTED_ACTIONS[matched_action]
        missing = [f for f in schema["required"] if f not in entities]
        if missing:
            return {
                "status": "PARAM_DEFICIENCY",
                "action": matched_action,
                "missing_fields": missing,
                "prompt": f"Please provide missing parameter(s): {', '.join(missing)}"
            }
            
        return {
            "status": "READY_FOR_DISPATCH",
            "action": matched_action,
            "endpoint": schema["endpoint"],
            "payload": {k: entities[k] for k in schema["required"]}
        }
