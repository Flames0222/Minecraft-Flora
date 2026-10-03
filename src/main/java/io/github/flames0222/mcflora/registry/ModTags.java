package io.github.flames0222.mcflora.registry;

import io.github.flames0222.mcflora.McFlora;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.block.Block;

public final class ModTags {
    /** Blocks that tundra plants (reindeer lichen, arctic poppy) can root in besides dirt. */
    public static final TagKey<Block> TUNDRA_PLANTABLE = TagKey.create(Registries.BLOCK, McFlora.id("tundra_plantable"));

    private ModTags() {
    }
}
