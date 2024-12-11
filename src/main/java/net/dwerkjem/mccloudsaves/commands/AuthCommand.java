// src/main/java/net/dwerkjem/mccloudsaves/commands/AuthCommand.java
package net.dwerkjem.mccloudsaves.commands;

import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import org.slf4j.Logger;
import net.dwerkjem.mccloudsaves.MCcloudsaves;

public class AuthCommand {
    private static final Logger LOGGER = MCcloudsaves.LOGGER;
    
    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(
            Commands.literal("auth")
                .executes(context -> {
                    context.getSource().sendSuccess(() -> Component.literal("Auth command executed"), false);
                    LOGGER.info("Auth command executed by {}", context.getSource().getPlayerOrException().getName().getString());
                    return 1;
                })
        );
    }
}