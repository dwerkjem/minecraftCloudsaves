package net.dwerkjem.mccloudsaves;

import com.mojang.logging.LogUtils;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;

@Mod(MCcloudsaves.MOD_ID)
public class MCcloudsaves {
    public static final String MOD_ID = "mccloudsaves";
    public static final Logger LOGGER = LogUtils.getLogger();

    public MCcloudsaves() {
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        MinecraftForge.EVENT_BUS.register(this);
    }
}
