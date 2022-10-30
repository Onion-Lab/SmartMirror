package com.example.smartmirro_rtsp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MenuActivity extends AppCompatActivity implements View.OnClickListener {

    private Button RTPS;
    private Button NeoPixel;
    private String ip;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        RTPS = findViewById(R.id.RTPS);
        RTPS.setOnClickListener(this);

        NeoPixel = findViewById(R.id.NeoPixel);
        NeoPixel.setOnClickListener(this);

        Intent intent = getIntent();
        ip = intent.getExtras().getString("ip");
    }

    @Override
    public void onClick(View view) {
        if(view.getId() == R.id.RTPS) {
            Intent intent = new Intent(getApplicationContext(),RTSPActivity.class);
            intent.putExtra("ip",ip);
            startActivity(intent);//액티비티 띄우기
        }
        else if(view.getId() == R.id.NeoPixel){
            Intent intent = new Intent(getApplicationContext(),NeoPixelActivity.class);
            startActivity(intent);//액티비티 띄우기
        }
    }
}