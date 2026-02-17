"""
Customer Care Multi-Agent System - SIMPLE VERSION
Only needs: pip install openai

No complex dependencies! Perfect for Windows!
DSA 2020A Lab 2 Assignment
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Try to import OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI library not installed!")
    print("Install it with: python -m pip install openai")
    exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

def get_api_key():
    """Get API key from user"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and api_key != "your-openai-api-key-here":
        print("✅ Found API key in environment!")
        return api_key
    
    print("\n" + "="*60)
    print("🔑 OpenAI API Key Required")
    print("="*60)
    print("Get your key from: https://platform.openai.com/api-keys")
    print("="*60)
    
    api_key = input("\nPaste your OpenAI API key here: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        exit(1)
    
    print("✅ API key accepted!\n")
    return api_key

# ============================================================================
# SHARED STATE
# ============================================================================

class CustomerCareState:
    """Shared memory across all agents"""
    def __init__(self):
        self.customer_query = ""
        self.customer_id = ""
        self.intent = ""
        self.sentiment = ""
        self.priority = ""
        self.research_findings = []
        self.customer_info = {}
        self.proposed_solution = ""
        self.final_message = ""
        self.actions_taken = []
        self.requires_human = False
        self.escalation_reason = ""
        self.quality_score = 0
        self.quality_feedback = ""
        self.follow_up_needed = False
        self.interaction_log = []
        
    def log(self, agent, action, result):
        """Log agent interaction"""
        self.interaction_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "result": result[:200]  # Truncate long results
        })
        
    def reset(self):
        """Reset for new query"""
        self.__init__()

# Global state
state = CustomerCareState()

# ============================================================================
# SIMULATED TOOLS (Same as before)
# ============================================================================

def search_knowledge_base(query: str) -> str:
    """Search company policies"""
    kb = {
        "refund": "Refund Policy: Full refunds within 30 days. Process time: 5-7 business days.",
        "return": "Return Process: Contact support → Receive label → Ship back → Refund processed.",
        "shipping": "Shipping: Standard (5-7 days) Free, Express (2-3 days) $15, Overnight $30",
        "tracking": "Tracking available 24-48 hours after order.",
        "account": "Account: Password reset via email. 2FA in Settings.",
        "billing": "Billing: Charges appear as 'ACME INC'. Contact billing@acme.com",
        "password": "Password Reset: Click 'Forgot Password' → Check email for reset link.",
        "warranty": "Warranty: 1 year on electronics. 2 years premium. Claims: warranty@acme.com",
        "exchange": "Exchanges: Available within 30 days. Free for size/color changes."
    }
    
    query_lower = query.lower()
    results = []
    for key, value in kb.items():
        if key in query_lower:
            results.append(f"{key.upper()}: {value}")
    
    return "\n".join(results) if results else "No specific policy found. Contact: support@acme.com"

def lookup_customer(customer_id: str) -> str:
    """Look up customer information"""
    customers = {
        "12345": {
            "name": "Jane Smith",
            "email": "jane@email.com",
            "tier": "Premium",
            "lifetime_value": "$2,450",
            "recent_orders": ["ORD-789: $85"],
            "notes": "VIP customer - expedited service"
        },
        "67890": {
            "name": "John Doe",
            "email": "john@email.com",
            "tier": "Standard",
            "lifetime_value": "$340",
            "recent_orders": ["ORD-321: $1,500"],
            "notes": "First major purchase"
        },
        "11111": {
            "name": "Sarah Johnson",
            "email": "sarah@email.com",
            "tier": "Gold",
            "lifetime_value": "$5,200",
            "recent_orders": ["ORD-555: $220"],
            "notes": "Loyal long-term customer"
        }
    }
    
    customer = customers.get(customer_id, {
        "name": "Valued Customer",
        "tier": "Standard",
        "notes": "New customer"
    })
    
    return json.dumps(customer, indent=2)

def process_refund(order_id: str, amount: float, reason: str) -> str:
    """Process refund (checks for human approval)"""
    if amount > 100:
        state.requires_human = True
        state.escalation_reason = f"Refund over $100 requires approval: ${amount} for {order_id}"
        return f"⚠️ ESCALATED: ${amount} refund requires human approval. Reason: {reason}"
    
    ref = f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    result = f"✓ Refund processed: ${amount} for {order_id}. Reference: {ref}. ETA: 5-7 days."
    state.actions_taken.append(result)
    return result

def send_email(recipient: str, subject: str) -> str:
    """Send email to customer"""
    email_id = f"EMAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    result = f"✓ Email sent to {recipient}. Subject: {subject}. ID: {email_id}"
    state.actions_taken.append(result)
    return result

def track_shipment(order_id: str) -> str:
    """Track package"""
    tracking = {
        "ORD-555": {"status": "In Transit", "location": "Chicago, IL", "eta": "2024-02-18"},
        "ORD-789": {"status": "Delivered", "date": "2024-02-10"}
    }
    data = tracking.get(order_id, {"status": "Not Found", "message": "Check back in 24-48 hours"})
    return json.dumps(data, indent=2)

# ============================================================================
# AI AGENTS (Using OpenAI API Directly)
# ============================================================================

class SimpleAgent:
    """Simple AI agent using OpenAI"""
    
    def __init__(self, client: OpenAI, name: str, role: str, goal: str, instructions: str):
        self.client = client
        self.name = name
        self.role = role
        self.goal = goal
        self.instructions = instructions
        
    def run(self, task: str, context: str = "") -> str:
        """Run agent with a task"""
        system_prompt = f"""You are {self.role}.

Your goal: {self.goal}

Instructions: {self.instructions}

Context from previous agents:
{context}

Be concise but thorough. Format your response clearly."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            state.log(self.name, task[:100], result)
            return result
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            state.log(self.name, task[:100], error_msg)
            return error_msg

# ============================================================================
# MULTI-AGENT SYSTEM
# ============================================================================

class CustomerCareSystem:
    """Main multi-agent customer care system"""
    
    def __init__(self, api_key: str):
        """Initialize system with API key"""
        self.client = OpenAI(api_key=api_key)
        
        # Create 7 specialized agents
        self.agents = {
            "greeter": SimpleAgent(
                self.client,
                "Greeter",
                "Customer Greeter and Intent Classifier",
                "Welcome customers and understand their needs",
                """Analyze the customer query and provide:
                - GREETING: Warm welcome
                - INTENT: (REFUND, RETURN, SHIPPING, TRACKING, ACCOUNT, BILLING, OTHER)
                - SENTIMENT: (POSITIVE, NEUTRAL, NEGATIVE, URGENT)
                - PRIORITY: (LOW, MEDIUM, HIGH, CRITICAL)
                - SUMMARY: What customer needs in 1-2 sentences"""
            ),
            
            "researcher": SimpleAgent(
                self.client,
                "Researcher",
                "Knowledge Researcher",
                "Find accurate information to support resolution",
                """Use these tools to gather information:
                - Search knowledge base for policies
                - Look up customer details
                - Track shipments if relevant
                Provide relevant findings to support the solution."""
            ),
            
            "tone_adapter": SimpleAgent(
                self.client,
                "Tone Adapter",
                "Empathy and Tone Specialist",
                "Craft empathetic, appropriately-toned responses",
                """Create a customer-ready response that:
                - Matches the customer's sentiment
                - Shows genuine empathy
                - Is professional and clear
                - Uses customer's name if available"""
            ),
            
            "resolver": SimpleAgent(
                self.client,
                "Resolver",
                "Problem Resolver",
                "Execute solutions and take actions",
                """Determine what actions to take:
                - Process refunds (flag if over $100)
                - Send emails
                - Track packages
                List specific actions needed."""
            ),
            
            "quality": SimpleAgent(
                self.client,
                "Quality Reviewer",
                "Quality Assurance",
                "Ensure accuracy and completeness",
                """Review the entire interaction:
                - Was the issue properly addressed?
                - Is information accurate?
                - Is tone appropriate?
                - Are all steps complete?
                Provide: APPROVED/NEEDS_REVISION and score (1-10)"""
            ),
            
            "escalation": SimpleAgent(
                self.client,
                "Escalation Coordinator",
                "Escalation Manager",
                "Identify when human intervention is needed",
                """Check if human escalation needed for:
                - High-value transactions (>$100)
                - Policy exceptions
                - VIP customers
                - Complex issues
                Provide: ESCALATE/NO_ESCALATION and reason"""
            ),
            
            "followup": SimpleAgent(
                self.client,
                "Follow-up Scheduler",
                "Follow-up Coordinator",
                "Plan future customer touchpoints",
                """Determine if follow-up needed for:
                - Delivery confirmations
                - Satisfaction checks
                - VIP relationship building
                Provide: FOLLOW_UP/NO_FOLLOW_UP with timing"""
            )
        }
    
    def handle_query(self, customer_query: str, customer_id: str = None) -> Dict:
        """Process customer query through all agents"""
        
        # Reset state
        state.reset()
        state.customer_query = customer_query
        state.customer_id = customer_id or "Unknown"
        
        print("\n" + "="*80)
        print("🎯 NEW CUSTOMER INQUIRY")
        print("="*80)
        print(f"Query: {customer_query}")
        if customer_id:
            print(f"Customer ID: {customer_id}")
        print("="*80 + "\n")
        
        # Build context as we go
        context = f"Customer Query: {customer_query}\n"
        if customer_id:
            context += f"Customer ID: {customer_id}\n"
        
        # AGENT 1: Greeter
        print("🤝 Agent 1: Greeter & Intent Classifier")
        print("-" * 80)
        greeting_result = self.agents["greeter"].run(
            f"Analyze this customer query: {customer_query}",
            context
        )
        print(greeting_result)
        print()
        
        # Extract intent and sentiment
        if "INTENT:" in greeting_result:
            state.intent = greeting_result.split("INTENT:")[1].split("\n")[0].strip()
        if "SENTIMENT:" in greeting_result:
            state.sentiment = greeting_result.split("SENTIMENT:")[1].split("\n")[0].strip()
        if "PRIORITY:" in greeting_result:
            state.priority = greeting_result.split("PRIORITY:")[1].split("\n")[0].strip()
        
        context += f"\n{greeting_result}\n"
        
        # AGENT 2: Researcher
        print("🔍 Agent 2: Knowledge Researcher")
        print("-" * 80)
        
        # Call tools based on intent
        if state.intent and "REFUND" in state.intent:
            kb_result = search_knowledge_base("refund")
            print(f"📚 Knowledge Base: {kb_result}")
        
        if customer_id:
            cust_result = lookup_customer(customer_id)
            print(f"👤 Customer Info: {cust_result}")
            state.customer_info = json.loads(cust_result)
            context += f"\nCustomer Info: {cust_result}\n"
        
        research_task = f"Based on the intent '{state.intent}', what information do we need to resolve this?"
        research_result = self.agents["researcher"].run(research_task, context)
        print(research_result)
        print()
        
        context += f"\n{research_result}\n"
        
        # AGENT 3: Tone Adapter
        print("💙 Agent 3: Empathy & Tone Adapter")
        print("-" * 80)
        tone_task = f"Craft an empathetic response for a customer with {state.sentiment} sentiment."
        tone_result = self.agents["tone_adapter"].run(tone_task, context)
        print(tone_result)
        print()
        
        state.final_message = tone_result
        context += f"\n{tone_result}\n"
        
        # AGENT 4: Resolver
        print("🛠️  Agent 4: Problem Resolver")
        print("-" * 80)
        resolver_task = "What specific actions should we take to resolve this issue?"
        resolver_result = self.agents["resolver"].run(resolver_task, context)
        print(resolver_result)
        
        # Execute actions based on resolver's decision
        if "refund" in resolver_result.lower() and "ORD-" in customer_query:
            # Extract order ID and amount
            order_id = "ORD-789"  # Simplified
            amount = 85.0  # Would extract from query
            if "1500" in customer_query or "$1,500" in customer_query:
                amount = 1500.0
            
            action_result = process_refund(order_id, amount, state.intent)
            print(f"   {action_result}")
            
        if "email" in resolver_result.lower():
            email = state.customer_info.get("email", "customer@email.com")
            email_result = send_email(email, f"Re: Your {state.intent} Request")
            print(f"   {email_result}")
        
        print()
        context += f"\n{resolver_result}\n"
        
        # AGENT 5: Quality Reviewer
        print("✅ Agent 5: Quality Reviewer")
        print("-" * 80)
        quality_task = "Review this entire interaction for quality, accuracy, and completeness."
        quality_result = self.agents["quality"].run(quality_task, context)
        print(quality_result)
        print()
        
        # Extract quality score
        if "/10" in quality_result:
            try:
                score_text = quality_result.split("/10")[0].split()[-1]
                state.quality_score = int(score_text)
            except:
                state.quality_score = 8
        
        # AGENT 6: Escalation Coordinator
        print("🚨 Agent 6: Escalation Coordinator")
        print("-" * 80)
        escalation_task = "Should this be escalated to a human?"
        escalation_result = self.agents["escalation"].run(escalation_task, context)
        print(escalation_result)
        print()
        
        # AGENT 7: Follow-up Scheduler
        print("📅 Agent 7: Follow-up Scheduler")
        print("-" * 80)
        followup_task = "Should we schedule a follow-up with this customer?"
        followup_result = self.agents["followup"].run(followup_task, context)
        print(followup_result)
        print()
        
        if "FOLLOW_UP" in followup_result and "NO_FOLLOW_UP" not in followup_result:
            state.follow_up_needed = True
        
        # Check for human escalation
        if state.requires_human:
            print("\n⚠️  HUMAN ESCALATION REQUIRED")
            print(f"Reason: {state.escalation_reason}")
            print("\n⏸️  Would pause here for human approval...")
            approval = input("\nApprove? (yes/no): ").strip().lower()
            if approval not in ['yes', 'y']:
                return {
                    "status": "ESCALATED",
                    "requires_human": True,
                    "reason": state.escalation_reason
                }
        
        # Final summary
        print("\n" + "="*80)
        print("✅ RESOLUTION COMPLETE")
        print("="*80)
        
        return {
            "status": "RESOLVED",
            "intent": state.intent,
            "sentiment": state.sentiment,
            "priority": state.priority,
            "actions_taken": state.actions_taken,
            "quality_score": state.quality_score,
            "requires_human": state.requires_human,
            "follow_up_needed": state.follow_up_needed,
            "interaction_log": state.interaction_log
        }

# ============================================================================
# INTERACTIVE MENU
# ============================================================================

def show_menu():
    """Display test scenario menu"""
    print("\n" + "="*80)
    print("🤖 CUSTOMER CARE MULTI-AGENT SYSTEM")
    print("="*80)
    print("\nChoose a scenario to test:")
    print("\n1. 📦 Standard Refund (Defective Product)")
    print("2. 💰 High-Value Refund (Requires Approval)")
    print("3. 🚚 Shipping Delay + Billing Issue")
    print("4. 🔐 Password Reset Request")
    print("5. 📍 Track My Package")
    print("6. 🔄 Product Exchange")
    print("7. 📝 Custom Query")
    print("8. 🚪 Exit")
    print("\n" + "="*80)

def get_scenario(choice: str):
    """Get predefined scenario"""
    scenarios = {
        "1": {
            "query": "Hi, I received my order yesterday but the product is completely defective. The screen has lines through it. I'd like a full refund for order ORD-789.",
            "customer_id": "12345"
        },
        "2": {
            "query": "I purchased a gaming laptop last week for $1,500 but it keeps crashing. I want a full refund ASAP!",
            "customer_id": "67890"
        },
        "3": {
            "query": "My package was supposed to arrive 3 days ago but it's stuck in transit. Plus I was charged TWICE - $89.99 twice! This is urgent!",
            "customer_id": "12345"
        },
        "4": {
            "query": "I can't log into my account. I tried resetting my password but I'm not receiving the email. I need to check my order status urgently.",
            "customer_id": "11111"
        },
        "5": {
            "query": "Where is my package? Order ORD-555 was supposed to be here by now and I'm getting worried.",
            "customer_id": "11111"
        },
        "6": {
            "query": "I ordered a medium blue shirt but received a large red one. I'd like to exchange it for the correct item please.",
            "customer_id": "12345"
        }
    }
    return scenarios.get(choice)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function"""
    
    print("\n" + "🌟"*40)
    print("CUSTOMER CARE MULTI-AGENT SYSTEM")
    print("Simple Version - Only needs OpenAI!")
    print("DSA 2020A Lab 2 Assignment")
    print("🌟"*40)
    
    # Get API key
    api_key = get_api_key()
    
    # Initialize system
    print("\n🔧 Initializing 7-agent team...")
    try:
        system = CustomerCareSystem(api_key)
        print("✅ System ready!\n")
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        print("\nMake sure your API key is correct!")
        return
    
    # Interactive loop
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "8":
            print("\n👋 Thank you for using Customer Care System!")
            break
        
        if choice == "7":
            custom_query = input("\nEnter your query: ").strip()
            custom_id = input("Enter customer ID (or press Enter to skip): ").strip() or None
            scenario = {"query": custom_query, "customer_id": custom_id}
        else:
            scenario = get_scenario(choice)
        
        if not scenario:
            print("❌ Invalid choice. Please try again.")
            continue
        
        # Process query
        try:
            result = system.handle_query(
                customer_query=scenario["query"],
                customer_id=scenario.get("customer_id")
            )
            
            # Display summary
            print("\n" + "📊"*40)
            print("RESOLUTION SUMMARY")
            print("📊"*40)
            print(f"\n✅ Status: {result['status']}")
            print(f"🎯 Intent: {result.get('intent', 'N/A')}")
            print(f"😊 Sentiment: {result.get('sentiment', 'N/A')}")
            print(f"⚡ Priority: {result.get('priority', 'N/A')}")
            print(f"⭐ Quality Score: {result.get('quality_score', 'N/A')}/10")
            print(f"\n🎬 Actions Taken:")
            for action in result.get('actions_taken', []):
                print(f"   • {action}")
            print(f"\n👤 Human Escalation: {'Yes' if result.get('requires_human') else 'No'}")
            print(f"📅 Follow-up Needed: {'Yes' if result.get('follow_up_needed') else 'No'}")
            print("\n" + "="*80)
            
        except Exception as e:
            print(f"\n❌ Error processing query: {e}")
            print("This might be an API issue. Check your internet connection and API key.")
        
        continue_choice = input("\nTest another scenario? (yes/no): ").strip().lower()
        if continue_choice not in ['yes', 'y']:
            print("\n👋 Thank you for using Customer Care System!")
            break

if __name__ == "__main__":
    main()
