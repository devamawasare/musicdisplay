package com.example.musicremote.data.model

import com.google.gson.annotations.SerializedName

data class StatusResponse(
    val paused: Boolean,
    val recognizing: Boolean,
    val track: TrackInfo?
)

data class TrackInfo(
    val title: String,
    val artist: String?,
    val album: String?,
    @SerializedName("has_art") val hasArt: Boolean
)
