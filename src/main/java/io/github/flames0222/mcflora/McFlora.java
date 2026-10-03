package io.github.flames0222.mcflora;

import com.mojang.logging.LogUtils;
import io.github.flames0222.mcflora.registry.ModBlocks;
import io.github.flames0222.mcflora.registry.ModCreativeTabs;
import io.github.flames0222.mcflora.registry.ModItems;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.FireBlock;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import org.slf4j.Logger;

@Mod(McFlora.MOD_ID)
public final class McFlora {
    public static final String MOD_ID = "mcflora";
    public static final Logger LOGGER = LogUtils.getLogger();

    public McFlora(IEventBus modBus, ModContainer container) {
        ModBlocks.BLOCKS.register(modBus);
        ModItems.ITEMS.register(modBus);
        ModCreativeTabs.TABS.register(modBus);
        modBus.addListener(this::commonSetup);
    }

    private void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            FireBlock fire = (FireBlock) Blocks.FIRE;
            ModBlocks.flammablePlants().forEach(block -> fire.setFlammable(block.get(), 60, 100));
            ModBlocks.flammableMosses().forEach(block -> fire.setFlammable(block.get(), 5, 20));
        });
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
    }
}
