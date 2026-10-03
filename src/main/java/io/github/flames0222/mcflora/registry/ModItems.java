package io.github.flames0222.mcflora.registry;

import io.github.flames0222.mcflora.McFlora;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.DoubleHighBlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PlaceOnWaterBlockItem;
import net.minecraft.world.level.block.Block;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(McFlora.MOD_ID);

    // Order here is the order in the creative tab.
    public static final DeferredItem<BlockItem> SILVER_LICHEN = block(ModBlocks.SILVER_LICHEN);
    public static final DeferredItem<BlockItem> BLACK_LICHEN = block(ModBlocks.BLACK_LICHEN);
    public static final DeferredItem<BlockItem> BROWN_LICHEN = block(ModBlocks.BROWN_LICHEN);
    public static final DeferredItem<BlockItem> RUST_LICHEN = block(ModBlocks.RUST_LICHEN);
    public static final DeferredItem<BlockItem> OLD_MANS_BEARD = block(ModBlocks.OLD_MANS_BEARD);
    public static final DeferredItem<BlockItem> REINDEER_LICHEN = block(ModBlocks.REINDEER_LICHEN);
    public static final DeferredItem<BlockItem> FROST_MOSS_BLOCK = block(ModBlocks.FROST_MOSS_BLOCK);
    public static final DeferredItem<BlockItem> FROST_MOSS_CARPET = block(ModBlocks.FROST_MOSS_CARPET);
    public static final DeferredItem<BlockItem> SPHAGNUM_MOSS_BLOCK = block(ModBlocks.SPHAGNUM_MOSS_BLOCK);
    public static final DeferredItem<BlockItem> SPHAGNUM_MOSS_CARPET = block(ModBlocks.SPHAGNUM_MOSS_CARPET);
    public static final DeferredItem<DoubleHighBlockItem> COTTON_GRASS = tall(ModBlocks.COTTON_GRASS);
    public static final DeferredItem<BlockItem> ARCTIC_POPPY = block(ModBlocks.ARCTIC_POPPY);
    public static final DeferredItem<DoubleHighBlockItem> BRACKEN = tall(ModBlocks.BRACKEN);

    public static final DeferredItem<DoubleHighBlockItem> SASA_BAMBOO_GRASS = tall(ModBlocks.SASA_BAMBOO_GRASS);
    public static final DeferredItem<BlockItem> RED_SPIDER_LILY = block(ModBlocks.RED_SPIDER_LILY);
    public static final DeferredItem<DoubleHighBlockItem> JAPANESE_IRIS = tall(ModBlocks.JAPANESE_IRIS);
    public static final DeferredItem<BlockItem> BLUE_HYDRANGEA = block(ModBlocks.BLUE_HYDRANGEA);
    public static final DeferredItem<BlockItem> PINK_HYDRANGEA = block(ModBlocks.PINK_HYDRANGEA);
    public static final DeferredItem<PlaceOnWaterBlockItem> LOTUS_PAD = onWater(ModBlocks.LOTUS_PAD);
    public static final DeferredItem<PlaceOnWaterBlockItem> LOTUS_FLOWER = onWater(ModBlocks.LOTUS_FLOWER);

    public static final DeferredItem<DoubleHighBlockItem> MONSTERA = tall(ModBlocks.MONSTERA);
    public static final DeferredItem<BlockItem> BIRDS_NEST_FERN = block(ModBlocks.BIRDS_NEST_FERN);
    public static final DeferredItem<BlockItem> NEPENTHES = block(ModBlocks.NEPENTHES);
    public static final DeferredItem<BlockItem> RAFFLESIA = block(ModBlocks.RAFFLESIA);

    private ModItems() {
    }

    private static DeferredItem<BlockItem> block(DeferredBlock<? extends Block> block) {
        return ITEMS.registerSimpleBlockItem(block);
    }

    private static DeferredItem<DoubleHighBlockItem> tall(DeferredBlock<? extends Block> block) {
        return ITEMS.register(block.getId().getPath(), () -> new DoubleHighBlockItem(block.get(), new Item.Properties()));
    }

    private static DeferredItem<PlaceOnWaterBlockItem> onWater(DeferredBlock<? extends Block> block) {
        return ITEMS.register(block.getId().getPath(), () -> new PlaceOnWaterBlockItem(block.get(), new Item.Properties()));
    }
}
