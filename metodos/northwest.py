def noroeste(custos, oferta, demanda):
    ans = 0
    linha = 0 
    coluna = 0
    bfs = []
    while(linha != len(custos) and coluna != len(custos[0])):

        if(oferta[linha] <= demanda[coluna]):
            ans += oferta[linha] * custos[linha][coluna]
            demanda[coluna] -= oferta[linha]
            bfs.append(((linha, coluna), oferta[linha]))
            linha += 1
        else:
            ans += demanda[coluna] * custos[linha][coluna]
            oferta[linha] -= demanda[coluna]
            bfs.append(((linha, coluna), demanda[coluna]))
            coluna += 1 
    return ans, bfs
    
