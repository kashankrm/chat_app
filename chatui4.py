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
    
        
    # Display the chatbot's response
    response_text.configure(state='normal')
    response_text.insert('end', 'You: {}\n'.format(user_message))
    response_text.insert('end', 'Bot: ')
    # Send the message to the chatbot API
    # bot_response = ""
    print("Bot: ", end="", flush=True)
    for chunk in client.send_message("capybara", user_message, with_chat_break=False):
        # bot_response += chunk["new_text"] 
        response_text.insert('end', chunk["text_new"])
        print(chunk["text_new"], end="", flush=True)
    response_text.insert('end', '\n')
    response_text.configure(state='disabled')
    
    # Scroll to the bottom of the response text box
    response_text.see('end')

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
user_input.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

# Add a button to submit the user's message to the chatbot API
send_button = tk.Button(root, text='Send', command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='e')

# Bind the 'Enter' key to the send_message function
def enter_key(event):
    if event.keysym == 'Return' and event.state != 0x0010:
        send_message(event)
        
user_input.bind('<Key>', enter_key)

# Configure grid weights to make the GUI responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Start the GUI main loop
root.mainloop()