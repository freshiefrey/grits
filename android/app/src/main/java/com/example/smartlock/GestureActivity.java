package com.example.smartlock;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.media.Ringtone;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Vibrator;

public class GestureActivity extends AppCompatActivity {

    private static final int requestCode = 100;
    private static final String TAG = "GestureLog";

    private static final String COMMAND = "COMMAND";
    private static final String DISCONNECT = "DISCONNECT";
    private static final String GESTURE = "RESULT";

    private TextView resultText;
    private View mainScreen;

    public static final String mBroadcastGestureResult = "gestureResults";
    private IntentFilter mIntentFilter;


    private boolean isLight = false;
    private boolean flashLightStatus;
    private boolean hasCameraFlash;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gesture);
        resultText = findViewById(R.id.txtResult);
        mainScreen = findViewById(R.id.screen);

        mIntentFilter = new IntentFilter();
        mIntentFilter.addAction(mBroadcastGestureResult);

        hasCameraFlash = getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA_FLASH);
        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_DENIED) {
            ActivityCompat.requestPermissions(GestureActivity.this, new String[]{Manifest.permission.CAMERA}, requestCode);
        }

    }

    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(mReceiver, mIntentFilter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(mReceiver);
    }

    public void test(View v) {
        swipeScreen();
    }

    private BroadcastReceiver mReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            //Result code here
            if (intent.getAction().equals(mBroadcastGestureResult)) {
                Bundle data = intent.getExtras();
                String gestureResult = data.getString(GESTURE);
                resultText.setText(gestureResult);

                if (gestureResult.equals("Buddha clap")) {
                    gestureResult = Gesture.BuddhaClap.toString();
                }

                if (gestureResult.equals(Gesture.Knob.toString())) {
                    toggleLightDark();
                } else if (gestureResult.equals(Gesture.Swipe.toString())) {
                    swipeScreen();
                } else if (gestureResult.equals(Gesture.BuddhaClap.toString())) {
                    toggleFlash();
                } else if (gestureResult.equals(Gesture.Pushback.toString())) {
                   ringtone();
                   vibrate();
                } else {
                    resultText.setText(R.string.Unknown);
                }
            }
        }
    };

    public void vibrate() {
        Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);

        // Output yes if can vibrate, no otherwise
        if (vibrator.hasVibrator()) {
            Log.v("Can Vibrate", "YES");
        } else {
            Log.v("Can Vibrate", "NO");
        }

        vibrator.vibrate(2000);
    }

    public void ringtone(){
        Uri notification = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);
        Ringtone r = RingtoneManager.getRingtone(getApplicationContext(), notification);
        r.play();
    }

    //Swipe gesture
    public void swipeScreen() {
        Intent tempIntent = new Intent(GestureActivity.this, TempActivity.class);
        startActivity(tempIntent);
    }

    //Knob gesture
    public void toggleLightDark() {
        if (isLight) {
            isLight = false;
            mainScreen.setBackgroundColor(Color.parseColor("#000000"));
        } else {
            isLight = true;
            mainScreen.setBackgroundColor(Color.parseColor("#ffffbb33"));
        }
    }


    //Buddha clap gesture
    public void toggleFlash() {
        if (hasCameraFlash) {
            if (flashLightStatus)
                flashLightOff();
            else
                flashLightOn();
        } else {
            Toast.makeText(GestureActivity.this, "No flash available on your device",
                    Toast.LENGTH_SHORT).show();
        }
    }

    private void flashLightOn() {
        CameraManager cameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
        try {
            String cameraId = cameraManager.getCameraIdList()[0];
            cameraManager.setTorchMode(cameraId, true);
            flashLightStatus = true;
        } catch (CameraAccessException e) {
            Log.d(TAG, "Error activating flashlight!");
        }
    }

    private void flashLightOff() {
        CameraManager cameraManager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
        try {
            String cameraId = cameraManager.getCameraIdList()[0];
            cameraManager.setTorchMode(cameraId, false);
            flashLightStatus = false;
        } catch (CameraAccessException e) {
            Log.d(TAG, "Error deactivating flashlight!");
        }
    }

    public void disconnect(View v) {
        Intent disconnectIntent = new Intent(this, MqttHelper.class);
        disconnectIntent.putExtra(COMMAND, DISCONNECT);
        startService(disconnectIntent);
        Toast.makeText(getBaseContext(), "Disconnect from broker", Toast.LENGTH_SHORT).show();
        finish();
    }
}