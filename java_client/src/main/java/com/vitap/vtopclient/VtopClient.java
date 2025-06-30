package com.vitap.vtopclient;

import com.vitap.vtopclient.login.LoginService;
import com.vitap.vtopclient.model.LoggedInStudent;
import com.vitap.vtopclient.attendance.AttendanceService;
import com.vitap.vtopclient.biometric.BiometricService;
import com.vitap.vtopclient.examschedule.ExamScheduleService;
import com.vitap.vtopclient.marks.MarksService;
import com.vitap.vtopclient.mentor.MentorService;
import com.vitap.vtopclient.profile.ProfileService;
import com.vitap.vtopclient.timetable.TimetableService;
import com.vitap.vtopclient.gradehistory.GradeHistoryService;
import com.vitap.vtopclient.outing.OutingService;
import com.vitap.vtopclient.payments.PaymentService;

import java.io.Closeable;
import java.io.IOException;

/**
 * Simplified Java version of the Python VtopClient.
 * Only a few methods are implemented as an example.
 */
public class VtopClient implements Closeable {
    private final String registrationNumber;
    private final String password;
    private LoggedInStudent loggedInStudent;
    private final LoginService loginService = new LoginService();

    // Services replicating Python modules
    private final AttendanceService attendanceService = new AttendanceService();
    private final BiometricService biometricService = new BiometricService();
    private final TimetableService timetableService = new TimetableService();
    private final GradeHistoryService gradeHistoryService = new GradeHistoryService();
    private final MentorService mentorService = new MentorService();
    private final ProfileService profileService = new ProfileService();
    private final ExamScheduleService examScheduleService = new ExamScheduleService();
    private final MarksService marksService = new MarksService();
    private final OutingService outingService = new OutingService();
    private final PaymentService paymentService = new PaymentService();

    public VtopClient(String registrationNumber, String password) {
        this.registrationNumber = registrationNumber;
        this.password = password;
    }

    /** Perform login and store session info */
    public void login() throws IOException, InterruptedException {
        loggedInStudent = loginService.login(registrationNumber, password);
    }

    public boolean isLoggedIn() {
        return loggedInStudent != null;
    }

    /** Fetch attendance */
    public String getAttendance(String semSubId) throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return attendanceService.fetchAttendance(
                loggedInStudent.getRegistrationNumber(),
                semSubId,
                loggedInStudent.getCsrfToken());
    }

    /** Fetch profile */
    public String getProfile() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return profileService.fetchProfile(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getBiometric(String date) throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return biometricService.fetchBiometric(
                loggedInStudent.getRegistrationNumber(),
                date,
                loggedInStudent.getCsrfToken());
    }

    public String getTimetable(String semSubId) throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return timetableService.fetchTimetable(
                loggedInStudent.getRegistrationNumber(),
                semSubId,
                loggedInStudent.getCsrfToken());
    }

    public String getGradeHistory() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return gradeHistoryService.fetchGradeHistory(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getMentor() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return mentorService.fetchMentor(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getExamSchedule(String semSubId) throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return examScheduleService.fetchExamSchedule(
                loggedInStudent.getRegistrationNumber(),
                semSubId,
                loggedInStudent.getCsrfToken());
    }

    public String getMarks(String semSubId) throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return marksService.fetchMarks(
                loggedInStudent.getRegistrationNumber(),
                semSubId,
                loggedInStudent.getCsrfToken());
    }

    public String getWeekendOutings() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return outingService.fetchWeekendOutings(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getGeneralOutings() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return outingService.fetchGeneralOutings(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getPendingPayments() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return paymentService.fetchPendingPayments(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    public String getPaymentReceipts() throws IOException {
        if (!isLoggedIn()) {
            throw new IOException("Not logged in");
        }
        return paymentService.fetchPaymentReceipts(
                loggedInStudent.getRegistrationNumber(),
                loggedInStudent.getCsrfToken());
    }

    @Override
    public void close() throws IOException {
        // Nothing to close in this simplified version
    }
}
