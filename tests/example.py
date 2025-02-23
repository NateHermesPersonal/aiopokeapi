# import sys
import asyncio
import aiopoke
import re
# sys.path.append('C:/Users/nated/Documents/Github/aiopokeapi/src/aiopoke')

async def old():
    client = aiopoke.AiopokeClient()
    move = await client.get_move(13)
    print(f"{move.name}")
#    pokemon = await client.get_pokemon(25)
#    print(f"{pokemon.name}")
    await client.close()


async def samples():
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
        # move = await client.get_move(867) # TypeError: aiopoke.utils.minimal_resources.Url() argument after ** must be a mapping, not NoneType (https://pokeapi.co/api/v2/move/doodle)
        print(f"{move}")
        while not finished:
            try:
                generation = await client.get_generation(gen)
                # print(f"{generation.version_groups}")
                # print(f"{generation.main_region}")
                new = len(generation.pokemon_species)
                for ability in generation.abilities:
                    abilities.append(ability.name)
                    # abilities.append(ability.id)
                    # abilities.append(f"{ability.name}({ability.id})")
                for move in generation.moves:
                    if not re.search("(special|physical)", move.name): # remove Z moves
                        moves.append(move.name)
                        # moves.append(move.id)
                        # moves.append(f"{move.name}({move.id})")
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

async def write_moves():
    async with aiopoke.AiopokeClient() as client:
        gen = 1
        moves = []
        finished = False
        while not finished:
            try:
                generation = await client.get_generation(gen)
                for move in generation.moves:
                    # moves.append(f"{move.name}")
                    # moves.append(f"{move.id}")
                    # moves.append(move)
                    # dict = move.learned_by_pokemon
                    moves.append(f"{move.id}")
                    # print(f"{dict}")
                gen += 1
            except Exception as e:
                finished = True
        with open("output/movesByGen.txt", "w") as moveFile:
            moveFile.write("\n".join(moves))
        return moves

async def read_moves(movesList=None):
    async with aiopoke.AiopokeClient() as client:
        if not movesList:
            with open("output/movesByGen.txt", "r") as moveFile:
                moves = moveFile.read().splitlines()
        else:
            moves = movesList
        print(len(moves))
        issueMoves = []
        issues = 0
        # tasks = [client.get_move(move) for move in moves]
        # results = await asyncio.gather(*tasks)
        for move in moves:
            try:
                await client.get_move(move)
                issueMoves.append(move)
                # print(f"{move.name}")
            except Exception as e:
                # print(f"Exception {e}")
                # issueMoves.append(move)
                issueMoves.append(f"Issue with move {move}")
                issues += 1
        # with open("output/movesWithIssues_names.txt", "w") as moveFile:
        with open("output/movesWithIssues.txt", "w") as moveFile:
            moveFile.write("\n".join(issueMoves))
        print(issues)

async def tests():
    async with aiopoke.AiopokeClient() as client:
        # gen = 1
        # moves = []
        # finished = False
        # while not finished:
        #     try:
        #         generation = await client.get_generation(gen)
        #         for move in generation.moves:
        #             # moves.append(f"{move.name}")
        #             # moves.append(f"{move.id}")
        #             # moves.append(move)
        #             # dict = move.learned_by_pokemon
        #             moves.append(move.name)
        #             # print(f"{dict}")
        #         gen += 1
        #     except Exception as e:
        #         finished = True
        # tasks = [client.get_move(move) for move in moves]
        # results = await asyncio.gather(*tasks)
        # for r in results:
        #     print (f"{r.name}")
        # move = await client.get_move(13)
        # print(f"{move.name}")
        move = await client.get_move(407)
        print(f"{move.name}")
        # move = await client.get_move("pound")
        # move = await client.get_move("thrash")


# asyncio.run(samples())
# moves = asyncio.run(write_moves())
# asyncio.run(read_moves(moves))
# asyncio.run(old())

# asyncio.run(write_moves())
# asyncio.run(read_moves())

asyncio.run(tests())