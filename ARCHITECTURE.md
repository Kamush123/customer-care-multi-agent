# System Architecture Diagram

## High-Level Architecture

```
                                USER
                                  │
                                  │ Customer Query
                                  ▼
                    ┌─────────────────────────┐
                    │   CUSTOMER CARE CREW    │
                    │    (Orchestrator)       │
                    └─────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    │    Shared Memory/State    │
                    │  (CustomerCareState obj)  │
                    │                           │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        │      Sequential Task Execution Flow               │
        │                                                   │
        ▼                         ▼                         ▼


┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   AGENT 1:       │    │   AGENT 2:       │    │   AGENT 3:       │
│   Greeter &      │───▶│   Knowledge      │───▶│   Empathy &      │
│   Intent         │    │   Researcher     │    │   Tone Adapter   │
│   Classifier     │    │                  │    │                  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                                 ▼
                  ┌────────────────────────────┐
                  │   Shared State Updated     │
                  │   • Intent classified      │
                  │   • Research findings      │
                  │   • Draft response         │
                  └────────────────────────────┘
                                 │
                                 ▼


┌──────────────────┐                    ┌──────────────────┐
│   AGENT 4:       │                    │   AGENT 5:       │
│   Problem        │───────────────────▶│   Quality        │
│   Resolver &     │                    │   Reviewer       │
│   Action Taker   │                    │   (Critic)       │
└──────────────────┘                    └──────────────────┘
         │                                       │
         │ Uses Tools:                           │ Reviews:
         │ • process_refund()                    │ • Accuracy
         │ • send_email()                        │ • Completeness
         │ • lookup_customer()                   │ • Tone
         │                                       │ • Policy compliance
         │                                       │
         │                                       ▼
         │                              ┌─────────────────┐
         │                              │ Quality Score   │
         │                              │ APPROVED / FAIL │
         │                              └─────────────────┘
         │                                       │
         │                                       │
         ▼                                       ▼
┌──────────────────────────────────────────────────────┐
│           Human-in-the-Loop Check                    │
│                                                      │
│   IF (high_value_refund OR policy_exception)        │
│   THEN: Pause for human approval                    │
│   ELSE: Proceed to delivery                         │
└──────────────────────────────────────────────────────┘
                         │
                         │
                         ▼
                ┌────────────────┐
                │ FINAL RESPONSE │
                │   TO CUSTOMER  │
                └────────────────┘
```

---

## Agent Interaction Flow

### Phase 1: Understanding (Agent 1)
```
Customer Query
      │
      ▼
┌──────────────────────┐
│ Greeter & Classifier │
└──────────────────────┘
      │
      ├─▶ Classify Intent (REFUND/RETURN/SHIPPING/etc.)
      ├─▶ Assess Sentiment (POSITIVE/NEUTRAL/NEGATIVE/URGENT)
      ├─▶ Determine Priority (LOW/MEDIUM/HIGH/CRITICAL)
      └─▶ Summarize Core Need
      │
      ▼
   [Intent: REFUND, Sentiment: NEGATIVE, Priority: MEDIUM]
```

### Phase 2: Research (Agent 2)
```
Intent + Sentiment
      │
      ▼
┌──────────────────────┐
│ Knowledge Researcher │
└──────────────────────┘
      │
      ├─▶ Tool: search_knowledge_base("refund policy")
      ├─▶ Tool: lookup_customer("12345")
      ├─▶ Tool: web_search("product defect") [if needed]
      └─▶ Compile Findings
      │
      ▼
   [Policy: 30-day refund, Customer: Premium tier, Order: Valid]
```

### Phase 3: Communication (Agent 3)
```
Research Findings
      │
      ▼
┌──────────────────────┐
│ Empathy & Tone       │
│ Adapter              │
└──────────────────────┘
      │
      ├─▶ Adapt tone for NEGATIVE sentiment (more apologetic)
      ├─▶ Personalize for Premium customer
      ├─▶ Structure message clearly
      └─▶ Draft customer-ready response
      │
      ▼
   [Draft: "Dear Jane, I sincerely apologize..."]
```

### Phase 4: Action (Agent 4)
```
Approved Solution
      │
      ▼
┌──────────────────────┐
│ Problem Resolver     │
└──────────────────────┘
      │
      ├─▶ Tool: process_refund(order_id, amount, reason)
      │     │
      │     ├─▶ IF amount > $100: Flag for human approval
      │     └─▶ ELSE: Process automatically
      │
      ├─▶ Tool: send_email(customer, subject, body)
      └─▶ Log actions_taken[]
      │
      ▼
   [Actions: Refund processed ($85), Email sent]
```

### Phase 5: Quality Control (Agent 5)
```
Complete Interaction
      │
      ▼
┌──────────────────────┐
│ Quality Reviewer     │
└──────────────────────┘
      │
      ├─▶ Check: Issue addressed? ✓
      ├─▶ Check: Info accurate? ✓
      ├─▶ Check: Tone appropriate? ✓
      ├─▶ Check: All steps complete? ✓
      └─▶ Score: 9/10
      │
      ▼
   [Status: APPROVED, Recommendation: SEND TO CUSTOMER]
```

---

## Data Flow Through Shared State

```
CustomerCareState Object (Shared Memory)
├── customer_query: "I need a refund for order ORD-789"
├── intent: "REFUND" (set by Agent 1)
├── sentiment: "NEGATIVE" (set by Agent 1)
├── research_findings: ["Policy: 30-day...", "Customer: Premium..."] (Agent 2)
├── proposed_solution: "Process $85 refund" (Agent 2)
├── actions_taken: ["Refund processed", "Email sent"] (Agent 4)
├── requires_human: False (Agent 4 checks)
├── interaction_history: [
│     {agent: "Greeter", action: "Classified intent", timestamp: "..."},
│     {agent: "Researcher", action: "Found policy", timestamp: "..."},
│     ...
│   ]
└── customer_info: {id: "12345", tier: "Premium", ...}
```

Every agent reads from and writes to this shared state, ensuring context is maintained throughout the workflow.

---

## Tool Integration

```
┌─────────────────────────────────────────┐
│             TOOL LAYER                  │
├─────────────────────────────────────────┤
│                                         │
│  🔍 search_knowledge_base()             │
│     └─▶ Simulated FAQ/docs database    │
│                                         │
│  👤 lookup_customer()                   │
│     └─▶ Simulated CRM system           │
│                                         │
│  🌐 web_search()                        │
│     └─▶ Simulated external search      │
│                                         │
│  💰 process_refund()                    │
│     └─▶ Simulated payment API          │
│     └─▶ Triggers human approval if >$100│
│                                         │
│  📧 send_email()                        │
│     └─▶ Simulated email service        │
│                                         │
└─────────────────────────────────────────┘
```

---

## Decision Points & Conditional Logic

### 1. Refund Amount Threshold
```
IF refund_amount > $100:
    care_state.requires_human = True
    care_state.escalation_reason = "High-value refund"
    PAUSE for human approval
ELSE:
    Process automatically
```

### 2. Quality Score Check
```
IF quality_score >= 8:
    status = "APPROVED"
    PROCEED to delivery
ELIF quality_score >= 6:
    status = "NEEDS_REVISION"
    LOOP back to relevant agent
ELSE:
    status = "REJECTED"
    ESCALATE to human review
```

### 3. Intent Classification Routing
```
MATCH intent:
    CASE "REFUND":
        priority = "HIGH"
        required_agents = [Researcher, Resolver]
    CASE "SHIPPING":
        priority = "MEDIUM"
        required_agents = [Researcher, Tone_Adapter]
    CASE "ACCOUNT":
        priority = "LOW"
        required_agents = [Researcher]
```

---

## Error Handling & Fallbacks

```
┌────────────────────────────────┐
│   Error Scenario               │
├────────────────────────────────┤
│                                │
│  Agent fails to respond        │
│  └─▶ Retry with simplified     │
│      prompt                    │
│                                │
│  Tool call fails               │
│  └─▶ Log error, continue with  │
│      partial info              │
│                                │
│  Max iterations reached        │
│  └─▶ Terminate, escalate to    │
│      human                     │
│                                │
│  API rate limit hit            │
│  └─▶ Exponential backoff retry │
│                                │
│  Hallucination detected        │
│  └─▶ Quality reviewer catches, │
│      requests revision         │
│                                │
└────────────────────────────────┘
```

---

## Termination Conditions

The system stops when ONE of these is met:

1. ✅ **Quality Approved**: Quality reviewer approves (score ≥ 8)
2. ⚠️ **Human Escalation**: High-value action requires approval
3. 🔄 **Max Iterations**: Reached maximum revision loops (prevents infinite loops)
4. 🛑 **User Stop**: User cancels the interaction
5. ❌ **Critical Error**: Unrecoverable error (API failure, invalid state)

---

## Scalability Considerations

### Current Implementation (Sequential)
- Latency: ~35-45 seconds per query
- Cost: ~$0.12 per query (5 agents × GPT-4 calls)

### Future Parallel Implementation
```
               ┌──────────────┐
               │   Greeter    │
               └──────┬───────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐         ┌───────────────┐
│  Researcher   │         │ Tone Adapter  │ (Parallel)
│  (Tool calls) │         │ (No tools)    │
└───────┬───────┘         └───────┬───────┘
        │                         │
        └─────────────┬───────────┘
                      ▼
              ┌───────────────┐
              │   Resolver    │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │    Quality    │
              └───────────────┘

Latency: ~20-25 seconds (40% improvement)
```

---

## Monitoring & Observability

### Metrics to Track
```
┌─────────────────────────────────────┐
│  Performance Metrics                │
├─────────────────────────────────────┤
│  • Average response time            │
│  • Quality scores distribution      │
│  • Human escalation rate            │
│  • Cost per resolution              │
│  • Tool usage frequency             │
│  • Agent-specific latency           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Quality Metrics                    │
├─────────────────────────────────────┤
│  • Intent classification accuracy   │
│  • Policy compliance rate           │
│  • Tone appropriateness score       │
│  • Customer satisfaction (CSAT)     │
└─────────────────────────────────────┘
```

---

This architecture enables:
- ✅ Clear separation of concerns
- ✅ Easy debugging (agent boundaries)
- ✅ Flexible scaling (add/remove agents)
- ✅ Quality control (review layer)
- ✅ Risk management (human oversight)
- ✅ Full observability (audit trail)
