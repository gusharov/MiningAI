package test;

import java.net.InetSocketAddress;
import java.util.UUID;

import org.geysermc.mcprotocollib.auth.GameProfile;
import org.geysermc.mcprotocollib.network.Session;
import org.geysermc.mcprotocollib.network.event.server.ServerAdapter;
import org.geysermc.mcprotocollib.network.event.server.SessionAddedEvent;
import org.geysermc.mcprotocollib.network.event.session.DisconnectingEvent;
import org.geysermc.mcprotocollib.network.event.session.SessionAdapter;
import org.geysermc.mcprotocollib.network.factory.ClientNetworkSessionFactory;
import org.geysermc.mcprotocollib.network.packet.Packet;
import org.geysermc.mcprotocollib.network.server.NetworkServer;
import org.geysermc.mcprotocollib.network.session.ClientNetworkSession;
import org.geysermc.mcprotocollib.protocol.MinecraftProtocol;

import net.lenni0451.commons.httpclient.HttpClient;
import net.raphimc.minecraftauth.MinecraftAuth;
import net.raphimc.minecraftauth.step.java.session.StepFullJavaSession;
import net.raphimc.minecraftauth.step.msa.StepMsaDeviceCode;
public class MinecraftProxy {
    public static void main(String[] args) throws Exception {
        // 1) Authenticate once at startup
        HttpClient httpClient = MinecraftAuth.createHttpClient();
        StepFullJavaSession.FullJavaSession javaSession = MinecraftAuth.JAVA_DEVICE_CODE_LOGIN.getFromInput(
            httpClient,
            new StepMsaDeviceCode.MsaDeviceCodeCallback(code -> {
                System.out.println("Go to " + code.getVerificationUri());
                System.out.println("Enter code " + code.getUserCode());
                System.out.println("Direct link: " + code.getDirectVerificationUri());
            })
        );
        
        String name = javaSession.getMcProfile().getName();
        UUID uuid = javaSession.getMcProfile().getId();
        String accessToken = javaSession.getMcProfile().getMcToken().getAccessToken();
        System.out.println("Logged in as: " + name);
        String proxyHost = "localhost";
        int proxyPort = 25565;
        InetSocketAddress bindAddress = new InetSocketAddress(proxyHost, proxyPort);
        MinecraftProtocol hhe = new MinecraftProtocol(new GameProfile(uuid, name), accessToken);
        NetworkServer proxy = new NetworkServer(bindAddress, ()->hhe);
        System.out.println("1");
        ServerAdapter servlistener = new ServerAdapter(){
            @Override
            public void sessionAdded(SessionAddedEvent evt){
                Session clisession = evt.getSession();
                System.out.println("2");
                ClientNetworkSession serversession = ClientNetworkSessionFactory.factory()
                .setAddress("mc.minehut.com")
                .setProtocol(hhe)
                .create();
                System.out.println("3");
                serversession.connect();
                serversession.addListener(new SessionAdapter() {
                    @Override
                    public void packetReceived(Session session, Packet packet) {
                        System.out.println("Received packet: " + packet);
                        clisession.send(packet);
                    }

                    @Override
                    public void disconnecting(DisconnectingEvent event) {
                        serversession.disconnect("Server disconnected");
                    }
                });
                System.out.println("4");

                clisession.addListener(new SessionAdapter() {
                    @Override
                    public void packetReceived(Session session, Packet packet) {
                        serversession.send(packet);
                    }
                    @Override
                    public void disconnecting(DisconnectingEvent event) {
                        clisession.disconnect("Server disconnected");
                    }
                
                });
            }
        };
        proxy.addListener(servlistener);
        proxy.bind(true);
    }
}