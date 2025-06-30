package com.vitap.vtopclient.model;

public class LoggedInStudent {
    private final String registrationNumber;
    private final String csrfToken;

    public LoggedInStudent(String registrationNumber, String csrfToken) {
        this.registrationNumber = registrationNumber;
        this.csrfToken = csrfToken;
    }

    public String getRegistrationNumber() {
        return registrationNumber;
    }

    public String getCsrfToken() {
        return csrfToken;
    }
}
