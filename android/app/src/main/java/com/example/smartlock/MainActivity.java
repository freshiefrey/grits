package com.example.smartlock;

import androidx.appcompat.app.AppCompatActivity;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    public static final String mBroadcastLoginSuccess = "loginSuccess";
    public static final String mBroadcastLoginFailure = "loginFailure";

    private static final String TAG = "LoginActivityLog";
    private static final String COMMAND = "COMMAND";
    private static final String CONNECT = "CONNECT";
    private static final String USERID = "USERID";
    private static final String PASSWORD = "PASSWORD";

    private IntentFilter mIntentFilter;
    private EditText editUserId;
    private EditText editPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        editUserId = findViewById(R.id.editTxtUserId);
        editPassword = findViewById(R.id.editTxtPassword);
        mIntentFilter = new IntentFilter();
        mIntentFilter.addAction(mBroadcastLoginSuccess);
        mIntentFilter.addAction(mBroadcastLoginFailure);
    }

    @Override
    protected void onResume() {
        super.onResume();
        registerReceiver(mReceiver, mIntentFilter);
    }

    public void login(View v) {
        String userId = editUserId.getText().toString();
        String password = editPassword.getText().toString();

        if (userId.matches("") || password.matches("")) {
            Toast.makeText(getBaseContext(), "Some fields are missing!", Toast.LENGTH_SHORT).show();
        } else {
            Intent connectIntent = new Intent(this, MqttHelper.class);
            connectIntent.putExtra(COMMAND, CONNECT);
            connectIntent.putExtra(USERID, userId);
            connectIntent.putExtra(PASSWORD, password);
            startService(connectIntent);
        }
    }

    private BroadcastReceiver mReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals(mBroadcastLoginSuccess)) {
                Toast.makeText(getBaseContext(), "Successful login", Toast.LENGTH_SHORT).show();
                editUserId.getText().clear();
                editPassword.getText().clear();
                Log.d(TAG, "Connection to Broker Success");
                Intent gestureIntent = new Intent(MainActivity.this,GestureActivity.class);
                startActivity(gestureIntent);
            } else if (intent.getAction().equals(mBroadcastLoginFailure)) {
                Toast.makeText(getBaseContext(), "Wrong user details, please try again!", Toast.LENGTH_SHORT).show();
                Log.d(TAG, "Connection to Broker Failure");
            }
        }
    };
}