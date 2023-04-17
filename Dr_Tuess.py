import tkinter as tk
import openai
import requests
from io import BytesIO
from PIL import Image, ImageTk


# Set up OpenAI API key
openai.api_key = ""

# Set up DALL-E API key and endpoint
dalle_api_key = ""
dalle_api_url = 'https://api.openai.com/v1/images/generations'

def get_selected_topic():
    for topic, var in topic_var.items():
        if var.get():
            return topic
    return None


def generate_story(prompt, theme):
    model_engine = "text-davinci-002"
    prompt = f"Generate a 200 word story that is {theme} and about {prompt}"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


def generate_image(prompt):
    headers = {"Authorization": f"Bearer {dalle_api_key}"}
    data = {"prompt": prompt, "num_images": 1}
    response = requests.post(dalle_api_url, json=data, headers=headers)

    if response.status_code == 200:
        try:
            image_url = response.json()['data'][0]['url']
        except (IndexError, KeyError) as e:
            print(f"Unexpected response format: {response.json()}")
            return None

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Error generating image:", response.text)
        return None

def on_submit():

    prompt = prompt_entry.get()
    topic = get_selected_topic()
    story = generate_story(prompt, topic)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, story)

    image_prompt = f"{topic} {prompt}"
    image = generate_image(image_prompt)


    if image:
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
        image = image.resize((canvas_width, canvas_height), Image.LANCZOS)


        photo = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas.image = photo


root = tk.Tk()
root.title("AI Story & Image Generator")
root.configure(bg="dark grey")

# Entry for prompt
prompt_entry = tk.Entry(root, width=40, bg="dark grey", fg="white")
prompt_entry.grid(row=0, column=0, padx=10, pady=10)

# Submit button
submit_button = tk.Button(root, text="Generate", command=on_submit, bg="dark grey", fg="white")
submit_button.grid(row=0, column=1, padx=10, pady=10)



# Checkboxes for topics
topics = ["sci-fi", "fantasy", "horror"]
topic_var = {topic: tk.BooleanVar() for topic in topics}
for i, topic in enumerate(topics):
    topic_check = tk.Checkbutton(root, text=topic, variable=topic_var[topic])
    topic_check.grid(row=0, column=i+2, padx=10, pady=10)


# Text box for story
text_box = tk.Text(root, wrap=tk.WORD, width=60, height=30, bg="black", fg="white")
text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
scrollbar = tk.Scrollbar(root, command=text_box.yview)
scrollbar.grid(row=1, column=2, sticky="ns")
text_box.config(yscrollcommand=scrollbar.set)

# Canvas for displaying image
canvas = tk.Canvas(root, width=500, height=500, bg="dark grey")
canvas.grid(row=1, column=3, columnspan=2, padx=10, pady=10)









root.mainloop()

