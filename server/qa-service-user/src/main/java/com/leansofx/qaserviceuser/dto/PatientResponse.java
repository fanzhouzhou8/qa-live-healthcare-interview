package com.leansofx.qaserviceuser.dto;

import com.leansofx.qaserviceuser.entity.Patient;

import java.time.LocalDate;

public class PatientResponse {

    private String id;
    private String username;
    private String name;
    private LocalDate birthday;
    private String phone;
    private String gender;

    public static PatientResponse from(Patient patient) {
        PatientResponse response = new PatientResponse();
        response.id = patient.getId();
        response.username = patient.getUsername();
        response.name = patient.getName();
        response.birthday = patient.getBirthday();
        response.phone = patient.getPhone();
        response.gender = patient.getGender();
        return response;
    }

    public String getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getName() {
        return name;
    }

    public LocalDate getBirthday() {
        return birthday;
    }

    public String getPhone() {
        return phone;
    }

    public String getGender() {
        return gender;
    }
}
