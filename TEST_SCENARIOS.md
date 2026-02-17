# Customer Care System - Test Scenarios 🧪

This file contains comprehensive test scenarios to verify your multi-agent system works correctly.

---

## 📦 Scenario Category 1: Refunds & Returns

### Scenario 1.1: Simple Refund (Under $100)
**Customer Query:**
> "Hi, I bought a phone case last week but it doesn't fit my phone. I'd like a refund for order #ORD-789. My customer ID is 12345."

**Expected Outcome:**
- Intent: REFUND
- Sentiment: NEUTRAL
- Priority: MEDIUM
- Actions: Refund processed automatically ($85)
- Human approval: NOT required
- Status: RESOLVED

**What to Check:**
- ✅ Greeter correctly identifies REFUND intent
- ✅ Researcher finds refund policy
- ✅ Resolver processes refund without human intervention
- ✅ Quality reviewer approves
- ✅ Email sent to customer

---

### Scenario 1.2: High-Value Refund (Over $100) - Human Escalation
**Customer Query:**
> "I purchased a $1,500 laptop last week but it keeps crashing. I want a full refund immediately!"

**Expected Outcome:**
- Intent: REFUND
- Sentiment: NEGATIVE/URGENT
- Priority: HIGH
- Actions: Escalated for approval
- Human approval: REQUIRED
- Status: ESCALATED

**What to Check:**
- ✅ System recognizes amount > $100 threshold
- ✅ Escalation coordinator flags for human review
- ✅ System pauses and requests approval
- ✅ Clear escalation reason provided
- ✅ After approval, refund processes correctly

---

### Scenario 1.3: Defective Product Refund
**Customer Query:**
> "I received my order yesterday but the product is completely defective. The screen has lines through it and won't turn on properly. I'd like a full refund for order ORD-789."

**Expected Outcome:**
- Intent: REFUND
- Sentiment: NEGATIVE
- Priority: MEDIUM
- Actions: Refund + option for replacement offered
- Follow-up: Scheduled to confirm satisfaction

**What to Check:**
- ✅ Empathy agent acknowledges frustration
- ✅ Researcher checks warranty policy
- ✅ Tone adapter offers both refund AND replacement
- ✅ Quality reviewer ensures empathetic tone

---

## 🚚 Scenario Category 2: Shipping & Tracking

### Scenario 2.1: Track Package
**Customer Query:**
> "Where is my package? Order ORD-555 was supposed to be here by now and I'm getting worried."

**Expected Outcome:**
- Intent: TRACKING
- Sentiment: CONCERNED
- Priority: MEDIUM
- Actions: Tracking info provided, delivery estimate given

**What to Check:**
- ✅ Researcher uses track_shipment tool
- ✅ Current location and status provided
- ✅ Estimated delivery date communicated
- ✅ Tone is reassuring

---

### Scenario 2.2: Delayed Shipment
**Customer Query:**
> "My order was supposed to arrive 3 days ago but it's still stuck in transit. I need it for an event tomorrow!"

**Expected Outcome:**
- Intent: SHIPPING
- Sentiment: URGENT
- Priority: HIGH
- Actions: Carrier contacted, expedited delivery attempted
- Follow-up: Scheduled to confirm delivery

**What to Check:**
- ✅ Priority correctly classified as HIGH due to urgency
- ✅ Researcher investigates delay reason
- ✅ Resolver attempts to expedite
- ✅ Empathetic tone acknowledges time pressure

---

## 💳 Scenario Category 3: Billing & Account Issues

### Scenario 3.1: Duplicate Charge
**Customer Query:**
> "I was charged twice for the same order! My credit card shows two charges of $89.99. This is unacceptable!"

**Expected Outcome:**
- Intent: BILLING
- Sentiment: NEGATIVE/FRUSTRATED
- Priority: HIGH
- Actions: Explanation of temporary hold vs actual charge
- Follow-up: Confirm when hold drops

**What to Check:**
- ✅ Researcher explains temporary authorization holds
- ✅ Tone adapter acknowledges frustration
- ✅ Clear timeline provided (3-5 business days)
- ✅ Quality ensures accurate explanation

---

### Scenario 3.2: Password Reset Issue
**Customer Query:**
> "I can't log into my account. I tried resetting my password but I'm not receiving the email. I need to check my order status urgently."

**Expected Outcome:**
- Intent: ACCOUNT/PASSWORD
- Sentiment: FRUSTRATED
- Priority: MEDIUM
- Actions: Alternative reset method provided, account checked

**What to Check:**
- ✅ Researcher provides password reset instructions
- ✅ Alternative access methods offered
- ✅ Order status provided without login
- ✅ Follow-up to ensure access restored

---

## 🔄 Scenario Category 4: Exchanges & Product Issues

### Scenario 4.1: Wrong Item Received
**Customer Query:**
> "I ordered a medium blue shirt but received a large red one. I'd like to exchange it for the correct item please."

**Expected Outcome:**
- Intent: EXCHANGE
- Sentiment: NEUTRAL
- Priority: MEDIUM
- Actions: Exchange process initiated, return label sent

**What to Check:**
- ✅ Researcher finds exchange policy
- ✅ Free exchange offered (company error)
- ✅ Return label sent automatically
- ✅ Expedited shipping for correct item

---

## 🔥 Scenario Category 5: Complex Multi-Issue Queries

### Scenario 5.1: Shipping Delay + Billing Issue
**Customer Query:**
> "I am extremely frustrated! My package was supposed to arrive 3 days ago but tracking shows it's stuck in transit. On top of that, I was charged TWICE on my credit card for the same order - $89.99 twice! The party is tomorrow and I need this sorted NOW!"

**Expected Outcome:**
- Intent: SHIPPING + BILLING (multi-issue)
- Sentiment: URGENT/VERY FRUSTRATED
- Priority: CRITICAL
- Actions: Both issues addressed separately
- Compensation: Offered for poor experience

**What to Check:**
- ✅ Greeter identifies BOTH issues
- ✅ Researcher investigates BOTH problems
- ✅ Tone adapter addresses BOTH with high empathy
- ✅ Resolver tackles shipping AND billing
- ✅ Compensation offered (discount/gift card)
- ✅ Priority follow-up scheduled

---

### Scenario 5.2: Product Defect + Return Request + Account Issue
**Customer Query:**
> "This is ridiculous! The headphones I ordered are broken, I can't log into my account to track the return, and I've been waiting on hold with support for 30 minutes! Customer ID 12345."

**Expected Outcome:**
- Intent: REFUND + ACCOUNT + COMPLAINT (triple issue)
- Sentiment: EXTREMELY FRUSTRATED
- Priority: CRITICAL
- Actions: All three issues resolved, VIP treatment applied

**What to Check:**
- ✅ All three issues identified
- ✅ Premium customer status recognized
- ✅ Extra empathy applied
- ✅ Expedited processing
- ✅ Manager follow-up scheduled

---

## 👤 Scenario Category 6: VIP & Special Handling

### Scenario 6.1: Premium Customer Small Issue
**Customer Query:**
> "Hi, just wanted to check on my order status. Customer ID 12345."

**Expected Outcome:**
- Intent: TRACKING
- Sentiment: POSITIVE
- Priority: LOW
- Special handling: VIP customer recognized, extra courtesy shown

**What to Check:**
- ✅ Researcher identifies Premium tier
- ✅ Tone adapter adds VIP courtesy
- ✅ Proactive information offered
- ✅ Quality ensures premium treatment

---

## 🤖 Scenario Category 7: Edge Cases & Error Handling

### Scenario 7.1: Vague Query
**Customer Query:**
> "I have a problem with my order."

**Expected Outcome:**
- Intent: OTHER (clarification needed)
- Actions: Polite request for more details

**What to Check:**
- ✅ Greeter requests clarification politely
- ✅ Doesn't make assumptions
- ✅ Provides examples of what info is needed

---

### Scenario 7.2: No Customer ID Provided
**Customer Query:**
> "I need a refund for my broken item."

**Expected Outcome:**
- Intent: REFUND
- Actions: Request for order number or customer ID

**What to Check:**
- ✅ System politely requests identifying information
- ✅ Continues to be helpful without full data
- ✅ Provides general refund policy info

---

### Scenario 7.3: Unreasonable Request
**Customer Query:**
> "I bought this item 6 months ago and used it daily. Now it's worn out and I want a full refund!"

**Expected Outcome:**
- Intent: REFUND
- Actions: Politely explain 30-day policy, offer alternatives

**What to Check:**
- ✅ Researcher identifies out of policy window
- ✅ Tone adapter maintains empathy while setting boundaries
- ✅ Alternative solutions offered (warranty, discount on replacement)
- ✅ Quality ensures policy accurately explained

---

## 🎯 Testing Checklist

After running all scenarios, verify:

### Agent Performance
- [ ] Greeter correctly classifies all intents
- [ ] Researcher uses appropriate tools for each scenario
- [ ] Tone adapter adjusts empathy based on sentiment
- [ ] Resolver executes correct actions
- [ ] Quality reviewer catches any errors
- [ ] Escalation coordinator identifies high-risk situations
- [ ] Follow-up scheduler plans appropriate touchpoints

### System Functionality
- [ ] Shared state maintained across all scenarios
- [ ] Tools execute without errors
- [ ] Human approval triggers correctly (>$100 refunds)
- [ ] Quality scores are reasonable (7-10 range)
- [ ] Audit trail captures all interactions

### Output Quality
- [ ] Responses are empathetic and appropriate
- [ ] Policy information is accurate
- [ ] No hallucinated facts or numbers
- [ ] Tone matches customer sentiment
- [ ] All customer issues addressed

### Error Handling
- [ ] Graceful handling of missing information
- [ ] No crashes on edge cases
- [ ] Clear error messages if tools fail
- [ ] Appropriate fallbacks when info unavailable

---

## 📊 Automated Testing Script

To test all scenarios automatically, run:

```python
from customer_care_easy import CustomerCareCrew
import json

# Initialize system
api_key = "your-key-here"
system = CustomerCareCrew(api_key)

# Test scenarios
scenarios = [
    {"query": "Refund for defective product ORD-789", "customer_id": "12345"},
    {"query": "$1,500 laptop refund needed", "customer_id": "67890"},
    # ... add more
]

results = []
for scenario in scenarios:
    result = system.handle_customer_query(
        scenario["query"], 
        scenario.get("customer_id")
    )
    results.append({
        "query": scenario["query"],
        "status": result["status"],
        "actions": len(result.get("actions_taken", [])),
        "escalated": result.get("requires_human", False)
    })

# Print summary
for r in results:
    print(f"Query: {r['query']}")
    print(f"  Status: {r['status']}")
    print(f"  Actions: {r['actions']}")
    print(f"  Escalated: {r['escalated']}\n")
```

---

## 💡 Tips for Testing

1. **Test incrementally**: Start with simple scenarios, then add complexity
2. **Check the logs**: Enable verbose=True to see agent reasoning
3. **Verify shared state**: Ensure context flows between agents
4. **Test human approval**: Confirm the system actually pauses and waits
5. **Quality scores**: Track if they're consistently reasonable (8-10 is good)
6. **Cost tracking**: Monitor API usage to estimate real-world costs
7. **Compare outputs**: Run same query multiple times, check consistency

---

## 🎓 For Your Assignment

Test at least:
- ✅ 1 simple scenario (shows basic flow)
- ✅ 1 human escalation scenario (shows human-in-the-loop)
- ✅ 1 complex multi-issue scenario (shows coordination)

Include screenshots/transcripts of all three in your submission!
