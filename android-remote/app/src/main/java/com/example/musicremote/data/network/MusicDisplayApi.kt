package com.example.musicremote.data.network

import com.example.musicremote.data.model.ArtResponse
import com.example.musicremote.data.model.StatusResponse
import okhttp3.ResponseBody
import retrofit2.http.GET
import retrofit2.http.POST

interface MusicDisplayApi {
    @GET("status")
    suspend fun getStatus(): StatusResponse

    @GET("art")
    suspend fun getArt(): ArtResponse

    @POST("pause")
    suspend fun pause(): ResponseBody

    @POST("resume")
    suspend fun resume(): ResponseBody

    @POST("scan")
    suspend fun scan(): ResponseBody

    @POST("restart")
    suspend fun restart(): ResponseBody
}
