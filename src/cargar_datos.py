from db import init_db, add_item


def cargar_datos():
    init_db()

   
    add_item(
        title="Vikings",
        type_="serie",
        year=2013,
        synopsis="Saga de guerreros nórdicos liderados por Ragnar Lothbrok.",
        hints=[("Ragnar es protagonista", 5), ("Ambientada en Escandinavia", 5), ("Guerreros y barcos vikingos", 5)]
    )

    add_item(
        title="Peaky Blinders",
        type_="serie",
        year=2013,
        synopsis="Crónica de la familia Shelby y su banda criminal en Birmingham.",
        hints=[("Familia Shelby", 5), ("Ambientada en Birmingham", 5), ("Gánsters con gorras planas", 5)]
    )

    add_item(
        title="The Boys",
        type_="serie",
        year=2019,
        synopsis="Un grupo busca derribar a superhéroes corruptos.",
        hints=[("Superhéroes corruptos", 5), ("Basado en un cómic", 5), ("Grupo llamado The Boys", 5)]
    )

    add_item(
        title="The Mandalorian",
        type_="serie",
        year=2019,
        synopsis="Un cazarrecompensas viaja por la galaxia en el universo Star Wars.",
        hints=[("Cazarrecompensas solitario", 5), ("Baby Yoda", 5), ("Ambientada en Star Wars", 5)]
    )

    add_item(
        title="Breaking Bad",
        type_="serie",
        year=2008,
        synopsis="Un profesor de química se convierte en fabricante de metanfetamina.",
        hints=[("Profesor de química", 5), ("Metanfetamina", 5), ("Walter White", 5)]
    )

    # ----- PELÍCULAS -----
    add_item(
        title="Avengers Endgame",
        type_="pelicula",
        year=2019,
        synopsis="Los Vengadores intentan revertir los daños causados por Thanos.",
        hints=[("Thanos aparece", 5), ("Los Vengadores luchan juntos", 5), ("Final épico del MCU", 5)]
    )

    add_item(
        title="Pulp Fiction",
        type_="pelicula",
        year=1994,
        synopsis="Historias entrelazadas de criminales en Los Ángeles.",
        hints=[("Dirigida por Quentin Tarantino", 5), ("Cafetería y baile famoso", 5), ("Historias entrelazadas", 5)]
    )

    add_item(
        title="Dune",
        type_="pelicula",
        year=2021,
        synopsis="Un joven noble debe proteger a su familia y su planeta desértico.",
        hints=[("Planeta desértico Arrakis", 5), ("Especia valiosa", 5), ("Paul Atreides es protagonista", 5)]
    )

    add_item(
        title="Star Wars 3",
        type_="pelicula",
        year=2005,
        synopsis="La caída de Anakin Skywalker y la ascensión de Darth Vader.",
        hints=[("Anakin Skywalker", 5), ("Darth Vader", 5), ("La Orden 66", 5)]
    )

    add_item(
        title="Blade Runner 2049",
        type_="pelicula",
        year=2017,
        synopsis="Un nuevo blade runner descubre secretos que podrían cambiar la sociedad.",
        hints=[("Ambientada en el futuro", 5), ("Replicantes", 5), ("Detective K", 5)]
    )


if __name__ == "__main__":
    cargar_datos()
