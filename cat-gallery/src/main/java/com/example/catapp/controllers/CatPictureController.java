package com.example.catapp.controllers;

import com.example.catapp.models.CatPicture;
import com.example.catapp.repositories.CatPictureRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@Controller
public class CatPictureController {

    @Autowired
    private CatPictureRepository catPictureRepository;

    @GetMapping("/search")
    public String searchForm() {
        return "search";
    }

    @PostMapping("/search")
    public String search(@RequestParam String name, Model model) {
        List<CatPicture> results = catPictureRepository.findByNameQuery(name);
        model.addAttribute("pictures", results);
        return "searchResults";
    }

    @GetMapping("/delete")
    public String deleteForm() {
        return "delete";
    }

    @PostMapping("/delete")
    public String deletePicture(@RequestParam int id, Model model) {
        catPictureRepository.deleteById(id);
        model.addAttribute("message", "Picture deleted");
        return "deleteResult";
    }
}
