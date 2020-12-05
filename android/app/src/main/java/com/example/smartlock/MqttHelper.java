package com.example.smartlock;

import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;

import java.io.UnsupportedEncodingException;
import java.util.Arrays;

public class MqttHelper extends Service {

    private static final String URL = "tcp://54.255.221.131";
    private static final String TAG = "MqttLog";

    private static final String COMMAND = "COMMAND";
    private static final String CONNECT = "CONNECT";
    private static final String DISCONNECT = "DISCONNECT";

    private static final String USERID = "USERID";
    private static final String PASSWORD = "PASSWORD";

    private static final String GESTURETOPIC = "GRITS/Gesture";
    private static final String[] TOPICLIST = {GESTURETOPIC};

    private MqttAndroidClient client;

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        Bundle extras = intent.getExtras();
        if (extras != null) {
            String command = extras.getString(COMMAND);
            if (command.equals(CONNECT)) {
                String userId = extras.getString(USERID);
                String password = extras.getString(PASSWORD);
                client = createMqttAndroidClient();
                MqttConnectOptions options = createMqttConnectOptions(userId, password);
                connect(options);

            } else if (command.equals(DISCONNECT)) {
                unSubscribe(TOPICLIST);
                disconnect();
            }
            /*else if (command.equals(TEMPERATURE)) {
                publish(SENSORTOPIC, "TEMP");
            }*/
        }
        return START_STICKY;
    }

    private MqttConnectOptions createMqttConnectOptions(String userId, String password) {
        MqttConnectOptions options = new MqttConnectOptions();
        options.setUserName(userId);
        options.setPassword(password.toCharArray());
        return options;
    }

    private MqttAndroidClient createMqttAndroidClient() {
        //create and return client
        String clientId = MqttClient.generateClientId();
        return new MqttAndroidClient(this.getApplicationContext(), URL, clientId);
    }

    public void connect(MqttConnectOptions options) {
        // Try to connect
        final Intent broadcastIntent = new Intent();
        try {
            if (!client.isConnected()) {
                IMqttToken token = client.connect(options);
                token.setActionCallback(new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        // We are connected
                        broadcastIntent.setAction(MainActivity.mBroadcastLoginSuccess);
                        sendBroadcast(broadcastIntent);
                        Log.d(TAG, "Connection Success");
                        subscribe(TOPICLIST);
                        setCallback();
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        // Something went wrong e.g. connection timeout or firewall problems
                        broadcastIntent.setAction(MainActivity.mBroadcastLoginFailure);
                        sendBroadcast(broadcastIntent);
                        Log.d(TAG, "Connection Failure");
                    }
                });
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void disconnect() {
        try {
            client.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void subscribe(String[] topicList) {
        try {
            for (String topic : topicList) {
                IMqttToken subscribeToken = client.subscribe(topic, 1);
                subscribeToken.setActionCallback(new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Log.d(TAG, "Subscription Success");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Log.d(TAG, "Subscription Failure");
                    }
                });
            }

        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void unSubscribe(String[] topicList) {
        try {
            for (String topic : topicList) {
                IMqttToken unSubscribeToken = client.unsubscribe(topic);
                unSubscribeToken.setActionCallback(new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Log.d(TAG, "Unsubscribe Success");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Log.d(TAG, "Unsubscribe Failure");
                    }
                });
            }

        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void publish(String topic, String payload) {
        byte[] encodedPayload;
        try {
            encodedPayload = payload.getBytes("UTF-8");
            MqttMessage message = new MqttMessage(encodedPayload);
            client.publish(topic, message);
        } catch (UnsupportedEncodingException | MqttException e) {
            e.printStackTrace();
            Log.d(TAG, "Publish Failure");
        }
    }

    public void setCallback() {
        client.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {
                Log.d(TAG, "Connection Lost!!");
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                /*if (topic.equals(TEMPTOPIC)) {
                    Log.d(TAG,"Temp Package Received");
                    String[] tempMessage = message.toString().split(",");
                    Intent broadcastIntent = new Intent();
                    broadcastIntent.setAction(TempActivity.mBroadcastTempData);
                    broadcastIntent.putExtra("DataPackage", tempMessage);
                    sendBroadcast(broadcastIntent);
                }*/
                if (topic.equals(GESTURETOPIC)){
                    Log.d(TAG,"Gesture Result Received");
                    String result = message.toString();
                    result = result.substring(1,result.length() - 1);
                    Log.d(TAG, result);
                    Intent broadcastIntent = new Intent();
                    broadcastIntent.setAction(GestureActivity.mBroadcastGestureResult);
                    broadcastIntent.putExtra("RESULT",result);
                    sendBroadcast(broadcastIntent);
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
                Log.d(TAG, "Delivery Complete!");
            }
        });
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
