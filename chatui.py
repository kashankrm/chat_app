import tkinter as tk
import socket


import poe
import logging
import sys

#send a message and immediately delete it
with open("/home/kashan/poe_api/token.txt", "r") as f:
  token = f.read().strip()
poe.logger.setLevel(logging.INFO)
client = poe.Client(token)



# Define a function to send messages to the server
def send_message():
    message = entry.get()
    text.insert('end', "user: " + message + '\n')
    for chunk in client.send_message("capybara", message, with_chat_break=False):
        pass
    print(chunk["text"])
    text.insert('end', "bot: " + chunk["text"])

    # client_socket.send(message.encode())
    entry.delete(0, 'end')


# Create the GUI
root = tk.Tk()
root.title('Message Client')

# Create the message display
text = tk.Text(root)
text.pack()

# Create the message entry
entry = tk.Entry(root)
entry.pack()

# Create the send button
send_button = tk.Button(root, text='Send', command=send_message)
send_button.pack()


# Start the GUI main loop
root.mainloop()

