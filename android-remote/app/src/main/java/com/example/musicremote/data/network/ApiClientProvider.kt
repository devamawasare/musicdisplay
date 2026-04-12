package com.example.musicremote.data.network

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ApiClientProvider {
    private var currentHost: String = ""
    private var retrofit: Retrofit? = null

    fun get(host: String): MusicDisplayApi {
        if (host != currentHost || retrofit == null) {
            currentHost = host
            val client = OkHttpClient.Builder()
                .connectTimeout(3, TimeUnit.SECONDS)
                .readTimeout(5, TimeUnit.SECONDS)
                .build()
            retrofit = Retrofit.Builder()
                .baseUrl("http://$host:5000/")
                .client(client)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }
        return retrofit!!.create(MusicDisplayApi::class.java)
    }
}
