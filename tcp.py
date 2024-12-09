# Classe Cliente
class Cliente:
    # Método construtor
    def __init__(self):
        self.__estado = "CLOSED"  # Estado inicial do cliente

    # estado
    # getter
    @property
    def estado(self):
        return self.__estado

    # setter(estado)
    @estado.setter
    def estado(self, value):
        raise AttributeError("Não é possível alterar o estado do cliente.")

    # Método privado para alterar o estado do cliente dentro da classe
    def __set_estado(self, value):
        self.__estado = value

    # Método de classe para criar um cliente padrão
    @classmethod
    def criar_cliente(cls):
        cliente = Cliente()
        return cliente

    # Método para abrir o cliente e enviar SYN
    def enviar_syn(self, servidor):
        # verifica se o cliente está fechado
        if self.estado == "CLOSED":
            # verifica se o servidor está escutando
            if servidor.estado == "LISTEN":
                # envia SYN
                print("Cliente: Enviando SYN...")
                # transição para SYN_SENT
                self.__set_estado("SYN_SENT")
                # chama o método receber_syn do servidor
                servidor.receber_syn(self)
        else:
            # se não estiver fechado, não pode enviar SYN
            print("Cliente: Não pode enviar SYN neste estado.")

    # Método para receber SYN-ACK
    def receber_syn_ack(self, servidor):
        # verifica se o cliente está em SYN_SENT
        if self.estado == "SYN_SENT":
            # verifica se o servidor está em SYN_RECEIVED
            if servidor.estado == "SYN_RECEIVED":
                # recebe SYN-ACK e envia ACK
                print("Cliente: Recebido SYN-ACK. Enviando ACK...")
                # transição para ESTABLISHED
                self.__set_estado("ESTABLISHED")
                # chama o método enviar_syn_ack do servidor
                servidor.receber_syn_ack(self)
        else:
            # se não estiver em SYN_SENT, não pode receber SYN-ACK
            print("Cliente: Não pode receber SYN-ACK neste estado.")

    # Método para enviar FIN para encerrar a conexão
    def enviar_fin(self, servidor):
        if self.estado == "ESTABLISHED":
            if servidor.estado == "ESTABLISHED":
                print("Cliente: Enviando FIN...")
                self.__set_estado("FIN_WAIT_1")
                servidor.receber_fin(self)
        else:
            print("Cliente: Não pode enviar FIN neste estado.")

    # Método para receber FIN_ACK do servidor
    def receber_fin_ack(self, servidor):
        if self.estado == "FIN_WAIT_1":
            if servidor.estado == "CLOSE_WAIT":
                print("Cliente: Recebido ACK.")
                self.__set_estado("FIN_WAIT_2")
                servidor.enviar_fin(self)
        else:
            print("Cliente: Não pode receber ACK neste estado.")

    # Método para receber FIN do servidor
    def receber_fin(self, servidor):
        if self.estado == "FIN_WAIT_2":
            if servidor.estado == "LAST_ACK":
                print("Cliente: Recebido FIN. Enviando ACK...")
                self.__set_estado("TIME_WAIT")
                servidor.receber_ack(self)
        else:
            print("Cliente: Não pode receber FIN neste estado.")


# Classe Servidor
class Servidor:
    # Método construtor
    def __init__(self):
        self.__estado = "CLOSED"  # Estado inicial do servidor

    # estado
    # getter
    @property
    def estado(self):
        return self.__estado

    # setter(estado)
    @estado.setter
    def estado(self, estado):
        raise AttributeError("Não é possível alterar o estado do servidor.")

    # Método privado para alterar o estado do servidor dentro da classe
    def __set_estado(self, estado):
        self.__estado = estado

    # Método de classe para criar um servidor padrão
    @classmethod
    def criar_servidor(cls):
        servidor = Servidor()
        return servidor

    # Método para abrir o servidor
    def abrir_servidor(self):
        # verifica se o servidor está fechado
        if self.estado == "CLOSED":
            # abre o servidor
            print("Servidor: Abrindo servidor...")
            # transição para LISTEN
            self.__set_estado("LISTEN")
        else:
            # se não estiver fechado, não pode abrir o servidor
            print("Servidor: Não pode abrir o servidor neste estado.")

    # Método para receber SYN
    def receber_syn(self, cliente):
        # verifica se o servidor está escutando
        if self.estado == "LISTEN":
            # verifica se o cliente está enviando SYN
            if cliente.estado == "SYN_SENT":
                # recebe SYN e envia SYN-ACK
                print("Servidor: Recebido SYN. Enviando SYN-ACK...")
                # transição para SYN_RECEIVED
                self.__set_estado("SYN_RECEIVED")
            # chama o método enviar_syn_ack do cliente
            cliente.receber_syn_ack(self)
        else:
            # se não estiver escutando, não pode receber SYN
            print("Servidor: Não pode receber SYN neste estado.")

    # Método para receber SYN-ACK
    def receber_syn_ack(self, cliente):
        # verifica se o servidor está em SYN_RECEIVED
        if self.estado == "SYN_RECEIVED":
            # verifica se o cliente está em ESTABLISHED
            if cliente.estado == "ESTABLISHED":
                # recebe SYN-ACK e estabelece a conexão
                print("Servidor: Recebido SYN-ACK. Conexão estabelecida.")
                # transição para ESTABLISHED
                self.__set_estado("ESTABLISHED")
        else:
            # se não estiver em SYN_RECEIVED, não pode receber SYN-ACK
            print("Servidor: Não pode receber SYN-ACK neste estado.")

    # Método para receber FIN do cliente
    def receber_fin(self, cliente):
        # verifica se o servidor está em ESTABLISHED
        if self.estado == "ESTABLISHED":
            # verifica se o cliente está em FIN_WAIT_1
            if cliente.estado == "FIN_WAIT_1":
                # recebe FIN e envia ACK
                print("Servidor: Recebido FIN. Enviando ACK...")
                # transição para CLOSE_WAIT
                self.__set_estado("CLOSE_WAIT")
                # chama o método receber_fin_ack do cliente
                cliente.receber_fin_ack(self)
        else:
            print("Servidor: Não pode receber FIN neste estado.")

    # Método para enviar FIN para encerrar a conexão
    def enviar_fin(self, cliente):
        # verifica se o servidor está em CLOSE_WAIT
        if self.estado == "CLOSE_WAIT":
            # verifica se o cliente está em FIN_WAIT_2
            if cliente.estado == "FIN_WAIT_2":
                # envia FIN para encerrar a conexão
                print("Servidor: Enviando FIN...")
                # transição para LAST_ACK
                self.__set_estado("LAST_ACK")
                # chama o método receber_fin do cliente
                cliente.receber_fin(self)
        else:
            print("Servidor: Não pode enviar FIN neste estado.")

    # Método para receber ACK do cliente
    def receber_ack(self, cliente):
        # verifica se o servidor está em LAST_ACK
        if self.estado == "LAST_ACK":
            # verifica se o cliente está em TIME_WAIT
            if cliente.estado == "TIME_WAIT":
                # recebe ACK e encerra a conexão
                print("Servidor: Recebido ACK. Conexão encerrada.")
                # transição para CLOSED
                self.__set_estado("CLOSED")
        else:
            print("Servidor: Não pode receber ACK neste estado.")


# Programa principal para testar a implementação do TCP
if __name__ == "__main__":
    print("--------------------")
    print("TCP 3-way handshake")
    print("--------------------")
    c = Cliente.criar_cliente()
    s = Servidor.criar_servidor()
    print("Cliente: ", c.estado)
    print("Servidor: ", s.estado)
    print("--------------------")
    s.abrir_servidor()
    print("--------------------")
    c.enviar_syn(s)

    print("--------------------")
    print("TCP 4-way handshake")
    print("--------------------")
    print("Cliente: ", c.estado)
    print("Servidor: ", s.estado)
    print("--------------------")
    c.enviar_fin(s)
    print("--------------------")
