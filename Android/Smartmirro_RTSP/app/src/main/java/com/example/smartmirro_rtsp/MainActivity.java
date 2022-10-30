package com.example.smartmirro_rtsp;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements Button.OnClickListener{

    private TextView ipTextView;
    private EditText ipEditText;
    private Button MainNextButton;

    @SuppressLint("WrongViewCast")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipTextView = findViewById(R.id.ipTextView);

        ipEditText = findViewById(R.id.ipEditText);

        MainNextButton = findViewById(R.id.MainNextButton);
        MainNextButton.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.MainNextButton :
                String ip = ipEditText.getText().toString();
                Intent intent = new Intent(getApplicationContext(),MenuActivity.class);
                intent.putExtra("ip",ip);
                startActivity(intent);
                finish();
                break ;
        }
    }
}