package com.leansofx.qaserviceuser.controller;

import com.leansofx.qaserviceuser.dto.DoctorResponse;
import com.leansofx.qaserviceuser.service.DoctorService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/doctors")
public class DoctorController {

    private final DoctorService doctorService;

    public DoctorController(DoctorService doctorService) {
        this.doctorService = doctorService;
    }

    @GetMapping
    public Map<String, Object> listDoctors() {
        List<DoctorResponse> doctors = doctorService.listDoctors();
        Map<String, Object> response = new HashMap<>();
        response.put("code", 0);
        response.put("message", "ok");
        response.put("data", doctors);
        return response;
    }
}
