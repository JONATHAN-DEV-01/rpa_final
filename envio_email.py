import sqlite3
import smtplib
import os
import csv
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv()

def gerar_relatorio_csv(caminho_csv="relatorio.csv"):
    conn = sqlite3.connect("projeto_rpa.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cartas")
    cartas = cursor.fetchall()

    cursor.execute("SELECT * FROM dados_processados")
    validacoes = cursor.fetchall()

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["Code", "Value", "Suit", "Código Válido?"])

        for carta in cartas:
            code = carta[0]
            validacao = next((v[1] for v in validacoes if v[0] == code), False)
            writer.writerow([code, carta[1], carta[2], "Válido" if validacao else "Inválido"])

    conn.close()

def enviar_email():
    remetente = os.environ.get("EMAIL_REMETENTE")
    senha = os.environ.get("EMAIL_SENHA_APP")
    destinatarios = os.environ.get("EMAIL_DESTINATARIOS").split(",")

    caminho_csv = "relatorio.csv"
    gerar_relatorio_csv(caminho_csv)

    msg = MIMEMultipart()
    msg['Subject'] = 'Relatório Automatizado de Cartas (CSV em anexo)'
    msg['From'] = remetente
    msg['To'] = ", ".join(destinatarios)

    corpo = "Olá,\n\nSegue em anexo o relatório de cartas coletadas e processadas.\n\nAtt,\nSeu robô RPA"
    msg.attach(MIMEText(corpo, "plain"))

    with open(caminho_csv, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(caminho_csv))
        part['Content-Disposition'] = f'attachment; filename="{caminho_csv}"'
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatarios, msg.as_string())

        print("✔ E-mail enviado com anexo CSV.")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    enviar_email()
