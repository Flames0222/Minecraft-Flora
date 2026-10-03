# Minecraft Flora

Decorative wild plants for **NeoForge 1.21.1**, with a focus on cold-biome mosses, lichens and
tundra plants, plus some East Asian and jungle flora. It's a fresh 1.21.1 take on the idea behind
[Wild Flora](https://www.modpackindex.com/mod/168975/wild-flora) by lightdeficient. All code and
textures here are original; nothing is copied from that mod, and this project isn't affiliated with it.

## Plants

### Cold biomes: lichens and mosses
| Block | Where it grows | Notes |
|---|---|---|
| Silver, Black, Brown and Rust Lichen | Taigas, groves, windswept hills, peaks, stony shores | Grows on any face like glow lichen, crusting rock, cliffs and bark. Spreads with bone meal; shears to collect. Craft into dyes. |
| Old Man's Beard | Under spruce canopies in taigas and groves | Hangs from leaves and logs. |
| Reindeer Lichen | Snowy plains, snowy taiga, groves, slopes, peaks | Roots in snow, gravel, stone or moss. |
| Frost Moss Block / Carpet | Snowy plains, snowy taiga, groves, ice spikes | Bluish frosted moss patches. Craft: moss block + snowball. |
| Sphagnum Moss Block / Carpet | Taigas, old growth taigas, swamps | Reddish bog moss with ferns. Craft: moss block + red mushroom. |
| Cotton Grass | Snowy plains, taigas, meadows | Two blocks tall, with white seed tufts. |
| Arctic Poppy | Snowy plains, slopes, groves, peaks | Grows on snow and bare stone. |
| Bracken | All forests and taigas | Dense two-block fern undergrowth that slightly slows movement. |

### East Asian plants
| Block | Where it grows |
|---|---|
| Sasa Bamboo Grass (kumazasa, with white-edged leaves) | Bamboo jungles, cherry groves |
| Red Spider Lily (higanbana) | Cherry groves, bamboo jungles, flower forests |
| Japanese Iris (hanashōbu) | Next to water in cherry groves, bamboo jungles, swamps and rivers |
| Blue and Pink Hydrangea (ajisai) | Cherry groves, bamboo jungles, flower forests |
| Lotus Pad and Lotus Flower | On water in swamps, jungles and cherry groves |

### Jungle plants
| Block | Where it grows |
|---|---|
| Monstera | Jungle floors |
| Bird's Nest Fern | Jungle floors |
| Nepenthes (pitcher plant) | Hanging from jungle canopies |
| Rafflesia | Rare, jungle and bamboo jungle floors |

## Tectonic and other worldgen mods
Tectonic only reshapes terrain and keeps vanilla biomes, so no hard dependency is needed. To stay
compatible with it (and with other terrain mods):

* Every feature is placed against the live heightmap, never at hard-coded Y levels, so plants follow
  Tectonic's taller mountains and deeper valleys.
* All spawning goes through NeoForge biome modifiers that target **biome tags**
  (`data/mcflora/tags/worldgen/biome/has_*.json`). They include optional `#c:is_snowy`,
  `#c:is_taiga` and `#c:is_jungle` entries, so biome mods that use the common tags (like Terralith)
  get the plants too.
* To add or remove biomes, override a `has_*` tag in a datapack.

## Building
Needs JDK 21.

```sh
./gradlew build          # jar ends up in build/libs/
./gradlew runClient      # dev client
```

GitHub Actions builds the jar on every push. Download it from the run's **mcflora-jar** artifact.

### Regenerating assets
JSON and textures come from scripts, so edit those rather than the generated files:

```sh
pip install pillow
python3 tools/gen_textures.py   # 16x16 textures
python3 tools/gen_data.py       # blockstates, models, loot, tags, recipes, worldgen
```
