# resolver bug de logica da busca de salario
# resolver problema de coversao indeed
# resolver recaptcha
# resolver duplicidade de valores

# implementar time de busca
# implementar padrão de envio no wpp


# Tempo de execução do código 1° tentativa: 2m 19seg Sucesso (Indefinida - O teste da segunda execução apresentou um tempo maior, e parou na metade)
# Obs: Retornou todos os dados, menos o salário devido ao Recaptcha. Não executou o envio das msgs

# Tempo de execução do código 2° tentativa: 2m 50seg Erro
# Obs: Após tentativas posterirores a 1°, o código retornou a planilha em branco. O erro foi identificado no try/except trecho que identifica a caixa a
# do busca_salario. Todo o código, estava passando diretamente para o except, devido a um erro não identificado, mas possivelmente um TypeError, e retornando
# None. Foi removido o trecho do código try/except, entretanto, após algum tempo de execução o erro TypeError, retornou.

# Tempo de execução do código 3° tentativa: 3m 51seg Sucesso
# Obs: Retornou todos os dados, menos o salário devido a diversos erros (argument of type 'TypeError' is not iterable, Não localizada informações salariais).
# Executou o pseudo envio de mensagens.

# Tempo de execução do código 4° tentativa: 30 seg Erro
# Obs: Não houve qualquer especie de retorno, o código falhou na tratativa de erro na função buscar_salario. ERRO RECORRENTE