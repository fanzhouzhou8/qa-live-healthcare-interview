package com.leansofx.qaserviceuser.controller;

import com.leansofx.qaserviceuser.dto.PatientLoginRequest;
import com.leansofx.qaserviceuser.dto.PatientResponse;
import com.leansofx.qaserviceuser.service.PatientService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/patients")
public class PatientController {

    private final PatientService patientService;

    public PatientController(PatientService patientService) {
        this.patientService = patientService;
    }

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody PatientLoginRequest request) {
        Map<String, Object> response = new HashMap<>();

        if (request.getUsername() == null || request.getUsername().isBlank()
                || request.getPassword() == null || request.getPassword().isBlank()) {
            response.put("code", 400);
            response.put("message", "用户名和密码不能为空");
            response.put("data", null);
            return response;
        }

        Optional<PatientResponse> patient = patientService.login(
                request.getUsername().trim(),
                request.getPassword()
        );

        if (patient.isEmpty()) {
            response.put("code", 401);
            response.put("message", "用户名或密码错误");
            response.put("data", null);
            return response;
        }

        response.put("code", 0);
        response.put("message", "ok");
        response.put("data", patient.get());
        return response;
    }
}
