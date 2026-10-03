package io.github.flames0222.mcflora.registry;

import io.github.flames0222.mcflora.McFlora;
import io.github.flames0222.mcflora.block.BrackenBlock;
import io.github.flames0222.mcflora.block.FloraPlantBlock;
import io.github.flames0222.mcflora.block.FloraPlantBlock.Soil;
import io.github.flames0222.mcflora.block.HangingPlantBlock;
import io.github.flames0222.mcflora.block.LichenBlock;
import io.github.flames0222.mcflora.block.TundraFlowerBlock;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CarpetBlock;
import net.minecraft.world.level.block.DoublePlantBlock;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.TallFlowerBlock;
import net.minecraft.world.level.block.WaterlilyBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.List;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(McFlora.MOD_ID);

    private static final VoxelShape LOW_PLANT = Block.box(2, 0, 2, 14, 10, 14);
    private static final VoxelShape BUSHY_PLANT = Block.box(1, 0, 1, 15, 14, 15);
    private static final VoxelShape FLAT_FLOWER = Block.box(0, 0, 0, 16, 4, 16);

    // ---------------------------------------------------------------- cold biomes: lichens

    public static final DeferredBlock<LichenBlock> SILVER_LICHEN = lichen("silver_lichen", MapColor.COLOR_LIGHT_GRAY);
    public static final DeferredBlock<LichenBlock> BLACK_LICHEN = lichen("black_lichen", MapColor.COLOR_BLACK);
    public static final DeferredBlock<LichenBlock> BROWN_LICHEN = lichen("brown_lichen", MapColor.COLOR_BROWN);
    public static final DeferredBlock<LichenBlock> RUST_LICHEN = lichen("rust_lichen", MapColor.COLOR_ORANGE);

    public static final DeferredBlock<HangingPlantBlock> OLD_MANS_BEARD = BLOCKS.register("old_mans_beard",
            () -> new HangingPlantBlock(plant(MapColor.COLOR_LIGHT_GREEN).sound(SoundType.HANGING_ROOTS)
                    .offsetType(BlockBehaviour.OffsetType.XZ)));

    public static final DeferredBlock<FloraPlantBlock> REINDEER_LICHEN = BLOCKS.register("reindeer_lichen",
            () -> new FloraPlantBlock(plant(MapColor.TERRACOTTA_WHITE).sound(SoundType.MOSS_CARPET)
                    .offsetType(BlockBehaviour.OffsetType.XZ), LOW_PLANT, Soil.TUNDRA));

    // ---------------------------------------------------------------- cold biomes: mosses

    public static final DeferredBlock<Block> FROST_MOSS_BLOCK = BLOCKS.register("frost_moss_block",
            () -> new Block(moss(MapColor.COLOR_LIGHT_BLUE)));
    public static final DeferredBlock<CarpetBlock> FROST_MOSS_CARPET = BLOCKS.register("frost_moss_carpet",
            () -> new CarpetBlock(mossCarpet(MapColor.COLOR_LIGHT_BLUE)));
    public static final DeferredBlock<Block> SPHAGNUM_MOSS_BLOCK = BLOCKS.register("sphagnum_moss_block",
            () -> new Block(moss(MapColor.TERRACOTTA_GREEN)));
    public static final DeferredBlock<CarpetBlock> SPHAGNUM_MOSS_CARPET = BLOCKS.register("sphagnum_moss_carpet",
            () -> new CarpetBlock(mossCarpet(MapColor.TERRACOTTA_GREEN)));

    // ---------------------------------------------------------------- cold biomes: tundra & taiga plants

    public static final DeferredBlock<TallFlowerBlock> COTTON_GRASS = BLOCKS.register("cotton_grass",
            () -> new TallFlowerBlock(plant(MapColor.SNOW)));
    public static final DeferredBlock<TundraFlowerBlock> ARCTIC_POPPY = BLOCKS.register("arctic_poppy",
            () -> new TundraFlowerBlock(MobEffects.FIRE_RESISTANCE, 4.0F, plant(MapColor.COLOR_YELLOW)
                    .offsetType(BlockBehaviour.OffsetType.XZ)));
    public static final DeferredBlock<BrackenBlock> BRACKEN = BLOCKS.register("bracken",
            () -> new BrackenBlock(plant(MapColor.PLANT).replaceable()));

    // ---------------------------------------------------------------- east asian plants

    public static final DeferredBlock<DoublePlantBlock> SASA_BAMBOO_GRASS = BLOCKS.register("sasa_bamboo_grass",
            () -> new DoublePlantBlock(plant(MapColor.PLANT).replaceable()));
    public static final DeferredBlock<FlowerBlock> RED_SPIDER_LILY = BLOCKS.register("red_spider_lily",
            () -> new FlowerBlock(MobEffects.WITHER, 4.0F, plant(MapColor.COLOR_RED)
                    .offsetType(BlockBehaviour.OffsetType.XZ)));
    public static final DeferredBlock<TallFlowerBlock> JAPANESE_IRIS = BLOCKS.register("japanese_iris",
            () -> new TallFlowerBlock(plant(MapColor.COLOR_PURPLE)));
    public static final DeferredBlock<FlowerBlock> BLUE_HYDRANGEA = BLOCKS.register("blue_hydrangea",
            () -> new FlowerBlock(MobEffects.WATER_BREATHING, 6.0F, plant(MapColor.COLOR_BLUE)));
    public static final DeferredBlock<FlowerBlock> PINK_HYDRANGEA = BLOCKS.register("pink_hydrangea",
            () -> new FlowerBlock(MobEffects.REGENERATION, 6.0F, plant(MapColor.COLOR_PINK)));
    public static final DeferredBlock<WaterlilyBlock> LOTUS_PAD = BLOCKS.register("lotus_pad",
            () -> new WaterlilyBlock(lilyPad(MapColor.PLANT)));
    public static final DeferredBlock<WaterlilyBlock> LOTUS_FLOWER = BLOCKS.register("lotus_flower",
            () -> new WaterlilyBlock(lilyPad(MapColor.COLOR_PINK)));

    // ---------------------------------------------------------------- jungle plants

    public static final DeferredBlock<DoublePlantBlock> MONSTERA = BLOCKS.register("monstera",
            () -> new DoublePlantBlock(plant(MapColor.PLANT).replaceable()));
    public static final DeferredBlock<FloraPlantBlock> BIRDS_NEST_FERN = BLOCKS.register("birds_nest_fern",
            () -> new FloraPlantBlock(plant(MapColor.PLANT).replaceable()
                    .offsetType(BlockBehaviour.OffsetType.XZ), BUSHY_PLANT, Soil.DIRT));
    public static final DeferredBlock<HangingPlantBlock> NEPENTHES = BLOCKS.register("nepenthes",
            () -> new HangingPlantBlock(plant(MapColor.COLOR_RED).sound(SoundType.HANGING_ROOTS)
                    .offsetType(BlockBehaviour.OffsetType.XZ)));
    public static final DeferredBlock<FloraPlantBlock> RAFFLESIA = BLOCKS.register("rafflesia",
            () -> new FloraPlantBlock(plant(MapColor.COLOR_RED).sound(SoundType.WET_GRASS),
                    FLAT_FLOWER, Soil.DIRT));

    private ModBlocks() {
    }

    public static List<DeferredBlock<?>> flammablePlants() {
        return List.of(SILVER_LICHEN, BLACK_LICHEN, BROWN_LICHEN, RUST_LICHEN, OLD_MANS_BEARD, REINDEER_LICHEN,
                COTTON_GRASS, ARCTIC_POPPY, BRACKEN, SASA_BAMBOO_GRASS, RED_SPIDER_LILY, JAPANESE_IRIS,
                BLUE_HYDRANGEA, PINK_HYDRANGEA, MONSTERA, BIRDS_NEST_FERN, NEPENTHES, RAFFLESIA);
    }

    public static List<DeferredBlock<?>> flammableMosses() {
        return List.of(FROST_MOSS_BLOCK, FROST_MOSS_CARPET, SPHAGNUM_MOSS_BLOCK, SPHAGNUM_MOSS_CARPET);
    }

    private static DeferredBlock<LichenBlock> lichen(String name, MapColor color) {
        return BLOCKS.register(name, () -> new LichenBlock(BlockBehaviour.Properties.of()
                .mapColor(color)
                .replaceable()
                .noCollission()
                .strength(0.2F)
                .sound(SoundType.GLOW_LICHEN)
                .ignitedByLava()
                .pushReaction(PushReaction.DESTROY)));
    }

    private static BlockBehaviour.Properties plant(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .noCollission()
                .instabreak()
                .sound(SoundType.GRASS)
                .ignitedByLava()
                .pushReaction(PushReaction.DESTROY);
    }

    private static BlockBehaviour.Properties lilyPad(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .instabreak()
                .sound(SoundType.LILY_PAD)
                .noOcclusion()
                .pushReaction(PushReaction.DESTROY);
    }

    private static BlockBehaviour.Properties moss(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .strength(0.1F)
                .sound(SoundType.MOSS)
                .pushReaction(PushReaction.DESTROY);
    }

    private static BlockBehaviour.Properties mossCarpet(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .strength(0.1F)
                .sound(SoundType.MOSS_CARPET)
                .pushReaction(PushReaction.DESTROY);
    }
}
