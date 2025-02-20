package com.example.pj1;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class access extends AppCompatActivity {
    private final String username = "Donner";
    private final String password = "donner";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_access);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Button button = findViewById(R.id.complete_bt);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText username = findViewById(R.id.input_username);
                EditText password = findViewById(R.id.input_password);

                if (!isAppropied(username.getText().toString()) || !isAppropied(password.getText().toString())) {
                    Toast.makeText(v.getContext(), "The username or password inputed is not appropied!", Toast.LENGTH_LONG).show();

                    return;
                }

                if (!isCorrectCredentials(username.toString().trim(), password.toString().trim())) {
                    Toast.makeText(v.getContext(), "Wrong credentials!", Toast.LENGTH_LONG).show();
                    return;
                }

                Toast.makeText(v.getContext(), "Welcome " + username.getText().toString().trim() + "!", Toast.LENGTH_LONG).show();

            }
        });
    }

    private boolean isAppropied (String text) {
        if (text == null) return false;

        boolean result = true;


        if (text.isBlank() || text.isEmpty()) result = false;

        return result;
    }

    private boolean isCorrectCredentials (String username, String password) {
        Toast.makeText(this.getApplicationContext(), "pass username: " + username + "; in username: " + this.username, Toast.LENGTH_LONG);
        Toast.makeText(this.getApplicationContext(), "pass password: " + password + "; in password: " + this.password, Toast.LENGTH_LONG);

        if (username.equals(this.username) || password.equals(this.password)) return false;

        return true;
    }
}