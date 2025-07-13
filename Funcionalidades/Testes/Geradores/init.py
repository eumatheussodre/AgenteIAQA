# __init__.py (dentro da pasta Geradores)

# Importa as funções principais dos módulos deste diretório
# para que possam ser acedidas diretamente a partir de 'Geradores'.

from .generator_Date import gerar_massa_de_dados
from .generator_Casos import gerar_casos_de_teste
from .generator_Bank import gerar_massa_bancaria
from .generator_Report import exportar_relatorio

# É uma boa prática definir '__all__' para explicitar a API pública do pacote.
# Isto controla o que é importado quando se faz 'from .Geradores import *'.
__all__ = [
    "gerar_massa_de_dados",
    "gerar_casos_de_teste",
    "gerar_massa_bancaria",
    "exportar_relatorio"
]
