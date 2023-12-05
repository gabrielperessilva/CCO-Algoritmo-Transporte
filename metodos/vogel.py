INF = 10**5
def findDiff(custos):
    linhaDiff = []
    colunaDiff = []
    for i in range(len(custos)):
        arr = custos[i][:]
        arr.sort()
        linhaDiff.append(arr[1]-arr[0])
    coluna = 0
    while coluna < len(custos[0]):
        arr = []
        for i in range(len(custos)):
            arr.append(custos[i][coluna])
        arr.sort()
        coluna += 1
        colunaDiff.append(arr[1]-arr[0])
    return linhaDiff, colunaDiff

def vogel(custos, oferta, demanda):
    
    n = len(custos)
    m = len(custos[0])
    ans = 0
    bfs = []
    while max(oferta) != 0 or max(demanda) != 0:
        linha, coluna = findDiff(custos)
        maxi1 = max(linha)
        maxi2 = max(coluna)
    
        if(maxi1 >= maxi2):
            for ind, val in enumerate(linha):
                if(val == maxi1):
                    mini1 = min(custos[ind])
                    for ind2, val2 in enumerate(custos[ind]):
                        if(val2 == mini1):
                            mini2 = min(oferta[ind], demanda[ind2])
                            bfs.append(((ind, ind2), mini2))
                            ans += mini2 * mini1
                            oferta[ind] -= mini2
                            demanda[ind2] -= mini2
                            if(demanda[ind2] == 0):
                                for r in range(n):
                                    custos[r][ind2] = INF
                            else:
                                custos[ind] = [INF for i in range(m)]
                            break
                    break
            
        else:
            for ind, val in enumerate(coluna):
                if(val == maxi2):
                    mini1 = INF
                    for j in range(n):
                        mini1 = min(mini1, custos[j][ind])
    
                    for ind2 in range(n):
                        val2 = custos[ind2][ind]
                        if val2 == mini1:
                            mini2 = min(oferta[ind2], demanda[ind])
                            bfs.append(((ind2, ind), mini2))
                            ans += mini2 * mini1
                            oferta[ind2] -= mini2
                            demanda[ind] -= mini2
                            if(demanda[ind] == 0):
                                for r in range(n):
                                    custos[r][ind] = INF
                            else:
                                custos[ind2] = [INF for i in range(m)]
                            break
                    break
    return ans, bfs
