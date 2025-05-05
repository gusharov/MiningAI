package test;

import java.net.InetSocketAddress;
import java.net.SocketAddress;
import java.util.UUID;

import org.geysermc.mcprotocollib.auth.GameProfile;
import org.geysermc.mcprotocollib.network.Session;
import org.geysermc.mcprotocollib.network.event.server.ServerAdapter;
import org.geysermc.mcprotocollib.network.event.server.SessionAddedEvent;
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

public class clienttest {

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
        //HandshakeIntent h = HandshakeIntent.LOGIN;
        String name = javaSession.getMcProfile().getName();
        UUID uuid = javaSession.getMcProfile().getId();
        String accessToken = javaSession.getMcProfile().getMcToken().getAccessToken();
        //gets necessary variables for "faking" a client
        System.out.println("Logged in as: " + name);
            
        MinecraftProtocol hhe = new MinecraftProtocol(new GameProfile(uuid, name), accessToken);
        //hhe.newClientSession(session); //look into this method
        //Create a ClientSession
        
                
        //try adding the client listeener to proxyclient and if that doesnt work add it to realclient
        SocketAddress bindAddress = new InetSocketAddress("127.0.0.1", 25565); // Localhost:25565
        NetworkServer proxy = new NetworkServer(bindAddress, MinecraftProtocol::new);
        ServerAdapter proxlissten = new ServerAdapter(){
            @Override
            public void sessionAdded(SessionAddedEvent event) {
                System.out.println("session joined");
                Session localsess = event.getSession();
                ClientNetworkSession clisession = ClientNetworkSessionFactory.factory()
                .setAddress("mc.minehut.com")
                .setProtocol(hhe)
                .create();
                localsess.addListener(new SessionAdapter(){
                    @Override
                    public void packetReceived(Session session, Packet packet) {
                        System.out.println("Local Client");
                        System.out.println("packet sent");
                        System.out.println("packet type: " + packet.getClass().getSimpleName());
                        clisession.send(packet);
                        
                    }
                    @Override
                    public void packetSent(Session session, Packet packet) {
                        System.out.println("Local Client");
                        System.out.println("packet recieved");
                        System.out.println("packet type: " + packet.getClass().getSimpleName());
                        
                    }
                });
                clisession.addListener(new SessionAdapter(){
                    @Override
                    public void packetReceived(Session session, Packet packet) {
                        System.out.println("Local Client");
                        System.out.println("packet sent");
                        System.out.println("packet type: " + packet.getClass().getSimpleName());
                        localsess.send(packet);
                        
                    }
                });
                
                
                
            }
        };
        proxy.addListener(proxlissten);
        proxy.bind();
    }
}