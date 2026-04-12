package com.example.musicremote.ui.settings

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import com.example.musicremote.R
import com.example.musicremote.data.repository.SettingsRepository
import com.example.musicremote.databinding.FragmentSettingsBinding
import kotlinx.coroutines.launch

class SettingsFragment : Fragment() {

    private var _binding: FragmentSettingsBinding? = null
    private val binding get() = _binding!!

    private lateinit var settingsRepo: SettingsRepository

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSettingsBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        settingsRepo = SettingsRepository(requireContext().dataStore)

        lifecycleScope.launch {
            binding.etIpAddress.setText(settingsRepo.getPiIpAddress())
        }

        binding.btnSave.setOnClickListener {
            val ip = binding.etIpAddress.text.toString().trim()
            if (ip.isBlank()) {
                Toast.makeText(requireContext(), "Enter an IP address or hostname", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            lifecycleScope.launch {
                settingsRepo.savePiIpAddress(ip)
                Toast.makeText(requireContext(), "Saved", Toast.LENGTH_SHORT).show()
                findNavController().popBackStack()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

private val android.content.Context.dataStore: androidx.datastore.core.DataStore<androidx.datastore.preferences.core.Preferences>
    by androidx.datastore.preferences.preferencesDataStore(name = "settings")
