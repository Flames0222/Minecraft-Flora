package io.github.flames0222.mcflora.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.HangingRootsBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * A plant that hangs from the underside of a sturdy block or from leaves.
 * Used for old man's beard lichen and nepenthes pitchers.
 */
public class HangingPlantBlock extends HangingRootsBlock {
    public HangingPlantBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        BlockPos above = pos.above();
        BlockState support = level.getBlockState(above);
        // Leaves have an empty support shape in vanilla, so they need an explicit allowance.
        return support.is(BlockTags.LEAVES) || support.isFaceSturdy(level, above, Direction.DOWN);
    }
}
