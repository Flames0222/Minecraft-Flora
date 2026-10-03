package io.github.flames0222.mcflora.block;

import net.minecraft.world.level.block.GlowLichenBlock;

/**
 * Multi-face lichen that crusts over rock and bark. Shares glow lichen's placement, waterlogging,
 * shears-only drops and bone meal spreading, but does not emit light (light comes from block properties).
 */
public class LichenBlock extends GlowLichenBlock {
    public LichenBlock(Properties properties) {
        super(properties);
    }
}
