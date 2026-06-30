scoreboard players add $tick gigani_tps 1
execute if score $tick gigani_tps matches 1200.. run scoreboard players set $tick gigani_tps 0

scoreboard players remove $c2 gigani_tps 1
execute if score $c2 gigani_tps matches ..0 run function gigani_tps:tick_2
execute if score $c2 gigani_tps matches ..0 run scoreboard players set $c2 gigani_tps 2

scoreboard players remove $c5 gigani_tps 1
execute if score $c5 gigani_tps matches ..0 run function gigani_tps:tick_5
execute if score $c5 gigani_tps matches ..0 run scoreboard players set $c5 gigani_tps 5

scoreboard players remove $c10 gigani_tps 1
execute if score $c10 gigani_tps matches ..0 run function gigani_tps:tick_10
execute if score $c10 gigani_tps matches ..0 run scoreboard players set $c10 gigani_tps 10

scoreboard players remove $c20 gigani_tps 1
execute if score $c20 gigani_tps matches ..0 run function gigani_tps:tick_20
execute if score $c20 gigani_tps matches ..0 run scoreboard players set $c20 gigani_tps 20
