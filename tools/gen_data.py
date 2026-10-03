"""Generates blockstates, models, loot tables, tags, recipes, lang and worldgen JSON.
Re-run after editing: python3 tools/gen_data.py"""
import gzip
import json
import shutil
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "src/main/resources"
MOD = "mcflora"
A = ROOT / "assets" / MOD
D = ROOT / "data" / MOD


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def m(name):
    return f"{MOD}:{name}"


def tex(name):
    return f"{MOD}:block/{name}"


for sub in ("blockstates", "models"):
    shutil.rmtree(A / sub, ignore_errors=True)
for sub in ("loot_table", "recipe", "tags", "worldgen", "neoforge", "structure"):
    shutil.rmtree(D / sub, ignore_errors=True)
shutil.rmtree(ROOT / "data/minecraft/tags", ignore_errors=True)
shutil.rmtree(ROOT / "data/neoforge", ignore_errors=True)

# --------------------------------------------------------------------------- block catalogue

LICHENS = ["silver_lichen", "black_lichen", "brown_lichen", "rust_lichen"]
HANGING = ["old_mans_beard", "nepenthes"]
CROSS = ["reindeer_lichen", "arctic_poppy", "red_spider_lily", "blue_hydrangea", "pink_hydrangea", "birds_nest_fern"]
MOSS = {"frost_moss_block": "frost_moss_carpet", "sphagnum_moss_block": "sphagnum_moss_carpet"}
DOUBLE = ["cotton_grass", "bracken", "sasa_bamboo_grass", "japanese_iris", "monstera"]
LILY = ["lotus_pad", "lotus_flower"]
FLAT = ["rafflesia"]

NAMES = {
    "silver_lichen": "Silver Lichen", "black_lichen": "Black Lichen", "brown_lichen": "Brown Lichen",
    "rust_lichen": "Rust Lichen", "old_mans_beard": "Old Man's Beard", "reindeer_lichen": "Reindeer Lichen",
    "frost_moss_block": "Frost Moss Block", "frost_moss_carpet": "Frost Moss Carpet",
    "sphagnum_moss_block": "Sphagnum Moss Block", "sphagnum_moss_carpet": "Sphagnum Moss Carpet",
    "cotton_grass": "Cotton Grass", "arctic_poppy": "Arctic Poppy", "bracken": "Bracken",
    "sasa_bamboo_grass": "Sasa Bamboo Grass", "red_spider_lily": "Red Spider Lily", "japanese_iris": "Japanese Iris",
    "blue_hydrangea": "Blue Hydrangea", "pink_hydrangea": "Pink Hydrangea", "lotus_pad": "Lotus Pad",
    "lotus_flower": "Lotus Flower", "monstera": "Monstera", "birds_nest_fern": "Bird's Nest Fern",
    "nepenthes": "Nepenthes", "rafflesia": "Rafflesia",
}
ALL = list(NAMES)

CUTOUT = "minecraft:cutout"


def block_model(name, obj):
    write(A / "models/block" / f"{name}.json", obj)


def item_model(name, obj):
    write(A / "models/item" / f"{name}.json", obj)


def generated_item(name, texture):
    item_model(name, {"parent": "minecraft:item/generated", "textures": {"layer0": tex(texture)}})


def simple_state(name, model=None):
    write(A / "blockstates" / f"{name}.json", {"variants": {"": {"model": model or f"{MOD}:block/{name}"}}})


def cross(name, texture=None):
    block_model(name, {"parent": "minecraft:block/cross", "textures": {"cross": tex(texture or name)}, "render_type": CUTOUT})


# lichens: one flat face model rotated onto each side, as vanilla glow lichen does
FACES = {"north": {}, "south": {"y": 180}, "east": {"y": 90}, "west": {"y": 270}, "up": {"x": 270}, "down": {"x": 90}}
for name in LICHENS:
    block_model(name, {
        "ambientocclusion": False,
        "render_type": CUTOUT,
        "textures": {"particle": tex(name), "lichen": tex(name)},
        "elements": [{
            "from": [0, 0, 0.1], "to": [16, 16, 0.1],
            "faces": {"north": {"uv": [16, 0, 0, 16], "texture": "#lichen"},
                      "south": {"uv": [0, 0, 16, 16], "texture": "#lichen"}},
        }],
    })
    parts = []
    all_false = {f: "false" for f in FACES}
    for face, rot in FACES.items():
        apply = {"model": f"{MOD}:block/{name}", **rot}
        if face != "north":
            apply["uvlock"] = True
        parts.append({"when": {face: "true"}, "apply": apply})
        parts.append({"when": all_false, "apply": apply})
    write(A / "blockstates" / f"{name}.json", {"multipart": parts})
    generated_item(name, name)

for name in HANGING + CROSS:
    cross(name)
    simple_state(name)
    generated_item(name, name)

for block, carpet in MOSS.items():
    block_model(block, {"parent": "minecraft:block/cube_all", "textures": {"all": tex(block)}})
    block_model(carpet, {"parent": "minecraft:block/carpet", "textures": {"wool": tex(block)}})
    simple_state(block)
    simple_state(carpet)
    item_model(block, {"parent": f"{MOD}:block/{block}"})
    item_model(carpet, {"parent": f"{MOD}:block/{carpet}"})

for name in DOUBLE:
    cross(f"{name}_bottom")
    cross(f"{name}_top")
    write(A / "blockstates" / f"{name}.json", {"variants": {
        "half=lower": {"model": f"{MOD}:block/{name}_bottom"},
        "half=upper": {"model": f"{MOD}:block/{name}_top"},
    }})
    generated_item(name, f"{name}_top")

PAD_ELEMENT = {
    "from": [0, 0.25, 0], "to": [16, 0.25, 16],
    "faces": {"down": {"uv": [16, 16, 0, 0], "texture": "#pad"}, "up": {"uv": [16, 16, 0, 0], "texture": "#pad"}},
}
block_model("lotus_pad", {"ambientocclusion": False, "render_type": CUTOUT,
                          "textures": {"particle": tex("lotus_pad"), "pad": tex("lotus_pad")},
                          "elements": [PAD_ELEMENT]})
block_model("lotus_flower", {
    "ambientocclusion": False, "render_type": CUTOUT,
    "textures": {"particle": tex("lotus_flower"), "pad": tex("lotus_pad"), "flower": tex("lotus_flower")},
    "elements": [
        PAD_ELEMENT,
        {"from": [0.8, 0.25, 8], "to": [15.2, 16.25, 8], "shade": False,
         "rotation": {"origin": [8, 8, 8], "axis": "y", "angle": 45, "rescale": True},
         "faces": {"north": {"uv": [0, 0, 16, 16], "texture": "#flower"},
                   "south": {"uv": [0, 0, 16, 16], "texture": "#flower"}}},
        {"from": [8, 0.25, 0.8], "to": [8, 16.25, 15.2], "shade": False,
         "rotation": {"origin": [8, 8, 8], "axis": "y", "angle": 45, "rescale": True},
         "faces": {"west": {"uv": [0, 0, 16, 16], "texture": "#flower"},
                   "east": {"uv": [0, 0, 16, 16], "texture": "#flower"}}},
    ],
})
for name in LILY:
    write(A / "blockstates" / f"{name}.json", {"variants": {"": [
        {"model": f"{MOD}:block/{name}"}, {"model": f"{MOD}:block/{name}", "y": 90},
        {"model": f"{MOD}:block/{name}", "y": 180}, {"model": f"{MOD}:block/{name}", "y": 270},
    ]}})
    generated_item(name, name)

for name in FLAT:
    block_model(name, {
        "ambientocclusion": False, "render_type": CUTOUT,
        "textures": {"particle": tex(name), "texture": tex(name)},
        "elements": [{"from": [0, 0.5, 0], "to": [16, 0.5, 16],
                      "faces": {"up": {"uv": [0, 0, 16, 16], "texture": "#texture"},
                                "down": {"uv": [0, 16, 16, 0], "texture": "#texture"}}}],
    })
    write(A / "blockstates" / f"{name}.json", {"variants": {"": [
        {"model": f"{MOD}:block/{name}"}, {"model": f"{MOD}:block/{name}", "y": 90},
        {"model": f"{MOD}:block/{name}", "y": 180}, {"model": f"{MOD}:block/{name}", "y": 270},
    ]}})
    generated_item(name, name)

# --------------------------------------------------------------------------- lang

lang = {"itemGroup.mcflora": "Minecraft Flora"}
for key, value in NAMES.items():
    lang[f"block.{MOD}.{key}"] = value
write(A / "lang/en_us.json", lang)

# --------------------------------------------------------------------------- loot tables

SURVIVES = {"condition": "minecraft:survives_explosion"}


def drop_self(name, conditions=None):
    return {"type": "minecraft:block", "random_sequence": f"{MOD}:blocks/{name}", "pools": [{
        "rolls": 1, "bonus_rolls": 0,
        "entries": [{"type": "minecraft:item", "name": m(name)}],
        "conditions": conditions or [SURVIVES],
    }]}


for name in ALL:
    if name in LICHENS:
        functions = [{"function": "minecraft:set_count", "add": True, "count": 1,
                      "conditions": [{"condition": "minecraft:block_state_property", "block": m(name),
                                      "properties": {face: "true"}}]} for face in FACES]
        functions += [{"function": "minecraft:set_count", "add": True, "count": -1},
                      {"function": "minecraft:explosion_decay"}]
        table = {"type": "minecraft:block", "random_sequence": f"{MOD}:blocks/{name}", "pools": [{
            "rolls": 1, "bonus_rolls": 0,
            "entries": [{"type": "minecraft:item", "name": m(name), "functions": functions,
                         "conditions": [{"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}}]}],
        }]}
    elif name in DOUBLE:
        table = drop_self(name, [SURVIVES, {"condition": "minecraft:block_state_property", "block": m(name),
                                            "properties": {"half": "lower"}}])
    else:
        table = drop_self(name)
    write(D / "loot_table/blocks" / f"{name}.json", table)

# --------------------------------------------------------------------------- block & item tags

SMALL_FLOWERS = ["arctic_poppy", "red_spider_lily", "blue_hydrangea", "pink_hydrangea"]
TALL_FLOWERS = ["cotton_grass", "japanese_iris"]
MOSS_BLOCKS = list(MOSS)
CARPETS = list(MOSS.values())
PLANTS = [n for n in ALL if n not in MOSS_BLOCKS + CARPETS]


def tag(registry, namespace, name, values):
    write(ROOT / "data" / namespace / "tags" / registry / f"{name}.json", {"replace": False, "values": values})


def opt(id_):
    return {"id": id_, "required": False}


tag("block", "minecraft", "small_flowers", [m(n) for n in SMALL_FLOWERS])
tag("block", "minecraft", "tall_flowers", [m(n) for n in TALL_FLOWERS])
tag("item", "minecraft", "small_flowers", [m(n) for n in SMALL_FLOWERS])
tag("item", "minecraft", "tall_flowers", [m(n) for n in TALL_FLOWERS])
tag("block", "minecraft", "mineable/hoe", [m(n) for n in MOSS_BLOCKS + CARPETS])
tag("block", "minecraft", "sword_efficient", [m(n) for n in PLANTS])
tag("block", "minecraft", "replaceable_by_trees", [m(n) for n in PLANTS if n not in LILY])
tag("block", "minecraft", "dirt", [m(n) for n in MOSS_BLOCKS])
tag("block", "minecraft", "combination_step_sound_blocks", [m(n) for n in CARPETS])
tag("block", "minecraft", "enderman_holdable", [m(n) for n in SMALL_FLOWERS])

tag("block", MOD, "mosses", ["minecraft:moss_block"] + [m(n) for n in MOSS_BLOCKS])
tag("block", MOD, "tundra_plantable", ["#mcflora:mosses", "minecraft:snow_block", "minecraft:gravel",
                                       "minecraft:calcite", "minecraft:packed_ice", "#minecraft:base_stone_overworld"])
tag("block", MOD, "lichen_can_grow_on", ["#minecraft:base_stone_overworld", "#minecraft:logs", "minecraft:cobblestone",
                                         "minecraft:mossy_cobblestone", "minecraft:gravel", "minecraft:calcite",
                                         "minecraft:dripstone_block", "minecraft:coarse_dirt", "minecraft:podzol",
                                         "minecraft:moss_block", "minecraft:packed_ice"])
tag("block", MOD, "moss_replaceable", ["minecraft:grass_block", "minecraft:dirt", "minecraft:coarse_dirt",
                                       "minecraft:podzol", "minecraft:rooted_dirt", "minecraft:moss_block"])

# --------------------------------------------------------------------------- recipes


def shapeless(name, ingredients, result, count=1, group=None):
    obj = {"type": "minecraft:crafting_shapeless", "category": "misc",
           "ingredients": [{"item": i} for i in ingredients],
           "result": {"id": result, "count": count}}
    if group:
        obj["group"] = group
    write(D / "recipe" / f"{name}.json", obj)


DYES = {
    "silver_lichen": ("light_gray_dye", 1), "black_lichen": ("black_dye", 1), "brown_lichen": ("brown_dye", 1),
    "rust_lichen": ("orange_dye", 1), "old_mans_beard": ("lime_dye", 1), "arctic_poppy": ("yellow_dye", 1),
    "cotton_grass": ("white_dye", 2), "red_spider_lily": ("red_dye", 1), "japanese_iris": ("purple_dye", 2),
    "blue_hydrangea": ("light_blue_dye", 2), "pink_hydrangea": ("pink_dye", 2), "lotus_flower": ("pink_dye", 1),
    "rafflesia": ("red_dye", 2),
}
for src, (dye, count) in DYES.items():
    shapeless(f"{dye}_from_{src}", [m(src)], f"minecraft:{dye}", count, group=dye)

for block, carpet in MOSS.items():
    write(D / "recipe" / f"{carpet}.json", {
        "type": "minecraft:crafting_shaped", "category": "building", "group": "carpet",
        "pattern": ["##"], "key": {"#": {"item": m(block)}}, "result": {"id": m(carpet), "count": 3}})
shapeless("frost_moss_block", ["minecraft:moss_block", "minecraft:snowball"], m("frost_moss_block"))
shapeless("sphagnum_moss_block", ["minecraft:moss_block", "minecraft:red_mushroom"], m("sphagnum_moss_block"))

# --------------------------------------------------------------------------- compostables (NeoForge data map)

COMPOST = {n: 0.65 for n in ALL}
COMPOST.update({n: 0.3 for n in LICHENS + CARPETS + ["reindeer_lichen", "old_mans_beard"]})
COMPOST.update({n: 0.65 for n in MOSS_BLOCKS})
COMPOST.update({"monstera": 0.85, "rafflesia": 0.85, "lotus_pad": 0.65})
write(ROOT / "data/neoforge/data_maps/item/compostables.json",
      {"replace": False, "values": {m(k): {"chance": v} for k, v in COMPOST.items()}})

# --------------------------------------------------------------------------- worldgen
#
# Every feature is placed relative to the live heightmap rather than at fixed Y levels, and every
# biome filter is a biome *tag*. That keeps generation correct under Tectonic's taller terrain and
# lets other biome mods opt in (the optional #c: entries cover Terralith and friends).

WG = D / "worldgen"


def state(name, **props):
    s = {"Name": name if ":" in name else m(name)}
    if props:
        s["Properties"] = props
    return s


def provider(name, **props):
    return {"type": "minecraft:simple_state_provider", "state": state(name, **props)}


def survive_filter(st, extra=None):
    preds = [{"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
             {"type": "minecraft:would_survive", "state": st}]
    if extra:
        preds.append(extra)
    return [{"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:all_of", "predicates": preds}}]


def patch(name, to_place, survive_state, tries=32, xz=7, y=3, extra=None):
    write(WG / "configured_feature" / f"{name}.json", {"type": "minecraft:random_patch", "config": {
        "tries": tries, "xz_spread": xz, "y_spread": y,
        "feature": {"feature": {"type": "minecraft:simple_block", "config": {"to_place": to_place}},
                    "placement": survive_filter(survive_state, extra)},
    }})


def placed(name, modifiers, feature=None):
    write(WG / "placed_feature" / f"{name}.json", {"feature": m(feature or name), "placement": modifiers})


def surface(heightmap="MOTION_BLOCKING_NO_LEAVES", count=None, rarity=None, offset=None):
    mods = []
    if rarity:
        mods.append({"type": "minecraft:rarity_filter", "chance": rarity})
    if count:
        mods.append({"type": "minecraft:count", "count": count})
    mods += [{"type": "minecraft:in_square"}, {"type": "minecraft:heightmap", "heightmap": heightmap}]
    if offset:
        mods.append({"type": "minecraft:random_offset", "xz_spread": 0, "y_spread": offset})
    mods.append({"type": "minecraft:biome"})
    return mods


def biome_tag(name, values):
    tag("worldgen/biome", MOD, name, values)


def modifier(name, biomes, features):
    write(D / "neoforge/biome_modifier" / f"{name}.json", {
        "type": "neoforge:add_features", "biomes": f"#{MOD}:{biomes}",
        "features": [m(f) for f in features], "step": "vegetal_decoration"})


def uniform(lo, hi):
    return {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi}


# ---- biome tags
biome_tag("has_lichens", ["minecraft:taiga", "minecraft:snowy_taiga", "minecraft:old_growth_pine_taiga",
                          "minecraft:old_growth_spruce_taiga", "minecraft:grove", "minecraft:snowy_slopes",
                          "minecraft:windswept_hills", "minecraft:windswept_gravelly_hills",
                          "minecraft:windswept_forest", "minecraft:stony_peaks", "minecraft:jagged_peaks",
                          "minecraft:frozen_peaks", "minecraft:stony_shore", "minecraft:snowy_beach",
                          opt("#c:is_taiga"), opt("#c:is_snowy")])
biome_tag("has_old_mans_beard", ["#minecraft:is_taiga", "minecraft:windswept_forest", "minecraft:grove",
                                 opt("#c:is_taiga")])
biome_tag("has_reindeer_lichen", ["minecraft:snowy_plains", "minecraft:snowy_taiga", "minecraft:grove",
                                  "minecraft:snowy_slopes", "minecraft:ice_spikes", "minecraft:frozen_peaks",
                                  "minecraft:windswept_gravelly_hills", "minecraft:old_growth_pine_taiga",
                                  opt("#c:is_snowy")])
biome_tag("has_frost_moss", ["minecraft:snowy_plains", "minecraft:snowy_taiga", "minecraft:grove",
                             "minecraft:ice_spikes", "minecraft:snowy_slopes"])
biome_tag("has_sphagnum_moss", ["minecraft:taiga", "minecraft:old_growth_pine_taiga",
                                "minecraft:old_growth_spruce_taiga", "minecraft:swamp"])
biome_tag("has_cotton_grass", ["minecraft:snowy_plains", "minecraft:snowy_taiga", "minecraft:taiga",
                               "minecraft:windswept_hills", "minecraft:meadow"])
biome_tag("has_arctic_poppy", ["minecraft:snowy_plains", "minecraft:snowy_slopes", "minecraft:grove",
                               "minecraft:frozen_peaks", "minecraft:jagged_peaks", "minecraft:ice_spikes",
                               "minecraft:windswept_gravelly_hills"])
biome_tag("has_bracken", ["#minecraft:is_taiga", "#minecraft:is_forest", "minecraft:windswept_forest",
                          opt("#c:is_taiga")])
biome_tag("has_sasa", ["minecraft:bamboo_jungle", "minecraft:cherry_grove"])
biome_tag("has_red_spider_lily", ["minecraft:cherry_grove", "minecraft:bamboo_jungle", "minecraft:flower_forest"])
biome_tag("has_japanese_iris", ["minecraft:cherry_grove", "minecraft:bamboo_jungle", "minecraft:swamp",
                                "minecraft:river"])
biome_tag("has_hydrangea", ["minecraft:cherry_grove", "minecraft:bamboo_jungle", "minecraft:flower_forest"])
biome_tag("has_lotus", ["minecraft:swamp", "minecraft:mangrove_swamp", "#minecraft:is_jungle",
                        "minecraft:cherry_grove"])
biome_tag("has_jungle_flora", ["#minecraft:is_jungle", opt("#c:is_jungle")])
biome_tag("has_rafflesia", ["minecraft:jungle", "minecraft:bamboo_jungle"])

# ---- lichens: multiface growth that crusts over exposed rock, cliffs and bark
for name in LICHENS:
    write(WG / "configured_feature" / f"{name}.json", {"type": "minecraft:multiface_growth", "config": {
        "block": m(name), "search_range": 20, "chance_of_spreading": 0.6,
        "can_place_on_floor": True, "can_place_on_ceiling": True, "can_place_on_wall": True,
        "can_be_placed_on": "#mcflora:lichen_can_grow_on"}})
    placed(name, surface("MOTION_BLOCKING_NO_LEAVES", count=8, offset=uniform(0, 10)))
modifier("add_lichens", "has_lichens", LICHENS)

# ---- hanging old man's beard below spruce canopies
HANG_FILTER_Y = -4
patch("old_mans_beard", provider("old_mans_beard"), state("old_mans_beard"), tries=48, xz=6, y=6)
placed("old_mans_beard", surface("MOTION_BLOCKING", count=6, offset=HANG_FILTER_Y))
modifier("add_old_mans_beard", "has_old_mans_beard", ["old_mans_beard"])

# ---- ground lichen & tundra plants
patch("reindeer_lichen", provider("reindeer_lichen"), state("reindeer_lichen"), tries=24, xz=5, y=2)
placed("reindeer_lichen", surface(count=2))
modifier("add_reindeer_lichen", "has_reindeer_lichen", ["reindeer_lichen"])

patch("cotton_grass", provider("cotton_grass", half="lower"), state("cotton_grass", half="lower"), tries=40, xz=6)
placed("cotton_grass", surface(rarity=2))
modifier("add_cotton_grass", "has_cotton_grass", ["cotton_grass"])

patch("arctic_poppy", provider("arctic_poppy"), state("arctic_poppy"), tries=20, xz=5, y=2)
placed("arctic_poppy", surface(rarity=3))
modifier("add_arctic_poppy", "has_arctic_poppy", ["arctic_poppy"])

patch("bracken", provider("bracken", half="lower"), state("bracken", half="lower"), tries=56, xz=6)
placed("bracken", surface(rarity=2))
modifier("add_bracken", "has_bracken", ["bracken"])

# ---- moss carpets: patches of moss block topped with carpet and a few plants
MOSS_VEG = {
    "frost_moss_block": [(4, state("frost_moss_carpet")), (1, state("reindeer_lichen"))],
    "sphagnum_moss_block": [(4, state("sphagnum_moss_carpet")), (1, state("minecraft:fern"))],
}
for block, entries in MOSS_VEG.items():
    base = block.replace("_block", "")
    write(WG / "configured_feature" / f"{base}_vegetation.json", {"type": "minecraft:simple_block", "config": {
        "to_place": {"type": "minecraft:weighted_state_provider",
                     "entries": [{"weight": w, "data": s} for w, s in entries]}}})
    placed(f"{base}_vegetation", [])
    write(WG / "configured_feature" / f"{base}_patch.json", {"type": "minecraft:vegetation_patch", "config": {
        "replaceable": "#mcflora:moss_replaceable", "ground_state": provider(block),
        "vegetation_feature": m(f"{base}_vegetation"), "surface": "floor", "depth": 1,
        "extra_bottom_block_chance": 0.0, "vertical_range": 5, "vegetation_chance": 0.6,
        "xz_radius": uniform(2, 4), "extra_edge_column_chance": 0.4}})
placed("frost_moss_patch", surface(rarity=3))
placed("sphagnum_moss_patch", surface(rarity=4))
modifier("add_frost_moss", "has_frost_moss", ["frost_moss_patch"])
modifier("add_sphagnum_moss", "has_sphagnum_moss", ["sphagnum_moss_patch"])

# ---- east asian plants
patch("sasa_bamboo_grass", provider("sasa_bamboo_grass", half="lower"), state("sasa_bamboo_grass", half="lower"),
      tries=48, xz=6)
placed("sasa_bamboo_grass", surface(count=2))
modifier("add_sasa", "has_sasa", ["sasa_bamboo_grass"])

patch("red_spider_lily", provider("red_spider_lily"), state("red_spider_lily"), tries=24, xz=5, y=2)
placed("red_spider_lily", surface(rarity=3))
modifier("add_red_spider_lily", "has_red_spider_lily", ["red_spider_lily"])

NEAR_WATER = {"type": "minecraft:any_of", "predicates": [
    {"type": "minecraft:matching_fluids", "offset": off, "fluids": ["minecraft:water", "minecraft:flowing_water"]}
    for off in ([1, -1, 0], [-1, -1, 0], [0, -1, 1], [0, -1, -1])]}
patch("japanese_iris", provider("japanese_iris", half="lower"), state("japanese_iris", half="lower"),
      tries=64, xz=7, y=3, extra=NEAR_WATER)
placed("japanese_iris", surface(count=3))
modifier("add_japanese_iris", "has_japanese_iris", ["japanese_iris"])

patch("hydrangea", {"type": "minecraft:weighted_state_provider", "entries": [
    {"weight": 1, "data": state("blue_hydrangea")}, {"weight": 1, "data": state("pink_hydrangea")}]},
      state("blue_hydrangea"), tries=12, xz=4, y=2)
placed("hydrangea", surface(rarity=4))
modifier("add_hydrangea", "has_hydrangea", ["hydrangea"])

patch("lotus", {"type": "minecraft:weighted_state_provider", "entries": [
    {"weight": 3, "data": state("lotus_pad")}, {"weight": 1, "data": state("lotus_flower")}]},
      state("lotus_pad"), tries=12, xz=7, y=3)
placed("lotus", surface("WORLD_SURFACE_WG", count=3))
modifier("add_lotus", "has_lotus", ["lotus"])

# ---- jungle plants
patch("monstera", provider("monstera", half="lower"), state("monstera", half="lower"), tries=32, xz=6)
placed("monstera", surface(count=3))
patch("birds_nest_fern", provider("birds_nest_fern"), state("birds_nest_fern"), tries=24, xz=6)
placed("birds_nest_fern", surface(count=2))
patch("nepenthes", provider("nepenthes"), state("nepenthes"), tries=40, xz=6, y=6)
placed("nepenthes", surface("MOTION_BLOCKING", count=4, offset=HANG_FILTER_Y))
modifier("add_jungle_flora", "has_jungle_flora", ["monstera", "birds_nest_fern", "nepenthes"])

patch("rafflesia", provider("rafflesia"), state("rafflesia"), tries=4, xz=4, y=2)
placed("rafflesia", surface(rarity=10))
modifier("add_rafflesia", "has_rafflesia", ["rafflesia"])

# --------------------------------------------------------------------------- game test template
#
# An empty 11x8x11 box of air that the game tests build their terrain in (see FloraGameTests).

TAG_INT, TAG_STRING, TAG_LIST, TAG_COMPOUND = 3, 8, 9, 10


def nbt_string(value):
    data = value.encode("utf-8")
    return struct.pack(">H", len(data)) + data


def nbt_payload(tag_type, value):
    if tag_type == TAG_INT:
        return struct.pack(">i", value)
    if tag_type == TAG_STRING:
        return nbt_string(value)
    if tag_type == TAG_LIST:
        element_type, items = value
        return struct.pack(">bi", element_type, len(items)) + b"".join(nbt_payload(element_type, i) for i in items)
    if tag_type == TAG_COMPOUND:
        body = b"".join(struct.pack(">b", t) + nbt_string(k) + nbt_payload(t, v) for k, (t, v) in value.items())
        return body + b"\x00"
    raise ValueError(tag_type)


def write_structure(path, size, palette, blocks):
    root = {
        "DataVersion": (TAG_INT, 3955),  # Minecraft 1.21.1
        "size": (TAG_LIST, (TAG_INT, list(size))),
        "palette": (TAG_LIST, (TAG_COMPOUND, [{"Name": (TAG_STRING, name)} for name in palette])),
        "blocks": (TAG_LIST, (TAG_COMPOUND, [
            {"pos": (TAG_LIST, (TAG_INT, list(pos))), "state": (TAG_INT, state)} for pos, state in blocks])),
        "entities": (TAG_LIST, (TAG_COMPOUND, [])),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = struct.pack(">b", TAG_COMPOUND) + nbt_string("") + nbt_payload(TAG_COMPOUND, root)
    path.write_bytes(gzip.compress(raw, mtime=0))


PLATFORM = (11, 8, 11)
write_structure(D / "structure/platform.nbt", PLATFORM, ["minecraft:air"],
                [((x, y, z), 0) for y in range(PLATFORM[1]) for z in range(PLATFORM[2]) for x in range(PLATFORM[0])])

print("data written under", ROOT)
