# pysamba
Módulo criado para interação de sistemas linux com fileservers windows utilizando samba. Com esse módulo é possível listar diretórios, verificar arquivos e cópiar arquivos de ambiente windows para linux.   

Exemplos de uso:
```python
from dotenv import load_dotenv
from os import getenv
from pysamba import PySamba

# Carregando variáveis de ambiente.
load_dotenv()

FILENAME = f"arquivoQueSeraVerificado.txt"
DIRETORIO = "/Diretorio/Contabilidade/pessoas/"
DIRETORIO_DESTINO = "/home/usuario/"

# estabelecendo conexão com o fileserver.
pysamba = PySamba(
  share_name="NomeDiretorioPrincipal",
  server_ip="192.168.0.10",
  server_name="MyFileServer",
  network_username=getenv("NomeUser"),
  network_password=getenv("PWD_USER"),
  machine_name="usuario@myserver"
)

# Lista todos os arquivos de um diretório.
pysamba.lista_arquivos(DIRETORIO)

# Verifica se o arquivo está no local.
arquivo_existe = pysamba.verifica_arquivo(FILENAME, DIRETORIO)
print(arquivo_existe)

# Cópiando o arquivo
pysamba.copia_arquivo(
  nome_arquivo=FILENAME,
  diretorio_origem=DIRETORIO,
  diretorio_destino=DIRETORIO_DESTINO)

```
