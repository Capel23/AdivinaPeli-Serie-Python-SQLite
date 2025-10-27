from src.db import init_db
from src.ui import App

def main():
    init_db()  # Inicializa la base de datos
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
