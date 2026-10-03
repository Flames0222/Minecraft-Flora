package io.github.flames0222.mcflora.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * A flower that can also root on snow, gravel and bare stone, like real alpine and arctic flowers.
 */
public class TundraFlowerBlock extends FlowerBlock {
    public TundraFlowerBlock(Holder<MobEffect> effect, float seconds, Properties properties) {
        super(effect, seconds, properties);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return FloraPlantBlock.Soil.TUNDRA.test(state);
    }
}
