package com.example.musicremote.data.repository

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

class SettingsRepository(private val dataStore: DataStore<Preferences>) {
    private val KEY = stringPreferencesKey("pi_ip_address")

    // Default to the Pi's known IP address
    suspend fun getPiIpAddress(): String =
        dataStore.data.map { it[KEY] ?: "192.168.1.91" }.first()

    suspend fun savePiIpAddress(ip: String) =
        dataStore.edit { it[KEY] = ip.trim() }
}
