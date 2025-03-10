from .rules import BusinessRule
from .exceptions import BusinessRuleException

class ValidateMixinRules :
    def validateRule(self, rule : BusinessRule) :
        if not rule.is_valid() :
            raise BusinessRuleException(rule)