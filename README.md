# Customer Care Multi-Agent System 🤖
**DSA 2020A: Artificial Intelligence - Lab 2 Assignment**

A sophisticated multi-agent AI system that handles complex customer inquiries through collaborative team of specialized agents using CrewAI framework.

---

## 📋 Table of Contents
- [Use Case & Rationale](#use-case--rationale)
- [Agent Team Architecture](#agent-team-architecture)
- [How to Run](#how-to-run)
- [Example Interactions](#example-interactions)
- [Key Challenges & Solutions](#key-challenges--solutions)
- [Technical Implementation](#technical-implementation)
- [Reflection](#reflection)

---

## 🎯 Use Case & Rationale

### Chosen Domain: Customer Care Team

**Why Multi-Agent Approach?**

Traditional single-agent customer service systems face several limitations:
1. **Jack-of-all-trades problem**: One agent trying to do everything leads to mediocre performance
2. **No specialization**: Can't optimize prompts for specific sub-tasks (empathy vs. technical resolution)
3. **No quality control**: Responses go directly to customers without review
4. **Limited context retention**: Hard to maintain state across complex workflows

**Our Multi-Agent Solution:**

We implement a **collaborative team of 5 specialized agents** that mirror a real customer service department:
- **Division of Labor**: Each agent has a specific expertise (greeting, research, empathy, action, quality)
- **Iterative Improvement**: Quality reviewer provides feedback loop
- **Risk Management**: Human-in-the-loop for sensitive actions (high-value refunds)
- **Shared Memory**: All agents access common state to maintain context
- **Better Outcomes**: Specialization leads to higher quality responses and fewer errors

---

## 🏗️ Agent Team Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (CrewAI)                      │
│        (Sequential Process with Shared State Management)      │
└─────────────────────────┬─────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┬──────────────────┐
         │                │                │                  │
         ▼                ▼                ▼                  ▼
┌─────────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────────┐
│   AGENT 1:      │ │  AGENT 2:   │ │  AGENT 3:    │ │   AGENT 4:     │
│   Greeter &     │→│  Knowledge  │→│  Empathy &   │→│   Problem      │
│   Intent        │ │  Researcher │ │  Tone        │ │   Resolver &   │
│   Classifier    │ │             │ │  Adapter     │ │   Action Taker │
└─────────────────┘ └─────────────┘ └──────────────┘ └────────────────┘
         │                │                │                  │
         └────────────────┴────────────────┴──────────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │   AGENT 5:      │
                          │   Quality       │
                          │   Reviewer      │
                          │   (Critique)    │
                          └─────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Human-in-the-Loop Check     │
                    │  (For sensitive actions)     │
                    └──────────────────────────────┘
```

### Agent Roles & Responsibilities

| Agent | Role | Key Responsibilities | Tools |
|-------|------|---------------------|-------|
| **Greeter** | First Contact & Intent Classifier | • Warm welcome<br>• Intent classification (REFUND/RETURN/SHIPPING/etc.)<br>• Sentiment analysis (POSITIVE/NEUTRAL/NEGATIVE/URGENT)<br>• Priority assessment (LOW/MEDIUM/HIGH/CRITICAL) | None |
| **Researcher** | Knowledge Base Expert | • Search company policies & FAQs<br>• Customer history lookup<br>• External web search for additional context<br>• Compile relevant information | • `search_knowledge_base`<br>• `lookup_customer`<br>• `web_search` |
| **Tone Adapter** | Empathy & Communication Specialist | • Craft empathetic responses<br>• Adapt tone based on sentiment<br>• Ensure professional, caring communication<br>• Add appropriate disclaimers | None |
| **Resolver** | Action Executor | • Process refunds<br>• Send emails to customers<br>• Execute approved solutions<br>• Flag actions requiring human approval | • `process_refund`<br>• `send_email`<br>• `lookup_customer` |
| **Quality Reviewer** | QA & Critic | • Review entire interaction<br>• Verify accuracy of information<br>• Assess tone appropriateness<br>• Approve or request revisions<br>• Quality score (1-10) | None |

### Communication Flow

1. **Sequential Process**: Tasks execute in order (greeting → research → tone → resolution → review)
2. **Shared State**: `CustomerCareState` object accessible by all agents
3. **Context Passing**: Each task receives output from previous task
4. **Feedback Loop**: Quality reviewer can request revisions (future enhancement)
5. **Termination Conditions**:
   - Quality reviewer approves (APPROVED status)
   - Human escalation triggered (refunds >$100)
   - Max iterations reached (prevents infinite loops)
   - User stops interaction

---

## 🚀 How to Run

### Prerequisites
- Python 3.9 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd customer-care-multi-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your OpenAI API key**

Option A: Environment variable (recommended)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Option B: Create `.env` file
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

Option C: Direct in code (not recommended for production)
```python
API_KEY = "your-api-key-here"
```

### Running the System

#### Command Line Execution

```bash
python customer_care_system.py
```

#### Python Script Usage

```python
from customer_care_system import CustomerCareCrew

# Initialize the crew
care_system = CustomerCareCrew(
    openai_api_key="your-key-here",
    model="gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
)

# Handle a customer query
result = care_system.handle_customer_query(
    customer_query="I need a refund for my broken laptop",
    customer_id="12345"
)

print("Status:", result["status"])
print("Actions Taken:", result["actions_taken"])
```

#### Jupyter Notebook Demo

```bash
jupyter notebook demo_notebook.ipynb
```

### Configuration Options

You can customize the system behavior:

```python
# Use different LLM model
care_system = CustomerCareCrew(api_key, model="gpt-3.5-turbo")

# Adjust agent behavior via temperature
llm = ChatOpenAI(model="gpt-4", temperature=0.7)  # More creative
llm = ChatOpenAI(model="gpt-4", temperature=0.2)  # More deterministic
```

---

## 💬 Example Interactions

### Example 1: Standard Refund Request

**Customer Query:**
> "Hi, I received my order but the product is defective. I'd like a refund for order ORD-789. My customer ID is 12345."

**Agent Collaboration Transcript:**

```
🎯 Agent 1: Greeter & Intent Classifier
─────────────────────────────────────────
Output:
GREETING: Hello! I'm sorry to hear you received a defective product. 
          I'm here to help you with that right away.
INTENT: REFUND
SENTIMENT: NEGATIVE (disappointed but polite)
PRIORITY: MEDIUM
SUMMARY: Customer Jane Smith (Premium tier) received defective product 
         in order ORD-789 and requests a refund.

🔍 Agent 2: Knowledge Researcher
─────────────────────────────────────────
Tools Used:
  • lookup_customer(12345)
  • search_knowledge_base("refund policy")

Output:
CUSTOMER INFO:
  - Name: Jane Smith
  - Tier: Premium
  - Lifetime Value: $2,450
  - Account Since: 2022-03-15
  
COMPANY POLICY:
  "Full refunds within 30 days for unused products. 
   Process time: 5-7 business days."
  
PROPOSED SOLUTION:
  1. Verify order is within 30-day window
  2. Process full refund for ORD-789
  3. Offer replacement option (premium customer)
  4. Expedite refund processing (VIP treatment)

💙 Agent 3: Tone Adapter
─────────────────────────────────────────
Output:
"Dear Jane,

I sincerely apologize for the inconvenience this has caused you. 
As a valued Premium member since 2022, you deserve better, and I 
want to make this right immediately.

I've reviewed your order ORD-789, and I'm happy to confirm that 
you're eligible for a full refund, which we'll process right away. 
You should see the amount back in your account within 5-7 business 
days, though we'll do our best to expedite it for you.

If you'd prefer a replacement instead, we'd be more than happy to 
send one out with expedited shipping at no charge.

What would you prefer? We're here to help!"

🛠️ Agent 4: Problem Resolver
─────────────────────────────────────────
Tools Used:
  • process_refund("ORD-789", 85.00, "Defective product")
  • send_email("jane.smith@email.com", "Your Refund is Being Processed", ...)

Output:
ACTIONS TAKEN:
  ✓ Refund processed: $85.00 for order ORD-789
    Reference: REF-20240216143022
    ETA: 5-7 business days
  
  ✓ Email sent to jane.smith@email.com
    Subject: Your Refund is Being Processed
    Email ID: EMAIL-20240216143023

✅ Agent 5: Quality Reviewer
─────────────────────────────────────────
Output:
QUALITY ASSESSMENT:

Status: APPROVED ✓

Quality Score: 9/10

What was done well:
  ✓ Quick intent identification
  ✓ Accurate customer lookup and policy retrieval
  ✓ Empathetic, personalized tone (addressed by name)
  ✓ Acknowledged premium status appropriately
  ✓ Clear explanation of refund timeline
  ✓ Proactive offer of replacement option
  ✓ Actions executed correctly with confirmations

Minor improvements:
  • Could have asked about cause of defect (product quality feedback)
  
Recommendation: SEND TO CUSTOMER
Customer satisfaction probability: HIGH

═════════════════════════════════════════════════════
✅ RESOLUTION COMPLETE
═════════════════════════════════════════════════════
Status: RESOLVED
Actions: Refund processed ($85), Email sent
Duration: ~45 seconds
```

---

### Example 2: High-Value Refund (Human Escalation)

**Customer Query:**
> "I need to return a laptop I bought last week for $1,500. It's not working properly and I want a full refund."

**Agent Collaboration Transcript:**

```
🎯 Agent 1: Greeter & Intent Classifier
─────────────────────────────────────────
Output:
GREETING: I understand how frustrating it must be to have a 
          non-functioning laptop. Let me help you resolve this.
INTENT: REFUND
SENTIMENT: NEGATIVE (frustrated)
PRIORITY: HIGH (high-value item)
SUMMARY: Customer has a malfunctioning $1,500 laptop purchased 
         last week and wants full refund.

🔍 Agent 2: Knowledge Researcher
─────────────────────────────────────────
Output:
POLICY FINDINGS:
  • Within 30-day return window ✓
  • Full refund eligible
  • High-value transaction requires manager approval
  
RECOMMENDATION:
  • Process refund with manager authorization
  • Offer tech support troubleshooting first (retention)
  • Document issue for product quality team

💙 Agent 3: Tone Adapter
─────────────────────────────────────────
Output:
"I completely understand your frustration with a new laptop that's 
not working as expected. That's definitely not the experience we 
want for you.

Your laptop is well within our 30-day return window, so a full 
refund is absolutely possible. Given the value of your purchase, 
I'll need to get quick approval from my manager, which typically 
takes just a few minutes.

Before we proceed, would you be open to a brief tech support 
session? Sometimes issues can be resolved quickly, and if not, 
we'll still process your refund immediately. What do you think?"

🛠️ Agent 4: Problem Resolver
─────────────────────────────────────────
Tools Used:
  • process_refund("ORD-456", 1500.00, "Laptop malfunction")

Output:
⚠️ ESCALATION TRIGGERED

REASON: Refund amount $1,500.00 exceeds $100 threshold
STATUS: Awaiting manager approval

PENDING ACTIONS:
  • Refund: $1,500.00 for order ORD-456
  • Reference: REF-20240216143524
  
══════════════════════════════════════════════════════
⚠️  HUMAN ESCALATION REQUIRED
══════════════════════════════════════════════════════
Reason: Refund over $100 requires manager approval: 
        $1,500 for order ORD-456

⏸️  Pausing for human approval...

══════════════════════════════════════════════════════
HUMAN APPROVAL REQUEST
══════════════════════════════════════════════════════
Escalation Reason: High-value refund request
Customer: Jane Smith (Premium, $2,450 LTV)
Amount: $1,500.00
Reason: Laptop malfunction within 30 days
Policy Check: ✓ Eligible for refund
Risk Assessment: LOW (legitimate return)

Actions taken so far:
  • Customer verified
  • Policy checked
  • Empathetic response drafted

Waiting for manager input...

[MANAGER APPROVES] ✓

✅ Agent 5: Quality Reviewer
─────────────────────────────────────────
Output:
QUALITY ASSESSMENT:

Status: APPROVED (pending manager decision) ✓

Quality Score: 10/10

What was done well:
  ✓ Correctly identified high-value transaction
  ✓ Appropriately escalated to human review
  ✓ Offered tech support as retention strategy
  ✓ Maintained empathetic tone despite escalation
  ✓ Transparent about approval process
  ✓ Proper risk management

Recommendation: EXECUTE UPON MANAGER APPROVAL

═════════════════════════════════════════════════════
✅ RESOLUTION COMPLETE (After Approval)
═════════════════════════════════════════════════════
Status: RESOLVED
Requires Human: Yes (APPROVED)
Actions: Refund processed ($1,500) after manager approval
Duration: ~2 minutes (including human review)
```

---

### Example 3: Complex Multi-Issue Query

**Customer Query:**
> "My package was supposed to arrive 3 days ago but tracking shows it's stuck in transit. I also noticed I was charged twice on my credit card. This is really frustrating because I needed this for a gift. Can someone help me ASAP?"

**Key Interaction Points:**

```
🎯 Greeter identifies: MULTIPLE ISSUES
  - Primary: SHIPPING (delayed package)
  - Secondary: BILLING (duplicate charge)
  - Context: Time-sensitive (gift)
  - Sentiment: URGENT/FRUSTRATED
  - Priority: HIGH

🔍 Researcher finds:
  - Tracking: Package delayed due to weather
  - Billing: Temporary authorization hold + actual charge
  - Customer history: First-time issue

💙 Tone Adapter crafts:
  - Acknowledges frustration and urgency
  - Addresses both issues separately
  - Sets clear expectations
  - Offers proactive compensation

🛠️ Resolver executes:
  - Contacts carrier for expedited delivery
  - Explains duplicate charge (will drop in 3-5 days)
  - Offers $20 gift card for inconvenience
  
✅ Quality checks:
  - Both issues addressed ✓
  - Appropriate compensation ✓
  - Clear timeline provided ✓
  - Empathy demonstrated ✓
```

---

## 🔧 Key Challenges & Solutions

### Challenge 1: Coordination & Context Loss
**Problem**: Agents lose context when working sequentially, leading to repetitive questions or missed details.

**Solution**:
- Implemented **shared state object** (`CustomerCareState`) accessible by all agents
- Each agent logs interactions to shared history
- Context passing between tasks via CrewAI's task chaining
- Supervisor has global view of all agent activities

```python
# Shared state maintains context
care_state.log_interaction(
    agent_name="Researcher",
    action="Looked up customer",
    result="Found Premium customer with $2,450 LTV"
)
```

### Challenge 2: Hallucinations & Inaccurate Information
**Problem**: LLMs may invent policies, customer data, or refund numbers.

**Solution**:
- **Tool-based grounding**: All factual info comes from tools (KB search, DB lookup)
- **Quality Reviewer agent**: Explicitly checks for accuracy before approval
- **Structured outputs**: Agents return data in expected formats
- **Verification layer**: Resolver agent confirms data before taking action

```python
# Tools return structured data, not LLM-generated fiction
customer_data = lookup_customer("12345")  # Actual DB lookup
policy = search_knowledge_base("refund")  # Actual KB search
```

### Challenge 3: Infinite Loops & Non-Termination
**Problem**: Agents may keep revising or researching without reaching a conclusion.

**Solution**:
- **Sequential process**: Clear task order prevents circular dependencies
- **Quality reviewer terminates**: Explicit APPROVED/NEEDS_REVISION gates
- **Max iterations limit**: Prevent runaway processes
- **Human escalation**: Breaks loops for edge cases

```python
# Sequential process ensures forward progress
process=Process.sequential  # Not Process.hierarchical (prevents loops)

# Quality reviewer provides clear termination
if quality_score >= 8:
    return "APPROVED"
```

### Challenge 4: High API Costs
**Problem**: 5 agents × multiple calls = expensive at scale.

**Solution**:
- **Right-sized models**: Use GPT-3.5-turbo for simple tasks, GPT-4 for complex
- **Efficient prompts**: Minimize token usage in system prompts
- **Caching**: Reuse research findings for similar queries
- **Batching**: Process multiple queries in parallel (future enhancement)

```python
# Cost optimization
simple_agent = Agent(llm=ChatOpenAI(model="gpt-3.5-turbo"))  # Cheap
critical_agent = Agent(llm=ChatOpenAI(model="gpt-4"))  # Expensive but accurate
```

### Challenge 5: Debugging Multi-Agent Interactions
**Problem**: Hard to trace which agent caused an error or bad output.

**Solution**:
- **Verbose logging**: Every agent logs actions and decisions
- **Interaction history**: Full audit trail in shared state
- **Streaming output**: Real-time visibility into agent reasoning
- **Agent identifiers**: Clear labeling of which agent is speaking

```python
# Full observability
verbose=True  # Enable detailed logging
care_state.interaction_history  # Audit trail of all agent actions
```

---

## 🔬 Technical Implementation Details

### Framework: CrewAI
**Why CrewAI?**
- ✅ **Role-based design**: Natural fit for specialized agents
- ✅ **Task management**: Built-in task chaining and context passing
- ✅ **Tool integration**: Easy to add custom tools
- ✅ **Process control**: Sequential and hierarchical workflows
- ✅ **Production-ready**: Good documentation and community support

**Alternatives considered:**
- LangGraph: More flexible but steeper learning curve
- AutoGen: Better for conversational agents, less structured for workflows
- OpenAI Swarm: Too lightweight for complex orchestration

### Tools Implemented

| Tool Name | Purpose | Input | Output | Complexity |
|-----------|---------|-------|--------|------------|
| `search_knowledge_base` | Find company policies | Query string | Policy text | Low |
| `lookup_customer` | Retrieve customer data | Customer ID | JSON object | Low |
| `web_search` | External info retrieval | Query string | Search results | Medium |
| `process_refund` | Execute refund transaction | Order ID, amount, reason | Confirmation + escalation flag | High |
| `send_email` | Send customer communication | Recipient, subject, body | Email ID | Medium |

### Shared Memory Implementation

```python
class CustomerCareState:
    """Central state object shared across all agents"""
    def __init__(self):
        self.customer_query = ""
        self.intent = ""
        self.sentiment = ""
        self.research_findings = []
        self.proposed_solution = ""
        self.actions_taken = []
        self.requires_human = False
        self.interaction_history = []
```

### Human-in-the-Loop Mechanism

```python
def _request_human_approval(self) -> bool:
    """Pauses execution and waits for human decision"""
    print(f"⚠️  ESCALATED: {care_state.escalation_reason}")
    
    # In production: integrate with Slack/ticketing system
    # For demo: simulate with terminal input
    user_input = input("Approve? (yes/no): ")
    return user_input.lower() in ['yes', 'y']
```

### Reflection/Critique Loop

The **Quality Reviewer agent** provides a built-in critique mechanism:
1. Reviews entire interaction history
2. Scores quality (1-10)
3. Checks for: accuracy, completeness, tone, policy compliance
4. Returns APPROVED or NEEDS_REVISION
5. Future enhancement: Trigger re-work if score < 7

---

## 🧠 Reflection: Multi-Agent vs. Single-Agent

### Advantages of Multi-Agent Approach

**1. Specialization & Expertise**
- **Single Agent**: Jack-of-all-trades, master of none. One prompt tries to do everything.
- **Multi-Agent**: Each agent optimized for specific task (empathy vs. action execution).
- **Result**: Higher quality outputs in each domain. Tone adapter writes better empathetic messages than a generalist would.

**2. Built-in Quality Control**
- **Single Agent**: Responses go directly to customers without review.
- **Multi-Agent**: Quality reviewer acts as safety net, catches errors before delivery.
- **Result**: Fewer mistakes reaching customers, better brand protection.

**3. Easier Debugging & Iteration**
- **Single Agent**: Hard to pinpoint where things went wrong in a complex task.
- **Multi-Agent**: Clear audit trail showing which agent made which decision.
- **Result**: Faster bug fixes, easier prompt engineering improvements.

**4. Risk Management**
- **Single Agent**: No natural checkpoint for dangerous actions (e.g., large refunds).
- **Multi-Agent**: Resolver agent flags sensitive actions, triggering human approval.
- **Result**: Better compliance, reduced financial risk.

**5. Parallel Processing (Future)**
- **Single Agent**: Must do everything sequentially.
- **Multi-Agent**: Researcher can search KB while Tone Adapter drafts message (parallel execution).
- **Result**: Faster response times at scale.

### Trade-offs & When NOT to Use Multi-Agent

**Disadvantages:**
1. **Higher Cost**: 5 agents × API calls = 5x cost (mitigated by right-sizing models)
2. **Increased Latency**: Sequential processing takes longer than single call
3. **Coordination Overhead**: Agents need shared state, complex orchestration logic
4. **Over-engineering**: Simple queries (e.g., "What's your return policy?") don't need 5 agents

**When to Use Single Agent:**
- Simple Q&A or FAQ lookups
- Speed is critical (real-time chat)
- Budget constraints (high volume, low margin)
- Tasks with no natural subtask division

**When Multi-Agent Shines:**
- Complex workflows with distinct phases (research → analyze → act → review)
- High-stakes decisions requiring multiple checks
- Need for specialization (technical expertise + empathy + compliance)
- Quality is more important than speed

### Real-World Applicability

**Production Considerations:**
1. **Scalability**: Add agent orchestration layer (e.g., Kubernetes) for parallel processing
2. **Monitoring**: Integrate with observability tools (Datadog, Sentry) to track agent performance
3. **A/B Testing**: Compare multi-agent vs. single-agent outcomes with real customers
4. **Cost Optimization**: Use cheaper models (GPT-3.5) for routine agents, reserve GPT-4 for complex reasoning
5. **Human Handoff**: Integrate with existing ticketing systems (Zendesk, Intercom)

**Ethical Considerations:**
- **Transparency**: Customers should know they're interacting with AI
- **Accountability**: Clear responsibility chain when things go wrong
- **Bias Mitigation**: Each agent's prompts must be audited for fairness
- **Data Privacy**: Shared state must be properly secured (GDPR compliance)
- **Over-automation Risk**: Some situations genuinely require human judgment

---

## 📊 Performance Metrics (Hypothetical)

Based on the design, expected improvements vs. single-agent baseline:

| Metric | Single Agent | Multi-Agent | Improvement |
|--------|-------------|-------------|-------------|
| **First-Response Quality** | 72% approved | 89% approved | +23% |
| **Escalation Accuracy** | 83% | 96% | +16% |
| **Tone Appropriateness** | 68% | 91% | +34% |
| **Policy Compliance** | 78% | 95% | +22% |
| **Response Time** | 8 seconds | 35 seconds | -340% ⚠️ |
| **Cost per Query** | $0.03 | $0.12 | +300% ⚠️ |
| **Customer Satisfaction** | 3.2/5 | 4.4/5 | +38% |

**Key Insight**: Multi-agent trades speed and cost for quality. Ideal for high-value customers where satisfaction matters more than response time.

---

## 🚀 Future Enhancements

1. **Parallel Agent Execution**: Run Researcher + Tone Adapter concurrently
2. **Learning from Feedback**: Store quality scores, retrain prompts on low-scoring interactions
3. **Dynamic Agent Selection**: Supervisor decides which agents to invoke (not always all 5)
4. **Multi-Language Support**: Add translation agent for global customer base
5. **Sentiment Tracking**: Monitor sentiment shifts throughout interaction
6. **Integration with CRM**: Pull real customer data, update tickets automatically
7. **Voice Interface**: Add speech-to-text for phone support
8. **Agent Performance Dashboard**: Real-time monitoring of each agent's contributions

---

## 📚 References & Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Multi-Agent Systems](https://python.langchain.com/docs/modules/agents/)
- [DeepLearning.AI: Multi AI Agent Systems](https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/)
- [OpenAI Best Practices for Agents](https://platform.openai.com/docs/guides/function-calling)
- [Ethical AI in Customer Service](https://www.forrester.com/blogs/ethical-ai-customer-service/)

---

## 📝 License
MIT License - Feel free to use for educational purposes.

## 👥 Contributors
David Kamau
dakkamau@usiu.ac.ke

---

**Questions?** Open an issue or contact via email!
