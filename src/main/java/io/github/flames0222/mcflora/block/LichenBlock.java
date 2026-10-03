package io.github.flames0222.mcflora.block;

import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.block.GlowLichenBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Multi-face lichen that crusts over rock and bark. Shares glow lichen's placement, waterlogging,
 * shears-only drops and bone meal spreading, but does not emit light (light comes from block properties).
 */
public class LichenBlock extends GlowLichenBlock {
    public LichenBlock(Properties properties) {
        super(properties);
    }

    /**
     * Glow lichen hard-codes its own item here; check this block's item instead so that clicking with
     * the same lichen adds a face, and a fully covered block is placed against like any other.
     */
    @Override
    protected boolean canBeReplaced(BlockState state, BlockPlaceContext context) {
        if (!context.getItemInHand().is(this.asItem())) {
            return true;
        }
        for (Direction direction : Direction.values()) {
            if (!hasFace(state, direction)) {
                return true;
            }
        }
        return false;
    }
}
