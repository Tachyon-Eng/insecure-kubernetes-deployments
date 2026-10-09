package com.example.catapp.controllers;

import com.example.catapp.models.User;
import com.example.catapp.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import javax.servlet.http.HttpSession;

@Controller
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/register")
    public String registerForm(Model model) {
        return "register";
    }

    @PostMapping("/register")
    public String register(@RequestParam String username, @RequestParam String password, 
                          RedirectAttributes redirectAttributes, HttpSession session) {

        if (userRepository.findByUsername(username) != null) {
            redirectAttributes.addFlashAttribute("error", "Username already exists");
            return "redirect:/register";
        }

        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        userRepository.save(user);


        session.setAttribute("userId", user.getId());
        session.setAttribute("username", user.getUsername());

        redirectAttributes.addFlashAttribute("message", "Registration successful! Welcome " + username);
        return "redirect:/";
    }

    @GetMapping("/login")
    public String loginForm(HttpSession session, Model model) {

        if (session.getAttribute("userId") != null) {
            return "redirect:/";
        }
        return "login";
    }

    @PostMapping("/login")
    public String login(@RequestParam String username, @RequestParam String password, 
                       HttpSession session, Model model) {
        User user = userRepository.findByUsernameAndPassword(username, password);
        if (user != null) {

            session.setAttribute("userId", user.getId());
            session.setAttribute("username", user.getUsername());
            return "redirect:/";
        } else {
            model.addAttribute("error", "Invalid username or password");
            return "login";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/login";
    }


    @GetMapping("/profile")
    public String viewProfile(@RequestParam(required = false) Integer userId, 
                            HttpSession session, Model model) {

        if (userId == null) {
            userId = (Integer) session.getAttribute("userId");
            if (userId == null) {
                return "redirect:/login";
            }
        }


        User user = userRepository.findById(userId).orElse(null);
        if (user == null) {
            model.addAttribute("error", "User not found");
            model.addAttribute("title", "profile.html");
            model.addAttribute("content", "profile.html :: content");
            return "layout";
        }
        model.addAttribute("user", user);
        model.addAttribute("title", "profile.html");
        model.addAttribute("content", "profile.html :: content");
        return "layout";
    }


    @GetMapping("/editProfile")
    public String editProfileForm(@RequestParam(required = false) Integer userId, 
                                HttpSession session, Model model) {

        if (userId == null) {
            userId = (Integer) session.getAttribute("userId");
            if (userId == null) {
                return "redirect:/login";
            }
        }


        User user = userRepository.findById(userId).orElse(null);
        if (user == null) {
            model.addAttribute("error", "User not found");
            model.addAttribute("title", "editProfile.html");
            model.addAttribute("content", "editProfile.html :: content");
            return "layout";
        }
        model.addAttribute("user", user);
        model.addAttribute("title", "editProfile.html");
        model.addAttribute("content", "editProfile.html :: content");
        return "layout";
    }

    @PostMapping("/editProfile")
    public String editProfile(@RequestParam Integer userId, @RequestParam String username,
                            @RequestParam String password, RedirectAttributes redirectAttributes) {

        User user = userRepository.findById(userId).orElse(null);
        if (user != null) {
            user.setUsername(username);
            user.setPassword(password);
            userRepository.save(user);
            redirectAttributes.addFlashAttribute("message", "Profile updated successfully");
        } else {
            redirectAttributes.addFlashAttribute("error", "User not found");
        }
        return "redirect:/profile?userId=" + userId;
    }
}
