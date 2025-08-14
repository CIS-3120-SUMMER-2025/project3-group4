import gradio as gr
from workout_generator import generate_workout_plan

def gradio_interface(goal, duration_type, duration_value):
    return generate_workout_plan(goal, duration_type, duration_value)

with gr.Blocks() as demo:
    gr.Markdown("## Custom AI Workout Plan Generator")
    
    goal_input = gr.Dropdown(
        ["strength", "flexibility", "cardio"], 
        label="Select Fitness Goal"
    )
    
    duration_type = gr.Radio(
        ["days", "weeks"], 
        label="Duration Type", 
        value="days"
    )
    
    duration_value = gr.Slider(
        minimum=1, 
        maximum=14, 
        step=1, 
        value=3, 
        label="Number of Days/Weeks"
    )
    
    output_text = gr.Textbox(label="Generated Workout Plan", lines=20)
    submit_btn = gr.Button("Generate Plan")
    
    submit_btn.click(
        fn=gradio_interface, 
        inputs=[goal_input, duration_type, duration_value], 
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch(share=True)