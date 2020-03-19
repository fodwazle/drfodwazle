import weapons as wpn
name = input("Please enter your name ").rstrip()
name += " "
for i in wpn.weapon_list:
  print(str(i))
#print("please choose your weapon:\n"+str(wpn.Claymore)+"\n"+str(wpn.Knife))
weapon = input()
try:
  weapon = int(weapon)
  weaponEquipped = wpn.weapon_list[weapon - 1]
except:
  weaponEquipped = wpn.weapon_list[0]
