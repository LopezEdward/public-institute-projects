package com.example.pj1;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        Button button = this.findViewById(R.id.accessButton);
        button.setOnClickListener(v -> {
            Intent intent = new Intent(v.getContext(), access.class);
            startActivity(intent);
        });
    }
    /*
    @Override
    public void onStart () {
        //System.out.println(this.getContentScene().getSceneRoot().getChildCount());
        super.onStart();
        Toast.makeText(this.getApplication(), "HELLO WORLD!", Toast.LENGTH_LONG).show();

    }

    @Override
    public void onResume () {
        super.onResume();
        Toast.makeText(this.getApplication(), "I miss you <3", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onStop () {
        super.onStop();
        Toast.makeText(this.getApplication(), "I hate you *angry*", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onPause () {
        super.onPause();

        Toast.makeText(this.getApplication(), "I feel stopped xD", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onRestart () {
        super.onRestart();
        Toast.makeText(this.getApplication(), "Win32.dll error!", Toast.LENGTH_LONG).show();
    }

    @Override
    public void onDestroy () {
        super.onDestroy();

        Toast.makeText(this.getApplication(), "NOOOOOOOOOOOO *self destroyed xD* ", Toast.LENGTH_LONG).show();
    }*/
}