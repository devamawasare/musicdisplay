package com.example.musicremote.ui.nowplaying

import android.graphics.Bitmap
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.musicremote.data.model.TrackInfo
import com.example.musicremote.data.repository.DisplayRepository
import com.example.musicremote.data.repository.SettingsRepository
import com.example.musicremote.util.Base64ImageLoader
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

sealed class DisplayUiState {
    object Loading : DisplayUiState()
    object Unreachable : DisplayUiState()
    data class Paused(val lastTrack: TrackInfo?) : DisplayUiState()
    data class Recognizing(val lastTrack: TrackInfo?) : DisplayUiState()
    data class Playing(val track: TrackInfo, val artBitmap: Bitmap?) : DisplayUiState()
    object NoTrack : DisplayUiState()
}

class NowPlayingViewModel(
    private val settingsRepo: SettingsRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<DisplayUiState>(DisplayUiState.Loading)
    val uiState: StateFlow<DisplayUiState> = _uiState.asStateFlow()

    private var pollJob: Job? = null
    private var lastTrackTitle: String? = null
    private var cachedArt: Bitmap? = null

    fun startPolling() {
        pollJob?.cancel()
        pollJob = viewModelScope.launch {
            val ip = settingsRepo.getPiIpAddress()
            if (ip.isBlank()) {
                _uiState.value = DisplayUiState.Unreachable
                return@launch
            }
            val repo = DisplayRepository(ip)
            while (isActive) {
                val result = repo.getStatus()
                result.fold(
                    onSuccess = { status -> handleStatus(status, repo) },
                    onFailure = { _uiState.value = DisplayUiState.Unreachable }
                )
                delay(3000L)
            }
        }
    }

    private suspend fun handleStatus(
        status: com.example.musicremote.data.model.StatusResponse,
        repo: DisplayRepository
    ) {
        if (status.paused) {
            _uiState.value = DisplayUiState.Paused(status.track)
            return
        }
        if (status.recognizing) {
            _uiState.value = DisplayUiState.Recognizing(status.track)
            return
        }
        val track = status.track
        if (track == null) {
            _uiState.value = DisplayUiState.NoTrack
            return
        }
        if (track.title != lastTrackTitle) {
            lastTrackTitle = track.title
            cachedArt = if (track.hasArt) fetchArt(repo) else null
        }
        _uiState.value = DisplayUiState.Playing(track, cachedArt)
    }

    private suspend fun fetchArt(repo: DisplayRepository): Bitmap? {
        return repo.getArt().getOrNull()?.let { resp ->
            Base64ImageLoader.decode(resp.imageB64)
        }
    }

    fun onPauseResumeClicked() {
        viewModelScope.launch {
            val ip = settingsRepo.getPiIpAddress()
            val repo = DisplayRepository(ip)
            when (_uiState.value) {
                is DisplayUiState.Paused -> repo.sendResume()
                else -> repo.sendPause()
            }
        }
    }

    fun onForceScanClicked() {
        viewModelScope.launch {
            val ip = settingsRepo.getPiIpAddress()
            val repo = DisplayRepository(ip)
            repo.sendScan()
        }
    }

    fun onRestartClicked() {
        viewModelScope.launch {
            val ip = settingsRepo.getPiIpAddress()
            val repo = DisplayRepository(ip)
            repo.sendRestart()
            // Pi will go offline briefly — show loading state while it reboots
            _uiState.value = DisplayUiState.Loading
        }
    }

    fun stopPolling() {
        pollJob?.cancel()
    }

    class Factory(private val settingsRepo: SettingsRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T =
            NowPlayingViewModel(settingsRepo) as T
    }
}
