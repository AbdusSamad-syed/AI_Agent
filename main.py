# main.py
import os
import gradio as gr
from agents import create_agent
from utils import ensure_sample_data

ensure_sample_data()
agent = create_agent()

def run_workflow(name, dob, doctor, location, patient_type, email, phone, carrier, member_id, group_id):
    payload = "||".join([name,dob,doctor,location,patient_type,email,phone,carrier,member_id,group_id])
    prompt = (
        "Use tools to: 1) lookup patient, 2) schedule, 3) collect insurance, "
        "4) confirm, 5) send intake form, 6) send reminders. "
        f"Payload: {payload}"
    )
    try:
        return agent.run(prompt)
    except Exception as e:
        return f"ERROR: {e}"

with gr.Blocks(title="AI Scheduling Agent") as demo:
    gr.Markdown("# 🏥 AI Scheduling Agent")
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(label="Name")
            dob = gr.Textbox(label="DOB (YYYY-MM-DD)")
            doctor = gr.Dropdown(["Dr. Smith","Dr. Kapoor","Dr. Rao"], label="Doctor")
            location = gr.Textbox(label="Location")
            patient_type = gr.Radio(["new","returning"], label="Patient Type", value="new")
            email = gr.Textbox(label="Email")
            phone = gr.Textbox(label="Phone")
            carrier = gr.Textbox(label="Insurance Carrier")
            member_id = gr.Textbox(label="Member ID")
            group_id = gr.Textbox(label="Group ID")
            submit = gr.Button("Book Appointment")
        with gr.Column():
            output = gr.Textbox(label="Agent Output", lines=15)
    submit.click(fn=run_workflow, inputs=[name,dob,doctor,location,patient_type,email,phone,carrier,member_id,group_id], outputs=output)

if __name__ == "__main__":
    demo.launch()
