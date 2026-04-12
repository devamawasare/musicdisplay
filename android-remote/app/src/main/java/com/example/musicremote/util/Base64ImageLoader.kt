package com.example.musicremote.util

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64

object Base64ImageLoader {
    fun decode(b64: String): Bitmap? = runCatching {
        val bytes = Base64.decode(b64, Base64.DEFAULT)
        BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
    }.getOrNull()
}
