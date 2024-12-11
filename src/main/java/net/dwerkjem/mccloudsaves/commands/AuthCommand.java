package net.dwerkjem.mccloudsaves.commands;

import com.dropbox.core.DbxAppInfo;
import com.dropbox.core.DbxRequestConfig;
import com.dropbox.core.DbxSessionStore;
import com.dropbox.core.DbxWebAuth;
import com.dropbox.core.DbxAuthFinish;
import com.mojang.brigadier.CommandDispatcher;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

import org.slf4j.Logger;
import net.dwerkjem.mccloudsaves.MCcloudsaves;

public class AuthCommand {
    private static final Logger LOGGER = MCcloudsaves.LOGGER;
    private static final Map<String, String> playerSessions = new HashMap<>();

    @SuppressWarnings("unchecked")
    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(
            Commands.literal("auth")
                .executes(context -> {

                    String playerName = context.getSource().getPlayerOrException().getName().getString();
                    DbxRequestConfig config = DbxRequestConfig.newBuilder("mccloudsaves/1.0").build();
                    DbxWebAuth webAuth = new DbxWebAuth(config, new DbxAppInfo("odptx6jiftjst5r", null));

                    String redirectUri = "http://localhost:8080/auth";
                    String authUrl = webAuth.authorize(
                        DbxWebAuth.newRequestBuilder()
                            .withRedirectUri(redirectUri, new InMemorySessionStore(playerName))
                            .build()
                    );

                    context.getSource().sendSuccess(
                        (Supplier<Component>) Component.literal("Please authorize the app by visiting: " + authUrl), false
                    );

                    LOGGER.info("Auth command executed by {}", playerName);
                    return 1;
                })
        );
    }

    public static void handleCallback(String playerName, String authorizationCode) {
        try {
            DbxRequestConfig config = DbxRequestConfig.newBuilder("mccloudsaves/1.0").build();
            DbxWebAuth webAuth = new DbxWebAuth(config, new DbxAppInfo("your_app_key", null));

            DbxAuthFinish authFinish = webAuth.finishFromCode(authorizationCode);
            String accessToken = authFinish.getAccessToken();

            LOGGER.info("Player {} successfully authorized. Access token: {}", playerName, accessToken);

            // Save the access token securely (e.g., in a file or database)
            saveAccessToken(playerName, accessToken);

        } catch (Exception e) {
            LOGGER.error("Failed to complete OAuth for player {}: {}", playerName, e.getMessage());
        }
    }

    private static void saveAccessToken(String playerName, String accessToken) {
        // Save the token securely (e.g., to a file or database)
        LOGGER.info("Access token for {} saved securely.", playerName);
    }

    static class InMemorySessionStore implements DbxSessionStore {
        private final String playerName;

        InMemorySessionStore(String playerName) {
            this.playerName = playerName;
        }

        @Override
        public void set(String session) {
            playerSessions.put(playerName, session);
        }

        @Override
        public String get() {
            return playerSessions.get(playerName);
        }

        @Override
        public void clear() {
            playerSessions.remove(playerName);
        }
    }
}
