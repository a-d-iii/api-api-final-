package com.vitap.vtopclient.login;

import com.vitap.vtopclient.constants.Constants;
import com.vitap.vtopclient.model.LoggedInStudent;
import com.vitap.vtopclient.util.CsrfUtil;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class LoginService {
    private final HttpClient httpClient = HttpClient.newBuilder().build();

    public LoggedInStudent login(String registrationNumber, String password) throws IOException, InterruptedException {
        // Step 1: fetch CSRF token
        HttpRequest csrfReq = HttpRequest.newBuilder()
                .uri(URI.create(Constants.BASE_URL + Constants.CSRF_ROUTE))
                .GET()
                .build();
        HttpResponse<String> csrfResp = httpClient.send(csrfReq, HttpResponse.BodyHandlers.ofString());
        String csrf = CsrfUtil.findCsrf(csrfResp.body());
        if (csrf == null) {
            throw new IOException("Unable to fetch CSRF token");
        }

        // Step 2: send login request
        String form = "_csrf=" + csrf + "&username=" + registrationNumber + "&password=" + password;
        HttpRequest loginReq = HttpRequest.newBuilder()
                .uri(URI.create(Constants.BASE_URL + Constants.LOGIN_ROUTE))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(form))
                .build();

        HttpResponse<String> loginResp = httpClient.send(loginReq, HttpResponse.BodyHandlers.ofString());
        if (loginResp.statusCode() != 200) {
            throw new IOException("Login failed: status " + loginResp.statusCode());
        }

        return new LoggedInStudent(registrationNumber, csrf);
    }
}
