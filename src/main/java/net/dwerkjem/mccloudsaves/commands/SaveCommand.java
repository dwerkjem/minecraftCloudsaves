package net.dwerkjem.mccloudsaves.commands;

import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import org.slf4j.Logger;
import net.dwerkjem.mccloudsaves.MCcloudsaves;

public class SaveCommand {
    private static final Logger LOGGER = MCcloudsaves.LOGGER;

    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(
            Commands.literal("save")
                .executes(context -> {
                    context.getSource().sendSuccess(() -> Component.literal("Save command executed"), false);
                    LOGGER.info("Save command executed by {}", context.getSource().getPlayerOrException().getName().getString());
                    return 1;
                })
        );
    }
}