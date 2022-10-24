from datetime import datetime
from smb.SMBConnection import SMBConnection
import shutil
import tempfile

# Author: Daniel Noronha
#   Data: 20/10/2022


class PySamba:
  """
    Módulo criado para interação de sistemas linux com fileservers windows
    utilizando samba. Com esse módulo é possível listar diretórios, verificar
    arquivos e cópiar arquivos de ambiente windows para linux.

    Atributos
    ---------
    share_name : str
      Nome do diretório principal que será acessado no fileserver.
    server_ip : str
      IP do fileserver.
    server_name : str
      Hostname do fileserver.
    network_username : str
      Usuário com permissão para acessar o fileserver.
    network_password : str
      Senha do usuário utilizado no network_username.
    machine_name : str
      Nome do usuário e da máquina linux utilizada.
      Exemplo: user@machine

    Métodos
      lista_arquivos(diretorio)
        - Lista os arquivos de um diretório.

      copia_arquivo(nome_arquivo, diretorio_origem, diretorio_destino=None)
        - Cópia um arquivo para outro diretório.

      verifica_arquivo(nome_arquivo, diretorio)
        - Verifica se um arquivo existe dentro de um diretório.
    -------
  """
  def __init__ (self, share_name, server_ip, server_name, network_username, network_password, machine_name):
    self.share_name = share_name
    self.server_ip = server_ip
    self.server_name = server_name
    self.network_username = network_username
    self.network_password = network_password
    self.machine_name = machine_name

  def lista_arquivos(self, diretorio):
    """
      Lista os arquivos de um diretório que se encontra dentro do share_name (diretório principal).

    Args:
        diretorio (str): Diretório no qual será listado os arquivos.
    """

    # inicia a conexão com o fileserver.
    conn = SMBConnection(self.network_username, self.network_password, self.machine_name, self.server_name, use_ntlm_v2=True)
    assert conn.connect(self.server_ip, 139)

    # lista todos os arquivos do diretório.
    files = conn.listPath(self.share_name, diretorio)
    for item in files:
      print(item.filename)

    # fecha a conexão
    conn.close()

  def copia_arquivo(self, nome_arquivo, diretorio_origem, diretorio_destino=None):
    """
      Cópia o arquivo de um diretório do fileserver para dentro de um diretório
      da sua máquina Linux.

    Args:
        nome_arquivo (str):
          - Nome do arquivo que você quer cópiar.
        diretorio_origem (str):
          - Diretório onde o arquivo se encontra.
        diretorio_destino (str, opicional):
          - Diretório para onde o arquivo será cópiado.
          Caso não seja informado, será cópiado para o diretório onde o script será
          cópiado, o padrão é None.
    """

    # inicia a conexão com o fileserver.
    conn = SMBConnection(self.network_username, self.network_password, self.machine_name, self.server_name, use_ntlm_v2=True)
    assert conn.connect(self.server_ip, 139)

    # cria um arquivo temporário para a transferência.
    file_obj = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    file_name = file_obj.name
    file_attributes, copysize = conn.retrieveFile(self.share_name, f"{diretorio_origem}{nome_arquivo}", file_obj)
    file_obj.close()

    # Cópia o arquivo temporário para um diretório,
    # caso o diretório não for especificado, será
    # cópiado para o diretório local.
    if (diretorio_destino):
      shutil.copy(file_name, f"{diretorio_destino}{nome_arquivo}")
    else:
      shutil.copy(file_name, f"./{nome_arquivo}")

    # fecha a conexão
    conn.close()

  def verifica_arquivo(self, nome_arquivo, diretorio):
    """
      Verifica se um arquivo específico encontra-se em um diretório específico.

    Args:
        nome_arquivo (str): Nome do arquivo que será verificado.
        diretorio (str): Diretório onde será verificado que o arquivo existe

    Returns:
        boolean: Retorna True se o arquivo existir no diretório, se não, retorna False.
    """

    # inicia a conexão com o fileserver.
    conn = SMBConnection(self.network_username, self.network_password, self.machine_name, self.server_name, use_ntlm_v2=True)
    assert conn.connect(self.server_ip, 139)

    # verifica se o arquivo está no local.
    file = conn.getAttributes(self.share_name, f"{diretorio}{nome_arquivo}")

    # fecha a conexão
    conn.close()

    if (file.filename):
      return True
    else:
      return False
