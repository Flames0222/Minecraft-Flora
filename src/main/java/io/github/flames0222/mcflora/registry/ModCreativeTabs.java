package io.github.flames0222.mcflora.registry;

import io.github.flames0222.mcflora.McFlora;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, McFlora.MOD_ID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> FLORA = TABS.register("flora",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.mcflora"))
                    .icon(() -> new ItemStack(ModItems.RUST_LICHEN.get()))
                    .displayItems((params, output) -> ModItems.ITEMS.getEntries()
                            .forEach(item -> output.accept(item.get())))
                    .build());

    private ModCreativeTabs() {
    }
}
