package io.github.flames0222.mcflora.gametest;

import io.github.flames0222.mcflora.McFlora;
import io.github.flames0222.mcflora.registry.ModBlocks;
import io.github.flames0222.mcflora.registry.ModItems;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderSet;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.feature.ConfiguredFeature;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.minecraft.world.level.storage.loot.LootTable;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.datamaps.builtin.NeoForgeDataMaps;

import java.util.List;
import java.util.Map;

/**
 * Game tests that load the mod's data the way a real world does and place every worldgen feature.
 * Run with {@code ./gradlew runGameTestServer}; CI runs them on every push.
 *
 * <p>The template is an empty 11x8x11 box, so each test builds its own terrain. Terrain sits at
 * {@link #FLOOR} and above, clear of the structure block at the test's origin.
 */
@GameTestHolder(McFlora.MOD_ID)
@PrefixGameTestTemplate(false)
public final class FloraGameTests {
    private static final String TEMPLATE = "platform";
    private static final int FLOOR = 2;
    private static final int SIZE = 10;
    private static final int EXPECTED_RECIPES = 17;

    private FloraGameTests() {
    }

    // ------------------------------------------------------------------ data

    @GameTest(template = TEMPLATE)
    public static void biomeModifiersAddFeatures(GameTestHelper helper) {
        Registry<Biome> biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        Map<ResourceKey<Biome>, List<String>> expected = Map.of(
                Biomes.SNOWY_PLAINS, List.of("reindeer_lichen", "cotton_grass", "arctic_poppy", "frost_moss_patch"),
                Biomes.GROVE, List.of("reindeer_lichen", "old_mans_beard", "arctic_poppy", "frost_moss_patch"),
                Biomes.OLD_GROWTH_SPRUCE_TAIGA, List.of("silver_lichen", "black_lichen", "brown_lichen", "rust_lichen",
                        "old_mans_beard", "bracken", "sphagnum_moss_patch"),
                Biomes.CHERRY_GROVE, List.of("sasa_bamboo_grass", "red_spider_lily", "japanese_iris", "hydrangea", "lotus"),
                Biomes.BAMBOO_JUNGLE, List.of("sasa_bamboo_grass", "monstera", "birds_nest_fern", "nepenthes",
                        "rafflesia", "lotus"),
                Biomes.JUNGLE, List.of("monstera", "birds_nest_fern", "nepenthes", "rafflesia", "lotus"));
        int step = GenerationStep.Decoration.VEGETAL_DECORATION.ordinal();
        expected.forEach((key, features) -> {
            List<HolderSet<PlacedFeature>> steps = biomes.getOrThrow(key).getGenerationSettings().features();
            helper.assertTrue(steps.size() > step, key.location() + " has no vegetal decoration step");
            for (String feature : features) {
                helper.assertTrue(steps.get(step).stream().anyMatch(holder -> holder.is(McFlora.id(feature))),
                        key.location() + " is missing " + McFlora.id(feature));
            }
        });
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void lootRecipesTagsAndDataMapsLoad(GameTestHelper helper) {
        MinecraftServer server = helper.getLevel().getServer();
        for (DeferredHolder<Block, ? extends Block> block : ModBlocks.BLOCKS.getEntries()) {
            LootTable table = server.reloadableRegistries().getLootTable(block.get().getLootTable());
            helper.assertTrue(table != LootTable.EMPTY, "missing loot table for " + block.getId());
        }
        for (DeferredHolder<Item, ? extends Item> item : ModItems.ITEMS.getEntries()) {
            helper.assertTrue(item.get().builtInRegistryHolder().getData(NeoForgeDataMaps.COMPOSTABLES) != null,
                    item.getId() + " is not compostable");
        }
        long recipes = server.getRecipeManager().getRecipes().stream()
                .filter(recipe -> recipe.id().getNamespace().equals(McFlora.MOD_ID))
                .count();
        helper.assertTrue(recipes == EXPECTED_RECIPES, "expected " + EXPECTED_RECIPES + " recipes, loaded " + recipes);
        helper.assertTrue(ModBlocks.FROST_MOSS_BLOCK.get().defaultBlockState().is(BlockTags.DIRT),
                "frost moss should be in #minecraft:dirt");
        helper.assertTrue(ModItems.ARCTIC_POPPY.get().getDefaultInstance().is(ItemTags.SMALL_FLOWERS),
                "arctic poppy should be in #minecraft:small_flowers");
        helper.succeed();
    }

    // ------------------------------------------------------------------ survival rules

    @GameTest(template = TEMPLATE)
    public static void plantsRespectTheirSupport(GameTestHelper helper) {
        helper.setBlock(new BlockPos(2, 6, 2), leaves(Blocks.SPRUCE_LEAVES));
        assertSurvives(helper, ModBlocks.OLD_MANS_BEARD.get(), new BlockPos(2, 5, 2), true, "under spruce leaves");
        assertSurvives(helper, ModBlocks.OLD_MANS_BEARD.get(), new BlockPos(4, 5, 4), false, "with nothing above");
        helper.setBlock(new BlockPos(6, 6, 2), leaves(Blocks.JUNGLE_LEAVES));
        assertSurvives(helper, ModBlocks.NEPENTHES.get(), new BlockPos(6, 5, 2), true, "under jungle leaves");

        helper.setBlock(new BlockPos(2, FLOOR, 6), Blocks.SNOW_BLOCK);
        assertSurvives(helper, ModBlocks.REINDEER_LICHEN.get(), new BlockPos(2, FLOOR + 1, 6), true, "on snow");
        helper.setBlock(new BlockPos(4, FLOOR, 6), Blocks.STONE);
        assertSurvives(helper, ModBlocks.ARCTIC_POPPY.get(), new BlockPos(4, FLOOR + 1, 6), true, "on stone");
        assertSurvives(helper, ModBlocks.RED_SPIDER_LILY.get(), new BlockPos(4, FLOOR + 1, 6), false, "on stone");
        helper.setBlock(new BlockPos(6, FLOOR, 6), Blocks.SAND);
        assertSurvives(helper, ModBlocks.REINDEER_LICHEN.get(), new BlockPos(6, FLOOR + 1, 6), false, "on sand");
        helper.setBlock(new BlockPos(8, FLOOR, 6), ModBlocks.FROST_MOSS_BLOCK.get());
        assertSurvives(helper, ModBlocks.BRACKEN.get(), new BlockPos(8, FLOOR + 1, 6), true, "on frost moss");

        fill(helper, 7, FLOOR - 1, 7, 9, FLOOR, 9, Blocks.STONE.defaultBlockState());
        helper.setBlock(new BlockPos(8, FLOOR, 8), Blocks.WATER);
        assertSurvives(helper, ModBlocks.LOTUS_PAD.get(), new BlockPos(8, FLOOR + 1, 8), true, "on water");
        assertSurvives(helper, ModBlocks.LOTUS_FLOWER.get(), new BlockPos(7, FLOOR + 1, 7), false, "on stone");
        helper.succeed();
    }

    // ------------------------------------------------------------------ worldgen features

    @GameTest(template = TEMPLATE)
    public static void lichensCrustRock(GameTestHelper helper) {
        floor(helper, Blocks.STONE.defaultBlockState());
        assertPlaces(helper, "silver_lichen", new BlockPos(2, FLOOR + 1, 2), ModBlocks.SILVER_LICHEN.get());
        assertPlaces(helper, "black_lichen", new BlockPos(8, FLOOR + 1, 2), ModBlocks.BLACK_LICHEN.get());
        assertPlaces(helper, "brown_lichen", new BlockPos(2, FLOOR + 1, 8), ModBlocks.BROWN_LICHEN.get());
        assertPlaces(helper, "rust_lichen", new BlockPos(8, FLOOR + 1, 8), ModBlocks.RUST_LICHEN.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void tundraPlantsGrow(GameTestHelper helper) {
        floor(helper, Blocks.GRASS_BLOCK.defaultBlockState());
        BlockPos center = new BlockPos(5, FLOOR + 1, 5);
        assertPlaces(helper, "reindeer_lichen", center, ModBlocks.REINDEER_LICHEN.get());
        assertPlaces(helper, "cotton_grass", center, ModBlocks.COTTON_GRASS.get());
        assertPlaces(helper, "arctic_poppy", center, ModBlocks.ARCTIC_POPPY.get());
        assertPlaces(helper, "bracken", center, ModBlocks.BRACKEN.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void frostMossCarpetsGround(GameTestHelper helper) {
        floor(helper, Blocks.GRASS_BLOCK.defaultBlockState());
        assertPlaces(helper, "frost_moss_patch", new BlockPos(5, FLOOR + 1, 5), ModBlocks.FROST_MOSS_BLOCK.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void sphagnumMossCarpetsGround(GameTestHelper helper) {
        floor(helper, Blocks.GRASS_BLOCK.defaultBlockState());
        assertPlaces(helper, "sphagnum_moss_patch", new BlockPos(5, FLOOR + 1, 5), ModBlocks.SPHAGNUM_MOSS_BLOCK.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void oldMansBeardHangsFromCanopy(GameTestHelper helper) {
        fill(helper, 0, 6, 0, SIZE, 6, SIZE, leaves(Blocks.SPRUCE_LEAVES));
        assertPlaces(helper, "old_mans_beard", new BlockPos(5, 5, 5), ModBlocks.OLD_MANS_BEARD.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void eastAsianPlantsGrow(GameTestHelper helper) {
        // Grass with water channels on every even column, so irises and lotus have somewhere to go.
        fill(helper, 0, FLOOR - 1, 0, SIZE, FLOOR - 1, SIZE, Blocks.STONE.defaultBlockState());
        floor(helper, Blocks.GRASS_BLOCK.defaultBlockState());
        for (int x = 2; x <= 8; x += 2) {
            fill(helper, x, FLOOR, 1, x, FLOOR, SIZE - 1, Blocks.WATER.defaultBlockState());
        }
        BlockPos center = new BlockPos(5, FLOOR + 1, 5);
        assertPlaces(helper, "japanese_iris", center, ModBlocks.JAPANESE_IRIS.get());
        assertPlaces(helper, "lotus", center, ModBlocks.LOTUS_PAD.get());
        assertPlaces(helper, "sasa_bamboo_grass", center, ModBlocks.SASA_BAMBOO_GRASS.get());
        assertPlaces(helper, "red_spider_lily", center, ModBlocks.RED_SPIDER_LILY.get());
        assertPlaces(helper, "hydrangea", center, ModBlocks.BLUE_HYDRANGEA.get(), ModBlocks.PINK_HYDRANGEA.get());
        helper.succeed();
    }

    @GameTest(template = TEMPLATE)
    public static void junglePlantsGrow(GameTestHelper helper) {
        floor(helper, Blocks.GRASS_BLOCK.defaultBlockState());
        fill(helper, 0, 6, 0, SIZE, 6, SIZE, leaves(Blocks.JUNGLE_LEAVES));
        BlockPos center = new BlockPos(5, FLOOR + 1, 5);
        assertPlaces(helper, "monstera", center, ModBlocks.MONSTERA.get());
        assertPlaces(helper, "birds_nest_fern", center, ModBlocks.BIRDS_NEST_FERN.get());
        assertPlaces(helper, "rafflesia", center, ModBlocks.RAFFLESIA.get());
        assertPlaces(helper, "nepenthes", new BlockPos(5, 5, 5), ModBlocks.NEPENTHES.get());
        helper.succeed();
    }

    // ------------------------------------------------------------------ helpers

    private static BlockState leaves(Block block) {
        return block.defaultBlockState().setValue(LeavesBlock.PERSISTENT, true);
    }

    private static void floor(GameTestHelper helper, BlockState state) {
        fill(helper, 0, FLOOR, 0, SIZE, FLOOR, SIZE, state);
    }

    private static void fill(GameTestHelper helper, int x0, int y0, int z0, int x1, int y1, int z1, BlockState state) {
        for (BlockPos pos : BlockPos.betweenClosed(x0, y0, z0, x1, y1, z1)) {
            helper.setBlock(pos, state);
        }
    }

    private static void assertSurvives(GameTestHelper helper, Block block, BlockPos pos, boolean expected, String where) {
        boolean survives = block.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(pos));
        helper.assertTrue(survives == expected,
                block.getName().getString() + (expected ? " should survive " : " should not survive ") + where);
    }

    /**
     * Places a configured feature from the datapack, retrying a few seeds since patches scatter randomly,
     * then checks that at least one of the expected blocks appeared inside the test area.
     */
    private static void assertPlaces(GameTestHelper helper, String feature, BlockPos origin, Block... expected) {
        ServerLevel level = helper.getLevel();
        ConfiguredFeature<?, ?> configured = level.registryAccess()
                .registryOrThrow(Registries.CONFIGURED_FEATURE)
                .get(McFlora.id(feature));
        helper.assertTrue(configured != null, "missing configured feature " + McFlora.id(feature));
        boolean placed = false;
        for (long seed = 0; seed < 8 && !placed; seed++) {
            placed = configured.place(level, level.getChunkSource().getGenerator(), RandomSource.create(seed),
                    helper.absolutePos(origin));
        }
        helper.assertTrue(placed, McFlora.id(feature) + " placed nothing");
        helper.assertTrue(countInArea(helper, expected) > 0, McFlora.id(feature) + " did not place its plant");
    }

    private static int countInArea(GameTestHelper helper, Block... blocks) {
        int count = 0;
        for (BlockPos pos : BlockPos.betweenClosed(0, FLOOR, 0, SIZE, 7, SIZE)) {
            BlockState state = helper.getBlockState(pos);
            for (Block block : blocks) {
                if (state.is(block)) {
                    count++;
                }
            }
        }
        return count;
    }
}
