def inputSeguro(mensaje):
    """
    Función segura para obtener entrada del usuario.
    Maneja interrupciones de teclado y entradas vacías.
    """
    try:
        valor = input(mensaje).strip()
        if valor == "":
            return None
        return valor
    except (KeyboardInterrupt, EOFError):
        print("\n✗ Entrada cancelada por el usuario.")
        return None


def confirmarAccion(mensaje="¿Confirmar? (S/N): "):
    """
    Solicita confirmación al usuario.
    Retorna True para 'S', False para 'N', None si se cancela.
    """
    while True:
        try:
            respuesta = input(mensaje).strip().upper()
            
            if respuesta == "":
                print("✗ No puede dejar este campo vacío. Ingrese S para confirmar o N para cancelar.")
                continue
            
            if respuesta == "S":
                return True
            elif respuesta == "N":
                return False
            else:
                print("✗ Opción inválida. Ingrese 'S' para SÍ o 'N' para NO.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n✗ Entrada cancelada por el usuario.")
            return None