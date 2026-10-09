import java.io.*;

public class ImportFixture implements Serializable {
    private void readObject(ObjectInputStream ois) throws ClassNotFoundException, IOException {
        Runtime.getRuntime().exec("touch /tmp/import_complete");
    }

    public static void main(String[] args) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("payload.bin"))) {
            oos.writeObject(new ImportFixture());
        }
    }
}
