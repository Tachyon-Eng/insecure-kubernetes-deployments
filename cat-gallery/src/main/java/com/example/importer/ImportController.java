package com.example.importer;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;

@RestController
public class ImportController {

    @PostMapping("/import")
    public ResponseEntity<String> importObject(@RequestBody byte[] data) {
        try {
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
            Object importedObject = ois.readObject();
            return ResponseEntity.ok("Object imported: " + importedObject.toString());
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Import failed");
        }
    }
}
