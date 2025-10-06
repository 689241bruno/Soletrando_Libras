
palavra_escolhida = str(input("Digite uma palavra")).upper()
palavra = []

for letra in palavra_escolhida:
    sinal = str(input("letra: ")).upper()
    if sinal == letra:
        resposta = "correta"
    else:
        resposta = "incorrta"
    print(f" {sinal} <-> {letra} --> {resposta}")
    print('------')

    


