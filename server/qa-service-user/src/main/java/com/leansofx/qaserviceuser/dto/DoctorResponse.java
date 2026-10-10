package com.leansofx.qaserviceuser.dto;

import com.leansofx.qaserviceuser.entity.Doctor;

import java.util.List;

public class DoctorResponse {

    private String id;
    private String username;
    private String name;
    private String title;
    private String department;
    private String avatar;
    private String experience;
    private List<String> specialties;
    private Boolean isActive;

    public static DoctorResponse from(Doctor doctor) {
        DoctorResponse response = new DoctorResponse();
        response.id = doctor.getId();
        response.username = doctor.getUsername();
        response.name = doctor.getName();
        response.title = doctor.getTitle();
        response.department = doctor.getDepartment();
        response.avatar = doctor.getAvatar();
        response.experience = doctor.getExperience();
        response.specialties = doctor.getSpecialties();
        response.isActive = doctor.getIsActive();
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

    public String getTitle() {
        return title;
    }

    public String getDepartment() {
        return department;
    }

    public String getAvatar() {
        return avatar;
    }

    public String getExperience() {
        return experience;
    }

    public List<String> getSpecialties() {
        return specialties;
    }

    public Boolean getIsActive() {
        return isActive;
    }
}
