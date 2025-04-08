import os
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from decouple import config

#ARQUIVO .ENV
gmail_user = config("GMAIL_USER")
gmail_pass = config("GMAIL_PASS")

# API
API_URL = "https://reqres.in/api/users?page=1"


#Obter usuarios
def get_users():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  #erros HTTP/HTTPS
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao obter usuários da API: {e}")


#criar JSON
def save_users_to_file(users, filename):
    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)


#anexar arquivo no email
def send_email_with_attachment(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port,
                               smtp_username, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


#execução do script
def main():
    try:
        users = get_users()
        filename = "users.json"
        save_users_to_file(users, filename)

        sender_email = gmail_user
        receiver_email = ""
        subject = "Listagem de Usuários"
        body = "Segue em anexo a listagem de usuários."
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        smtp_username = gmail_user
        smtp_password = gmail_pass

        send_email_with_attachment(sender_email, receiver_email, subject, body, filename, smtp_server, smtp_port, > 'GET': (sum),
                                   smtp_username, smtp_password)
        print("Arquivo enviado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()