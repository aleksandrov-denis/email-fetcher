#!/usr/bin/python3

import imaplib, email, subprocess
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default

file = open('../../snake.txt', 'r')
password = file.readline()
file.close()

# connect to mail server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("you@thought.fella", password)

# change this to user arg
mail.select("kdlp/lfx")
_, messages = mail.search(None, 'SUBJECT "PATCH"')
messages = messages[0].split(b" ")

patches = []

# iterate through the messages and download the attachments
for message in messages:
    _, data = mail.fetch(message, "(RFC822)")
    msg = BytesParser(policy=default).parsebytes(data[0][1])
    patch_data = msg.as_string()
    filename = msg['subject'].replace(' ', '_').replace('[', "", 1).replace(']', "", 1).replace('/', "-", 1) + ".patch"
    f = open(filename, "w")
    f.write(patch_data)
    f.close()
    patches.append(filename)
    break


# apply patches and check the output for errors
for patch in patches:
    output = subprocess.run(["git", "am", patch], capture_output=True)
    if output.returncode != 0:
        print(f"{patch} did not apply cleanly:")
        print(output.stderr.decode())
    else:
        print(f"{patch} applied cleanly.")

mail.close()
mail.logout()
