package net.dwerkjem.mccloudsaves.commands;

import com.mojang.brigadier.CommandDispatcher;

import net.minecraft.commands.CommandSourceStack;
import static net.minecraft.commands.Commands.literal;

public class Auth {
    public Auth(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(
            literal("auth").executes(ctx -> {
                return 0;
            })
                    
        );
    }
    
}
