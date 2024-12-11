package net.dwerkjem.mccloudsaves.events;

import com.mojang.brigadier.CommandDispatcher;
import net.dwerkjem.mccloudsaves.MCcloudsaves;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraft.server.level.ServerPlayer;
import org.slf4j.Logger;

@Mod.EventBusSubscriber(modid = MCcloudsaves.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ModEvents {

    private static final Logger LOGGER = MCcloudsaves.LOGGER;

    // Command Registration
    @SubscribeEvent
    public static void onCommandsRegister(RegisterCommandsEvent event) {
        CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
        
        // Register the "auth" command
        dispatcher.register(
            Commands.literal("auth")
                .executes(context -> {
                    context.getSource().sendSuccess(() -> Component.literal("Auth command executed"), false);
                    LOGGER.info("Auth command executed by {}", context.getSource().getPlayerOrException().getName().getString());
                    return 1;
                })
        );

        // Register the "save" command
        dispatcher.register(
            Commands.literal("save")
                .executes(context -> {
                    context.getSource().sendSuccess(() -> Component.literal("Save command executed"), false);
                    LOGGER.info("Save command executed by {}", context.getSource().getPlayerOrException().getName().getString());
                    return 1;
                })
        );

        // Register the "load" command
        dispatcher.register(
            Commands.literal("load")
                .executes(context -> {
                    context.getSource().sendSuccess(() -> Component.literal("Load command executed"), false);
                    LOGGER.info("Load command executed by {}", context.getSource().getPlayerOrException().getName().getString());
                    return 1;
                })
        );

        LOGGER.info("All commands registered successfully.");
    }

    // Player Join Event
    @SubscribeEvent
    public static void onPlayerJoin(PlayerEvent.PlayerLoggedInEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        player.sendSystemMessage(Component.literal("Welcome to the server!"));
        LOGGER.info("Player {} has joined the server.", player.getName().getString());
    }
}