package io.github.flames0222.mcflora.block;

import com.mojang.serialization.MapCodec;
import io.github.flames0222.mcflora.registry.ModTags;
import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.BushBlock;
import net.minecraft.world.level.block.FarmBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * A simple single-block plant with a configurable outline shape and soil rule.
 */
public class FloraPlantBlock extends BushBlock {
    private final VoxelShape shape;
    private final Soil soil;

    public FloraPlantBlock(Properties properties, VoxelShape shape, Soil soil) {
        super(properties);
        this.shape = shape;
        this.soil = soil;
    }

    @Override
    protected MapCodec<? extends BushBlock> codec() {
        return simpleCodec(p -> new FloraPlantBlock(p, shape, soil));
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        Vec3 offset = state.getOffset(level, pos);
        return shape.move(offset.x, offset.y, offset.z);
    }

    @Override
    protected boolean mayPlaceOn(BlockState state, BlockGetter level, BlockPos pos) {
        return soil.test(state);
    }

    public enum Soil {
        /** Vanilla bush rules: any dirt-like block or farmland. */
        DIRT,
        /** Cold-climate plants: dirt plus anything in {@code #mcflora:tundra_plantable} (snow, gravel, stone, moss). */
        TUNDRA;

        public boolean test(BlockState state) {
            boolean dirt = state.is(BlockTags.DIRT) || state.getBlock() instanceof FarmBlock;
            return dirt || this == TUNDRA && state.is(ModTags.TUNDRA_PLANTABLE);
        }
    }
}
