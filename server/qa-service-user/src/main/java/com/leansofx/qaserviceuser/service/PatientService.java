package com.leansofx.qaserviceuser.service;

import com.leansofx.qaserviceuser.dto.PatientResponse;
import com.leansofx.qaserviceuser.repository.PatientRepository;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class PatientService {

    private final PatientRepository patientRepository;

    public PatientService(PatientRepository patientRepository) {
        this.patientRepository = patientRepository;
    }

    public Optional<PatientResponse> login(String username, String password) {
        return patientRepository.findByUsernameAndPassword(username, password)
                .map(PatientResponse::from);
    }
}
