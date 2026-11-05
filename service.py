from ast import Raise
from multiprocessing import Value
from re import error

import pandas as pd
from datetime import datetime, date


class Validar_Dados_registro:
    def validar(self, list_dict):
        df = pd.DataFrame(list_dict)
        caracteres = df.iloc[:, 0].str.len() < 30
        caracteres2 = df.iloc[:, 1].str.len() < 30
        valid_colunas = caracteres & caracteres2
        validando_caract = (~valid_colunas).any()
        assert not validando_caract, "ERRO: string muito grande!"

        data_convert = pd.to_datetime(df.iloc[:, 3])
        data_atual = date.today()
        limite = pd.to_datetime(data_atual)
        validando_data = data_convert <= limite
        # ex: [True, False, True ...] se a data for menor que a atual e não ultrapassada

        verificar_data = (~validando_data).any()
        # qualquer False será True com a converção (~) e vice-versa
        # any() identifica algum True convertido
        assert not verificar_data, "ERRO: Data inválida!"

        valor_vazio = (
            df.isna().any().any()
        )  # retorna um único valor booleano diretamente em vez de uma serie
        assert not valor_vazio, "ERRO: Existem valore(s) vázio(s)"

        valores_num_convert = pd.to_numeric(df.iloc[:, 2], errors="coerce")
        validando_inteiro = valores_num_convert.isna().any()
        apenas_inteiros = (
            df.iloc[:, 2].dropna().apply(lambda x: isinstance(x, int)).all()
        )
        validacao_final = ~((~apenas_inteiros) | validando_inteiro.any())
        assert (
            validacao_final
        ), 'ERRO: existe um valor não númerico ou não inteiro na coluna "Quantidade"'

        return True
