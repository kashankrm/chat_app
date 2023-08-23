import tkinter as tk
import requests
import json




import poe
import logging
import sys

#send a message and immediately delete it
with open("/home/kashan/poe_api/token.txt", "r") as f:
  token = f.read().strip()
poe.logger.setLevel(logging.INFO)
client = poe.Client(token)


# Create the GUI
root = tk.Tk()
root.title('Chatbot')

# Add a text box to display the chatbot's responses
response_text = tk.Text(root, width=50, height=10, state='disabled')
response_text.grid(row=0, column=0, padx=10, pady=10)

# Add an entry box for the user to input messages
user_input = tk.Entry(root, width=50)
user_input.grid(row=1, column=0, padx=10, pady=10)

# Define a function to send the user's message to the chatbot API
def send_message():
    user_message = user_input.get()
    user_input.delete(0, 'end')
    
    # Display the user's message
    # text.insert('end', "user: " + message + '\n')
    for chunk in client.send_message("capybara", user_message, with_chat_break=False):
        pass
    print(chunk["text"])
    # text.insert('end', "bot: " + chunk["text"])
    # Send the request to the API
    bot_response = chunk["text"]
    
    
    
    # Display the chatbot's response
    response_text.configure(state='normal')
    response_text.insert('end', 'You: {}\n'.format(user_message))
    response_text.insert('end', 'Bot: {}\n'.format(bot_response))
    response_text.configure(state='disabled')

# Add a button to submit the user's message to the chatbot API
send_button = tk.Button(root, text='Send', command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10)

# Start the GUI main loop
root.mainloop()