import numpy as np

def verificaIndices(x, y,bfs):
    for temp in bfs:
        if temp[0] == (x, y):
            return False
        
    return True

def get_us_and_vs(bfs, custos):
    us = [None] * len(custos)
    vs = [None] * len(custos[0])
    us[0] = 0
    bfs_copy = bfs.copy()
    while len(bfs_copy) > 0:
        for index, bv in enumerate(bfs_copy):
            i, j = bv[0]
            if us[i] is None and vs[j] is None:
                r = 0
                for index, bv in enumerate(bfs_copy):
                    a,b = bv[0]
                    if us[a] is not None or vs[b] is not None:
                        r = 1
                if r == 0:
                    if(i+1<len(custos)):
                        us[i+1] = 0
                        vs[j] = custos[i+1][j]
                        bfs_copy.append(((i+1, j),0))
                        bfs.append(((i+1, j),0))
                    elif(i-1>0):
                        us[i-1] = 0
                        vs[j] = custos[i-1][j]
                        bfs_copy.append(((i-1, j),0))
                        bfs.append(((i-1, j),0))
                r = 0 
                continue   
            custo = custos[i][j]
            if us[i] is None:
                us[i] = custo - vs[j]
            else: 
                vs[j] = custo - us[i]
            bfs_copy.pop(index)
            break
            
    return us, vs 

def get_ws(bfs, custos, us, vs):
    ws = []
    for i, linha in enumerate(custos):
        for j, custo in enumerate(linha):
            non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
            if non_basic:
                ws.append(((i, j), us[i] + vs[j] - custo))
    
    return ws 

def can_be_improved(ws):
    for p, v in ws:
        if v > 0: return True
    return False

def get_entering_variable_position(ws):
    ws_copy = ws.copy()
    ws_copy.sort(key=lambda w: w[1])
    return ws_copy[-1][0]

def get_possible_next_nodes(loop, not_visited):
    last_node = loop[-1]
    nodes_in_linha = [n for n in not_visited if n[0] == last_node[0]]
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
    if len(loop) < 2:
        return nodes_in_linha + nodes_in_column
    else:
        prev_node = loop[-2]
        linha_move = prev_node[0] == last_node[0]
        if linha_move: return nodes_in_column
        return nodes_in_linha

def get_loop(bv_positions, ev_position):
    def inner(loop):
        if len(loop) > 3:
            can_be_closed = len(get_possible_next_nodes(loop, [ev_position])) == 1
            if can_be_closed: return loop
        
        not_visited = list(set(bv_positions) - set(loop))
        possible_next_nodes = get_possible_next_nodes(loop, not_visited)
        for next_node in possible_next_nodes:
            new_loop = inner(loop + [next_node])
            if new_loop: return new_loop
    
    return inner([ev_position])

def loop_pivoting(bfs, loop):
    even_cells = loop[0::2]
    odd_cells = loop[1::2]
    get_bv = lambda pos: next(v for p, v in bfs if p == pos)
    leaving_position = sorted(odd_cells, key=get_bv)[0]
    leaving_value = get_bv(leaving_position)
    
    new_bfs = []
    for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]:
        if p in even_cells:
            v += leaving_value
        elif p in odd_cells:
            v -= leaving_value
        new_bfs.append((p, v))
        
    return new_bfs

def transportation_simplex_method(custos, bfs):
    def inner(bfs):
        us, vs = get_us_and_vs(bfs, custos)
        ws = get_ws(bfs, custos, us, vs)
        if can_be_improved(ws):
            ev_position = get_entering_variable_position(ws)
            loop = get_loop([p for p, v in bfs], ev_position)
            return inner(loop_pivoting(bfs, loop))
        return bfs
    
    variaveis_basicas = inner(bfs)
    solucao = np.zeros((len(custos), len(custos[0])))
    for (i, j), v in variaveis_basicas:
        solucao[i][j] = v

    return solucao

def get_custo_total(custos, solucao):
    custo_total = 0
    for i, linha in enumerate(custos):
        for j, custo in enumerate(linha):
            custo_total += custo * solucao[i][j]
    return custo_total