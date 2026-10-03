package io.github.flames0222.mcflora.block;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.DoublePlantBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Dense, two-block-tall undergrowth that slightly slows creatures pushing through it.
 */
public class BrackenBlock extends DoublePlantBlock {
    public static final MapCodec<BrackenBlock> CODEC = simpleCodec(BrackenBlock::new);
    private static final Vec3 SLOWDOWN = new Vec3(0.85, 1.0, 0.85);

    public BrackenBlock(Properties properties) {
        super(properties);
    }

    @Override
    public MapCodec<? extends DoublePlantBlock> codec() {
        return CODEC;
    }

    @Override
    protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (entity instanceof LivingEntity && !entity.isSpectator()) {
            entity.makeStuckInBlock(state, SLOWDOWN);
        }
    }
}
