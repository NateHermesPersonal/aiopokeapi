# import sys
import asyncio
import aiopoke
import re
# sys.path.append('C:/Users/nated/Documents/Github/aiopokeapi/src/aiopoke')

types = ["Normal",
        "Fire",
        "fighting",
        "Water",
        "Flying",
        "Grass",
        "Poison",
        "Electric",
        "Ground",
        "Psychic",
        "Rock",
        "Ice",
        "Bug",
        "Dragon",
        "Ghost",
        "Dark",
        "Steel",
        "Fairy"]

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
                    # abilities.append(ability.name)
                    # abilities.append(ability.id)
                    abilities.append(f"{ability.name}({ability.id})")
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

async def write_abilities():
    async with aiopoke.AiopokeClient() as client:
        gen = 1
        abilities = []
        finished = False
        while not finished:
            try:
                generation = await client.get_generation(gen)
                for ability in generation.abilities:
                    # moves.append(f"{move.name}")
                    # moves.append(f"{move.id}")
                    # moves.append(move)
                    # dict = move.learned_by_pokemon
                    abilities.append(f"{ability.name}")
                gen += 1
            except Exception as e:
                finished = True
            abilities.sort() # Alphabetize
        with open("output/abilitiesByGen.txt", "w") as abilityFile:
            abilityFile.write("\n".join(abilities))
        return abilities

async def read_missing_moves():
    async with aiopoke.AiopokeClient() as client:
        missingMoveDict = {}
        missingMoves = []
        with open("input/missing_moves.txt", "r") as moveFile:
            missingMoves = moveFile.read().splitlines()
        tasks = [client.get_move(m) for m in missingMoves]
        results = await asyncio.gather(*tasks)
        uniqueMons = {}
        for result in results:
            pokemon = []
            for p in result.learned_by_pokemon:
                if f"{p.name}" in missingMoveDict:
                    missingMoveDict[p.name].append(result.name)
                else:
                    missingMoveDict[p.name] = []
                    missingMoveDict[p.name].append(result.name)
                pokemon.append(p.name)
            if len(pokemon) == 1:
                name = pokemon[0]
                print(f"{result.name} - {len(pokemon)} Pokemon with this gen {result.generation.id} move ({name})")
                if name not in uniqueMons:
                    uniqueMons[name] = []
                uniqueMons[name].append(result.name)
        for mon in uniqueMons.keys():
            if len(uniqueMons[mon]) > 1:
                print(f"{mon} has multiple unique moves ({uniqueMons[mon]})")
            # if len(pokemon) == 0:
            #     print(f"{result.name} - {len(pokemon)} Pokemon with this gen {result.generation.id} move")
        # print(f"{len(missingMoveDict.keys())}")
        # print(f"{missingMoveDict["mew"]} ({len(missingMoveDict["mew"])})")
        # for pok in missingMoveDict.keys():
        #     print(f"{pok} {len(missingMoveDict[pok])}")
        # sortedMoves = dict(sorted(missingMoveDict.items(), key=lambda item: len(item[1])))
        sortedMoves = dict(sorted(missingMoveDict.items(), key=lambda item: len(item[1]), reverse=True))
        # for pok in sortedMoves.keys():
        #     print(f"{pok} {len(sortedMoves[pok])}")
        efficientDict = {} # FIXME consider that pokemon can have 4 moves, go through whole dictionary to see if move can go to a Pokemon with less than 4??  Want to do this before efficientDict?
        print(f"{len(missingMoves)} missing moves")
        with open("output/sortedMoveDict.txt", "w") as sortedMoveFile:
            for m in missingMoves:
                for pok in sortedMoves.keys():
                    if m in sortedMoves[pok]:
                        sortedMoveFile.write(f"{m} - {pok}\n")
                        if pok in efficientDict:
                            efficientDict[pok].append(m)
                        else:
                            efficientDict[pok] = []
                            efficientDict[pok].append(m)
                        break
                else:
                    sortedMoveFile.write(f"Could not find Pokemon for move {m}\n")
                    print(f"Could not find Pokemon for move {m}")
        # print(f"{efficientDict["mew"]}")
        # for mon in efficientDict.keys():
        #     if len(efficientDict[mon]) >=4:
        #         print(f"{mon} can learn {len(efficientDict[mon])} moves")
        #     print(f"{mon} - {",".join(efficientDict[mon])}")
        
async def read_missing_abilities():
    async with aiopoke.AiopokeClient() as client:
        missingAbilities = []
        with open("input/missing_abilities_13.txt", "r") as abilityFile:
            missingAbilities = abilityFile.read().splitlines()
        # print(f"{len(missingAbilities)}")
        tasks = [client.get_ability(a) for a in missingAbilities]
        results = await asyncio.gather(*tasks)
        for result in results:
            pokemon = []
            for p in result.pokemon:
                pokemon.append(p.pokemon.name)
            print(f"{result.name} - {len(pokemon)} Pokemon with this ability {",".join(pokemon)}")

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
        tasks = [client.get_move(move) for move in moves]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(f"{r.name}") # works, prints all moves
        # for move in moves:
        #     try:
        #         await client.get_move(move)
        #         issueMoves.append(move)
        #         # print(f"{move.name}")
        #     except Exception as e:
        #         # print(f"Exception {e}")
        #         # issueMoves.append(move)
        #         issueMoves.append(f"Issue with move {move}")
        #         issues += 1
        # # with open("output/movesWithIssues_names.txt", "w") as moveFile:
        # with open("output/movesWithIssues.txt", "w") as moveFile:
        #     moveFile.write("\n".join(issueMoves))
        # print(issues)

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
        # move = await client.get_move(407)
        move = await client.get_move("ice-burn")
        # move = await client.get_move("behemoth-blade")
        # move = await client.get_move("hold-hands")
        print(f"{move.learned_by_pokemon}")

def select_type():
    selectedType = None
    while True:
        i = 0
        while(i < len(types)):
            print(f"{i} - {types[i]}")
            i += 1
        selectedType = input("Enter the number next to the type to search for\n")
        selectedType = int(selectedType)
        try:
            types[selectedType]
            break
        except:
            print("Invalid input, please enter a valid type")
    return selectedType

async def find_mons_of_type():
    async with aiopoke.AiopokeClient() as client:
        choice = select_type()
        choice2 = None
        while True:
            anotherType = input(f"Do you want to combine type {types[choice]} with another type? (y/n)\n")
            if anotherType == "y":
                choice2 = select_type()
                break
            elif anotherType == "n":
                break
            else:
                print("Invalid input, please enter 'y' or 'n'")
        choice = types[choice].lower()
        if choice2 and choice != choice2:
            choice2 = types[choice2].lower()
            print(f"Will search for combination of types {choice} and {choice2}")
        else:
            print(f"Will search for type {choice}")
        
        gen = 1
        pokemonSpecies = []
        while True:
            try:
                generation = await client.get_generation(gen)
                pokemonSpecies.extend( [species.id for species in generation.pokemon_species] )
                gen += 1
            except Exception as e:
                break
        
        tasks = [client.get_pokemon_species(s) for s in pokemonSpecies]
        speciesList = await asyncio.gather(*tasks)
        varietyList = []
        for s in speciesList:
            varietyList.extend( [v.pokemon.name for v in s.varieties] )
        tasks2 = [client.get_pokemon(v) for v in varietyList]
        pokemonList = await asyncio.gather(*tasks2)
        matches = []
        for pokemon in pokemonList:
            pokemonTypes = [type.type.name for type in pokemon.types]
            # print(f"Types for {pokemon.name}: {pokemonTypes}")
            if choice in pokemonTypes:
                if choice2:
                    if choice2 in pokemonTypes:
                        matches.append(pokemon.name)
                else:
                    matches.append(pokemon.name)
        print(f"The following pokemon match types {choice} and {choice2}: {matches}")

# asyncio.run(samples())
# moves = asyncio.run(write_moves())
# abilities = asyncio.run(write_abilities())
# asyncio.run(read_moves(moves))
# asyncio.run(old())

# asyncio.run(write_moves())
# asyncio.run(read_moves())

# asyncio.run(read_missing_moves())
# asyncio.run(read_missing_abilities())
asyncio.run(find_mons_of_type())

# asyncio.run(tests())