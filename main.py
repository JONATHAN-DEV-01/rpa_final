import api
import processamento
import envio_email

def executar_projeto():
    print("Coletando dados...")
    api.coletar_dados()

    print("Processando dados...")
    processamento.processar_dados()

    print("Enviando relatório por e-mail...")
    envio_email.enviar_email()

    print("Processo concluído com sucesso.")

if __name__ == "__main__":
    executar_projeto()
