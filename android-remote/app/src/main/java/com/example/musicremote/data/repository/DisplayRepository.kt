package com.example.musicremote.data.repository

import com.example.musicremote.data.model.ArtResponse
import com.example.musicremote.data.model.StatusResponse
import com.example.musicremote.data.network.ApiClientProvider

class DisplayRepository(host: String) {
    private val api = ApiClientProvider.get(host)

    suspend fun getStatus(): Result<StatusResponse> = runCatching { api.getStatus() }
    suspend fun getArt(): Result<ArtResponse> = runCatching { api.getArt() }
    suspend fun sendPause(): Result<Unit> = runCatching { api.pause(); Unit }
    suspend fun sendResume(): Result<Unit> = runCatching { api.resume(); Unit }
    suspend fun sendScan(): Result<Unit> = runCatching { api.scan(); Unit }
    suspend fun sendRestart(): Result<Unit> = runCatching { api.restart(); Unit }
}
