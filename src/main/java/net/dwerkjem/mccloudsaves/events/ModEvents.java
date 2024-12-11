package net.dwerkjem.mccloudsaves.events;

import com.mojang.brigadier.CommandDispatcher;
import net.dwerkjem.mccloudsaves.MCcloudsaves;
import net.minecraft.commands.CommandSourceStack;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import org.slf4j.Logger;
import net.dwerkjem.mccloudsaves.commands.*;

@Mod.EventBusSubscriber(modid = MCcloudsaves.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ModEvents {
    private static final Logger LOGGER = MCcloudsaves.LOGGER;

    @SubscribeEvent
    public static void onCommandsRegister(RegisterCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
        
        AuthCommand.register(dispatcher);
        SaveCommand.register(dispatcher);
        LoadCommand.register(dispatcher);

        LOGGER.info("All commands registered successfully.");
    }
}