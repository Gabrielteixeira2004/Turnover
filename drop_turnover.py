#!/usr/bin/env python
# coding: utf-8

# In[10]:


def drop_turnover(df):
    '''
    Código situacao, codsituacao and situacao: Not relevant to the analysis as
    it does not show situation history and possible data leakage.
    datademissao: Only used to filter.
    Data Leakage: motivo_desligamento, tipo_desligamento_classificação,
    tipo_desligamento
    integrada: Only used to filter.
    tipo_função: Only used to filter.
    codsecao: contagion function.
    codsecao_gerencia: contagion function.
    codsecao_gerencia_group_contagion: contagion function.
    funcao_descricao: contagion function.
    funcao_descricao_clean: contagion function.
    funcao_descricao_clean_group_contagion: contagion function.
    '''

    drop_feature = ['codigo_situacao', 'codsituacao', 'situacao',
                    'datademissao', 'motivo_desligamento',
                    'tipo_desligamento_classificação', 'tipo_desligamento',
                    'integrada', 'codsecao', 'tipo_função',
                    'funcao_descricao', 'codsecao_gerencia',
                    'funcao_descricao_clean', 'codsecao_gerencia_group_contagion',
                    'funcao_descricao_clean_group_contagion']

    '''
    Unique records and high cardinality features

    '''

    registros_unicos = [
                        'codpessoa',
                        'nome',
                        'chave_coligada_chapa'
                        ]

    alta_cardinalidade = ['codcoligada',
                          'filial_cidade',
                          'codsindicato',
                          'residencia_cidade',
                          'residencia_estado',
                          'escolaridade_descricao',
                          'Residência',
                          'Filial',
                          'nome_sindicato',
                          'nome_sindicato_abreviado',
                          'setor',
                          'VP',
                          'filial_estado']

    '''
    tipo_colaborador_bertelsmann: Redundant, only contains CLT
    dataadmissao: Redundant when considering tempo de casa
    faixa_tempo_casa: Redundant when considering ord_faixa_tempo_casa
    faixa_etaria: Redundant when considering ord_faixa_etaria
    escolaridade_faixas : Redundant when considering escolaridade_classificação
    raiz_vp: Redundant when considering VP_descricao
    tempo_casa_anos: Redudant when considering tempo de casa
    codregional and regional: Does not offer a better structure perspective
    '''

    especial = [
        'tipo_colaborador_bertelsmann',
        'faixa_tempo_casa',
        'faixa_etaria',
        'escolaridade_faixas',
        'dataadmissao',
        'raiz_vp',
        'tempo_casa_anos',
        'codregional',
        'regional']

    df1 = df.drop(
        drop_feature + registros_unicos + alta_cardinalidade + especial, axis=1
    )

    return df1