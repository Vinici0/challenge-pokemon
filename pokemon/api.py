import requests
import time
import requests

class PokemonDataFetcher:
    """
    Clase encargada de obtener datos básicos del Pokémon desde la PokeAPI.

    Attributes:
        pk_name (str): El nombre del Pokémon.
        pokemon_json (dict): Datos JSON obtenidos de la PokeAPI.
    """
    def __init__(self, pk_name: str) -> None:
        """
        Inicializa una nueva instancia de PokemonDataFetcher.

        Args:
            pk_name (str): El nombre del Pokémon.
        """
        self.pk_name = pk_name
        self.pokemon_json = requests.get(
            f'https://pokeapi.co/api/v2/pokemon/{pk_name.lower()}'
        ).json()

    def get_pokemon_data(self) -> dict:
        """
        Obtiene los datos básicos del Pokémon.

        Returns:
            dict: Datos básicos del Pokémon en formato JSON.
        """
        return self.pokemon_json


class PokemonParser:
    """
    Clase encargada de analizar y extraer información específica de los datos del Pokémon.

    Attributes:
        pokemon_data (dict): Datos básicos del Pokémon en formato JSON.
    """
    def __init__(self, pokemon_data: dict) -> None:
        """
        Inicializa una nueva instancia de PokemonParser.

        Args:
            pokemon_data (dict): Datos básicos del Pokémon en formato JSON.
        """
        self.pokemon_data = pokemon_data

    def parse_pokemon_moves(self) -> list:
        """
        Analiza y devuelve la lista de movimientos del Pokémon.

        Returns:
            list: Lista de movimientos del Pokémon.
        """
        moves = []
        for move in self.pokemon_data["moves"]:
            move_data = requests.get(move["move"]["url"]).json()
            moves.append({
                "name": move["move"]["name"],
                "description": move_data["flavor_text_entries"][0]["flavor_text"].replace(
                    "\n", " "
                ).capitalize(),
                "accuracy": move_data["accuracy"],
                "dmg_type": move_data["damage_class"]["name"],
            })
        return moves

    def parse_pokemon_types(self) -> list:
        """
        Analiza y devuelve la lista de tipos del Pokémon.

        Returns:
            list: Lista de tipos del Pokémon.
        """
        types = []
        for slot in self.pokemon_data["types"]:
            types.append(slot["type"]["name"].title())
        return types

    def parse_pokemon_stats(self) -> dict:
        """
        Analiza y devuelve las estadísticas del Pokémon.

        Returns:
            dict: Estadísticas del Pokémon en formato de diccionario.
        """
        stats = {}
        for stat in self.pokemon_data["stats"]:
            stats[stat["stat"]["name"]] = stat["base_stat"]
        return stats

    def parse_pokemon_abilities(self) -> list:
        """
        Analiza y devuelve la lista de habilidades del Pokémon.

        Returns:
            list: Lista de habilidades del Pokémon.
        """
        abilities = []
        for ability in self.pokemon_data["abilities"]:
            abilities.append(ability["ability"]["name"].title())
        return abilities

    def parse_pokemon_game_version(self) -> int:
        """
        Analiza y devuelve la versión del juego en la que aparece el Pokémon.

        Returns:
            int: Índice de la versión del juego.
        """
        for version in self.pokemon_data["game_indices"]:
            if version["version"]["name"] in ["diamond", "black"]:
                return version["game_index"]


class Pokemon:
    """
    Clase principal que encapsula la lógica del Pokémon.

    Attributes:
        pk_name (str): El nombre del Pokémon.
        data_fetcher (PokemonDataFetcher): Instancia de PokemonDataFetcher.
        parser (PokemonParser): Instancia de PokemonParser.
    """
    def __init__(self, pk_name: str) -> None:
        """
        Inicializa una nueva instancia de Pokemon.

        Args:
            pk_name (str): El nombre del Pokémon.
        """
        self.pk_name = pk_name
        self.data_fetcher = PokemonDataFetcher(pk_name)
        self.parser = PokemonParser(self.data_fetcher.get_pokemon_data())

    def get_moves(self) -> list:
        """
        Obtiene y devuelve la lista de movimientos del Pokémon.

        Returns:
            list: Lista de movimientos del Pokémon.
        """
        return self.parser.parse_pokemon_moves()

    def get_types(self) -> list:
        """
        Obtiene y devuelve la lista de tipos del Pokémon.

        Returns:
            list: Lista de tipos del Pokémon.
        """
        return self.parser.parse_pokemon_types()

    def get_stats(self) -> dict:
        """
        Obtiene y devuelve las estadísticas del Pokémon.

        Returns:
            dict: Estadísticas del Pokémon en formato de diccionario.
        """
        return self.parser.parse_pokemon_stats()

    def get_abilities(self) -> list:
        """
        Obtiene y devuelve la lista de habilidades del Pokémon.

        Returns:
            list: Lista de habilidades del Pokémon.
        """
        return self.parser.parse_pokemon_abilities()

    def get_game_version(self) -> int:
        """
        Obtiene y devuelve la versión del juego en la que aparece el Pokémon.

        Returns:
            int: Índice de la versión del juego.
        """
        return self.parser.parse_pokemon_game_version()


# Ejemplo de uso
x = Pokemon("pikachu")
print(type(x.get_game_version()))
