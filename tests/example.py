import asyncio
import aiopoke

# async def main():
#    client = aiopoke.AiopokeClient()
#    pokemon = await client.get_pokemon(25)
#    print(f"{pokemon.name}")

#    await client.close()

async def main():
    async with aiopoke.AiopokeClient() as client:
        pokemon = await client.get_pokemon(25)
        print(f"{pokemon.name}")
        print(f"{len(pokemon.forms)}")

        species = await client.get_pokemon_species(25)
        print(species.name)
        print(f"{len(species.varieties)}")

        generation = await client.get_generation(9)
        print(f"{generation.version_groups}")
        print(f"{generation.main_region}")
        print(f"{generation.name}")

        gen = 1
        total = 0
        finished = False
        while not finished:
            try:
                generation = await client.get_generation(gen)
                new = len(generation.pokemon_species)
                print(f"{generation.name} added {new} new Pokemon")
                total += new
                gen += 1
            except Exception as e:
                # print(f"{e}")
                finished = True
        print(f"{total} total Pokemon")


asyncio.run(main())