package com.example.smartlock;

import android.content.Context;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class RemoteFetch {

    private static final String weatherURL
            = "https://api.openweathermap.org/data/2.5/weather?id={apiKey}";
    private static final String TAG = "APILog";

    public static JSONObject getJson(Context context) {

        try {
            URL url = new URL(weatherURL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));


            StringBuffer json = new StringBuffer(1024);
            String tmp = "";
            while ((tmp = reader.readLine()) != null)
                json.append(tmp).append("\n");
            reader.close();

            JSONObject data = new JSONObject(json.toString());

            if (data.getInt("cod") != 200) {
                return null;
            }

            return data;

        } catch (MalformedURLException e) {
            Log.d(TAG, "Error forming URL!");
            return null;
        } catch (IOException e) {
            Log.d(TAG, "Error forming HTTP Connection!");
            return null;
        } catch (JSONException e) {
            Log.d(TAG, "Error forming JSON object!");
            return null;
        }

    }
}
