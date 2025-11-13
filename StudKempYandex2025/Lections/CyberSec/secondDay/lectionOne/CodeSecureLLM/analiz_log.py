import pandas as pd 

logs = pd.read_csv('llm_audit.log', sep = '|', names = ['Time', 'IP', 'Prompt', 'Response'])
suspictious = logs[logs['Prompt'].str.contains('взломать|пароль', case = False)]

print(suspictious)
