# agents.py
import os
from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent
from tools import (
    lookup_patient_tool, schedule_appointment_tool, collect_insurance_tool,
    confirm_appointment_tool, send_intake_form_tool, send_reminders_tool
)

# Wrap as LangChain Tools
lookup_tool = Tool(name="lookup_patient", func=lookup_patient_tool, description="Lookup patient record.")
schedule_tool = Tool(name="schedule_appointment", func=schedule_appointment_tool, description="Schedule an appointment.")
insurance_tool = Tool(name="collect_insurance", func=collect_insurance_tool, description="Collect insurance details.")
confirm_tool = Tool(name="confirm_appointment", func=confirm_appointment_tool, description="Confirm appointment.")
intake_tool = Tool(name="send_intake_form", func=send_intake_form_tool, description="Send intake form to email.")
reminder_tool = Tool(name="send_reminders", func=send_reminders_tool, description="Send 3 reminders.")

ALL_TOOLS = [lookup_tool, schedule_tool, insurance_tool, confirm_tool, intake_tool, reminder_tool]

def create_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY first.")
    llm = OpenAI(temperature=0)
    return initialize_agent(ALL_TOOLS, llm, agent="zero-shot-react-description", verbose=False)
