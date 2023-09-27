import pandas as pd

# Ler o arquivo issues.csv com codificação UTF-8
input_file = 'issues.csv'
df = pd.read_csv(input_file, encoding='utf-8')

# Deletar as linhas em que a coluna "user" está vazia
df.dropna(subset=['user'], inplace=True)

# Verificar se a primeira coluna é "user" e, se for, converter todas as entradas em maiúsculas
if df.columns[0] == 'user':
    df['user'] = df['user'].str.upper()

# Ordenar as linhas em ordem alfabética com base na coluna "user"
df.sort_values(by='user', inplace=True)

# Adicionar 5 colunas extras após a coluna B
num_colunas_extra = 5
colunas_extra = ['Entrega', 'Atraso', 'Nota', 'OBS', 'Aula']  # Nomes das colunas extras

# Encontre o índice da coluna "url" (coluna B)
indice_coluna_url = df.columns.get_loc('url')

for i in range(num_colunas_extra):
    df.insert(indice_coluna_url + i + 1, colunas_extra[i], '')

# Inverter a ordem das colunas a partir da oitava coluna
colunas = list(df.columns)
colunas[7:] = colunas[7:][::-1]
df = df[colunas]

# Salvar os dados no arquivo gsheets.csv com codificação UTF-8
output_file = 'gsheets.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

print(f'Arquivo {output_file} criado com sucesso.')
