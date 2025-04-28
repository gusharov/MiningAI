package test;

import java.util.UUID;

import org.geysermc.mcprotocollib.auth.GameProfile;
import org.geysermc.mcprotocollib.network.Session;
import org.geysermc.mcprotocollib.network.event.session.ConnectedEvent;
import org.geysermc.mcprotocollib.network.event.session.DisconnectedEvent;
import org.geysermc.mcprotocollib.network.event.session.SessionAdapter;
import org.geysermc.mcprotocollib.network.factory.ClientNetworkSessionFactory;
import org.geysermc.mcprotocollib.network.packet.Packet;
import org.geysermc.mcprotocollib.network.session.ClientNetworkSession;
import org.geysermc.mcprotocollib.protocol.MinecraftProtocol;

import net.lenni0451.commons.httpclient.HttpClient;
import net.raphimc.minecraftauth.MinecraftAuth;
import net.raphimc.minecraftauth.step.java.session.StepFullJavaSession;
import net.raphimc.minecraftauth.step.msa.StepMsaDeviceCode;

public class MinecraftClient {

    public static void main(String[] args) throws Exception {
        HttpClient httpClient = MinecraftAuth.createHttpClient();
        StepFullJavaSession.FullJavaSession javaSession = MinecraftAuth.JAVA_DEVICE_CODE_LOGIN.getFromInput(
            httpClient,
            new StepMsaDeviceCode.MsaDeviceCodeCallback(code -> {
                System.out.println("Go to " + code.getVerificationUri());
                System.out.println("Enter code " + code.getUserCode());
                System.out.println("Direct link: " + code.getDirectVerificationUri());
            })
        );
        //the above authenticates and gets an access token
        String name = javaSession.getMcProfile().getName();
        UUID uuid = javaSession.getMcProfile().getId();
        String accessToken = javaSession.getMcProfile().getMcToken().getAccessToken();
        //gets necessary variables for "faking" a client
        System.out.println("Logged in as: " + name);

        MinecraftProtocol hhe = new MinecraftProtocol(new GameProfile(uuid, name), accessToken);
        //hhe.newClientSession(session); //look into this method
        // Create a ClientSession
        ClientNetworkSession clisession = ClientNetworkSessionFactory.factory()
                .setAddress("mc.minehut.com")
                .setProtocol(hhe)
                .create();

        // Add event listeners
        clisession.addListener(new SessionAdapter() {
            @Override
            public void connected(ConnectedEvent event) {
                // TODO Auto-generated method stub
                System.out.print("connected!");
            }
            @Override
            public void packetReceived(Session session, Packet packet) {
                System.out.println("Received packet: " + packet.getClass().getSimpleName() + " " + packet);
            }
            @Override
            public void packetSent(Session session, Packet packet) {
                System.out.println("Received packet: " + packet.getClass().getSimpleName() + " " + packet);
            }
            @Override
            public void disconnected(DisconnectedEvent event) {
                System.out.println("Disconnected: " + event.getReason() );
            }
        });

        // Connect to the server
        clisession.connect(true);
        while (clisession.isConnected()) {
            // Keep the session alive
            try {
                Thread.sleep(100); // Sleep to reduce CPU usage
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}