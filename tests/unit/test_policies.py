from decimal import Decimal
from safeopsbench.core.policies import Decision,authorize,credit_policy,discount_policy,hold_policy,inventory_policy
def test_credit_requires_approval():assert credit_policy(Decimal("18750"),Decimal("4600"),Decimal("20000")).decision is Decision.REQUIRE_APPROVAL
def test_hold_denies():assert hold_policy(True).decision is Decision.DENY
def test_inventory_authoritative():assert inventory_policy(5,10).decision is Decision.DENY
def test_discount_threshold():assert discount_policy("sales_rep",Decimal("25")).decision is Decision.REQUIRE_APPROVAL
def test_permission_denied():assert authorize("sales_rep","invoice.create").decision is Decision.DENY
