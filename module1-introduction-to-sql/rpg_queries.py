import os
import sqlite3

Database_filepath = os.path.join(os.path.dirname(
                                 __file__),'rpg_db.sqlite3')

connection = sqlite3.connect(Database_filepath)

cursor = connection.cursor()


# how many characters are there 
# 302
query_one = "Select count(distinct character_id) as character_count from charactercreator_character"

num_characters = cursor.execute(query_one).fetchall()
print("--------------------------------------------------")
for row in num_characters:
    print(num_characters)

# how many of each specific subclass 
# subclasses: mage (necromancer), thief, cleric, fighter
# mage 108
# thief 51 
# fighter 68
# cleric 75 
# necromancy 11 
query_two = """
            SELECT
                count(distinct charactercreator_mage.character_ptr_id) as mage_counts
	            , count(distinct charactercreator_thief.character_ptr_id) as thief_counts
	            , count(distinct charactercreator_fighter.character_ptr_id) as fighter_counts
	            , count(distinct charactercreator_cleric.character_ptr_id) as cleric_counts
	            , count(distinct charactercreator_necromancer.mage_ptr_id) as necromancer_counts
            FROM charactercreator_mage, charactercreator_thief, charactercreator_cleric, 
                 charactercreator_fighter, charactercreator_necromancer
             """

subclass_totals = cursor.execute(query_two).fetchall()
print("--------------------------------------------------")
for row in subclass_totals:
    print(subclass_totals)

# how many total items 
# 174
query_three = "SELECT count(distinct item_id) as item_count from armory_item"

total_items = cursor.execute(query_three).fetchall()
print("--------------------------------------------------")
for row in total_items:
    print(total_items)

# how many of the items are weapons 37
# how many are not total items(174) - weapons(37) 
query_four = """
            SELECT count(distinct item_ptr_id) as weapon_count
	              , count (distinct armory_item.item_id) - count(distinct item_ptr_id) as NonWeapon_Item
	        from armory_weapon, armory_item
            """
	
distinction = cursor.execute(query_four).fetchall()
print("--------------------------------------------------")
for row in distinction:
    print(distinction)

# how many items does each character have? return first 20 rows
query_five = """
            SELECT character_id, count(distinct item_id) as item_count 
            from charactercreator_character_inventory
                group by character_id 
            LIMIT 20
             """

character_items = cursor.execute(query_five).fetchall()
print("--------------------------------------------------")
for row in character_items:
    print(character_items)

# how many weapons does each character have? limit 20
# need to do a join on armory item, armory weapon and character inventory
# distinct count on item id in weapons
query_six = """
            SELECT charactercreator_character_inventory.character_id
                   , count(distinct armory_weapon.item_ptr_id) as weapon_count
            FROM armory_weapon
            JOIN  charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
            JOIN armory_item on armory_item.item_id = armory_weapon.item_ptr_id
                group by charactercreator_character_inventory.character_id
            LIMIT 20
            """
character_weapons = cursor.execute(query_six).fetchall()
print("--------------------------------------------------")
for row in character_weapons:
    print(character_weapons)

#average weapon count for each character 1.3096
# average item count for each character 1.3096
query_seven = """
              SELECT Avg(weapon_count), Avg(item_count)
                from (
                    SELECT charactercreator_character_inventory.character_id
                           , count(distinct armory_weapon.item_ptr_id) as weapon_count
                           , count(distinct charactercreator_character_inventory.item_id) as item_count
                    FROM armory_weapon
                    JOIN  charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
                    JOIN armory_item on armory_item.item_id = armory_weapon.item_ptr_id
                    group by charactercreator_character_inventory.character_id
                    )
              """
averages = cursor.execute(query_seven).fetchall()
print("--------------------------------------------------")
for row in averages:
    print(averages)
print("--------------------------------------------------")
                    