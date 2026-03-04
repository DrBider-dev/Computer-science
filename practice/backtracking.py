def combinaciones(n):
    solucion = []

    def backtrack():
        if len(solucion) == n:
            print("".join(solucion))
            return
        
        for opcion in ["0", "1"]:
            
            solucion.append(opcion)
            
            backtrack()
            
            solucion.pop()   # ← BACKTRACK REAL
    
    backtrack()