package com.example.smartlock;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.JsonReader;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class TempActivity extends AppCompatActivity {

    private static final String TAG = "WeatherLog";

    private TextView descriptionText;
    private TextView tempText;
    private TextView humidText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_temp);
        tempText = findViewById(R.id.txtTemp);
        humidText = findViewById(R.id.txtHumid);
        descriptionText = findViewById(R.id.txtWeatherDescription);
    }

    public void disconnect(View v) {
        finish();
    }

    public void updateWeatherData(View v){
        Runnable r = new Runnable() {
            @Override
            public void run() {
                final JSONObject json = RemoteFetch.getJson(TempActivity.this);

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        renderWeather(json);
                    }
                });

            }
        };

        Thread t = new Thread(r);
        t.start();
    }

    public void renderWeather(JSONObject json) {
        try {
            JSONArray weather = json.getJSONArray("weather");
            JSONObject weatherInstance = weather.getJSONObject(0);

            String weatherDetails = weatherInstance.getString("description");
            JSONObject details = json.getJSONObject("main");
            String temperature = details.getString("temp");
            String humidity = details.getString("humidity");

            descriptionText.setText(weatherDetails.toUpperCase());
            tempText.setText(temperature + " °C");
            humidText.setText(humidity + " RH");
        }catch(JSONException e){
            e.printStackTrace();
            Log.d(TAG,"Error processing Json");
            Toast.makeText(this,"Error reading Json Data",Toast.LENGTH_SHORT).show();
        }

    }



}