def numero_mas_frecuente(lista):
    max_frecuencia = 0
    resultado = None

    for num in lista:
        frecuencia_actual = lista.count(num)

        if frecuencia_actual > max_frecuencia:
            max_frecuencia = frecuencia_actual
            resultado = num
        elif frecuencia_actual == max_frecuencia:
            if num < resultado:
                resultado = num

    return resultado


print(numero_mas_frecuente([1, 3, 1, 3, 2, 1]))  
print(numero_mas_frecuente([4, 4, 5, 5]))        
