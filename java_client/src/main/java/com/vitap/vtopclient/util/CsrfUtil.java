package com.vitap.vtopclient.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CsrfUtil {
    private static final Pattern CSRF_PATTERN = Pattern.compile("name=\\"_csrf\\" value=\\"(.*?)\\"");

    public static String findCsrf(String html) {
        Matcher m = CSRF_PATTERN.matcher(html);
        if (m.find()) {
            return m.group(1);
        }
        return null;
    }
}
