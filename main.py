from ui.menus import menuPrincipal
import sys

if __name__ == "__main__":
    try:
        menuPrincipal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)