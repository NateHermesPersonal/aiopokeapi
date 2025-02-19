import asyncio
import aiopoke
import re

# async def main():
#    client = aiopoke.AiopokeClient()
#    pokemon = await client.get_pokemon(25)
#    print(f"{pokemon.name}")

#    await client.close()


async def main():
    async with aiopoke.AiopokeClient() as client:
        # pokemon = await client.get_pokemon(25)
        # print(f"{pokemon.name}")
        # print(f"{len(pokemon.forms)}")

        # species = await client.get_pokemon_species(25)
        # print(species.name)
        # print(f"{len(species.varieties)}")

        gen = 1
        total = 0
        abilities = []
        moves = []
        finished = False
        # move = await client.get_move("eruption") # works, prints 284 (https://pokeapi.co/api/v2/move/eruption)
        # move = await client.get_move("doodle") # TypeError: aiopoke.utils.minimal_resources.Url() argument after ** must be a mapping, not NoneType (https://pokeapi.co/api/v2/move/doodle)
        # print(f"{move.id}")
        while not finished:
            try:
                generation = await client.get_generation(gen)
                # print(f"{generation.version_groups}")
                # print(f"{generation.main_region}")
                new = len(generation.pokemon_species)
                for ability in generation.abilities:
                    # abilities.append(f"{ability.name}({ability.id})")
                    abilities.append(ability.name)
                for move in generation.moves:
                    if not re.search("(special|physical)", move.name): # remove Z moves
                        # moves.append(f"{move.name}({move.id})")
                        moves.append(move.name)
                print(f"{generation.name} added {new} new Pokemon")
                total += new
                gen += 1
            except Exception as e:
                finished = True
        print(f"{total} total Pokemon")

        abilities.sort() # Alphabetize
        list(dict.fromkeys(abilities)) # Remove duplicates (efficient and preserves order)
        with open("output/abilities.txt", "w") as abilityFile:
            abilityFile.write("\n".join(abilities))
        
        moves.sort()
        list(dict.fromkeys(moves))
        with open("output/moves.txt", "w") as moveFile:
            moveFile.write("\n".join(moves))

asyncio.run(main())