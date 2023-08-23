import tkinter as tk
import requests
import json
import poe
import logging

#set up Path of Exile API client
with open("/home/kashan/poe_api/token.txt", "r") as f:
    token = f.read().strip()
poe.logger.setLevel(logging.INFO)
client = poe.Client(token)

# Define a function to send the user's message to the chatbot API
def send_message(event=None):
    # Get the user's message
    user_message = user_input.get('1.0', 'end-1c')
    user_input.delete('1.0', 'end')
    if not user_message:
        return
    
    # Send the message to the chatbot API
    bot_response = ""
    for chunk in client.send_message("capybara", user_message, with_chat_break=False):
        pass
    bot_response = chunk["text"] + "\n"
        
    # Display the chatbot's response
    response_text.configure(state='normal')
    response_text.insert('end', 'You: {}\n'.format(user_message))
    response_text.insert('end', 'Bot: {}\n'.format(bot_response))
    response_text.configure(state='disabled')

# Create the GUI
root = tk.Tk()
root.title('Chatbot')

# Add a text box to display the chatbot's responses
response_text = tk.Text(root, width=50, height=10, wrap='word', state='disabled')
response_text.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Add a scrollbar to the text box
scrollbar = tk.Scrollbar(root, command=response_text.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
response_text['yscrollcommand'] = scrollbar.set

# Add an entry box for the user to input messages
user_input = tk.Text(root, width=50, height=5, wrap='word')
user_input.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Add a button to submit the user's message to the chatbot API
send_button = tk.Button(root, text='Send', command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

# Bind the 'Enter' key to the send_message function
root.bind('<Return>', send_message)

# Configure grid weights to make the GUI responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Start the GUI main loop
root.mainloop()
