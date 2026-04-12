package com.example.musicremote.ui.nowplaying

import android.os.Bundle
import android.view.LayoutInflater
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import androidx.core.view.MenuProvider
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import com.example.musicremote.R
import com.example.musicremote.data.repository.SettingsRepository
import com.example.musicremote.databinding.FragmentNowPlayingBinding
import com.example.musicremote.dataStore
import kotlinx.coroutines.launch

class NowPlayingFragment : Fragment() {

    private var _binding: FragmentNowPlayingBinding? = null
    private val binding get() = _binding!!

    private val viewModel: NowPlayingViewModel by viewModels {
        NowPlayingViewModel.Factory(
            SettingsRepository(requireContext().dataStore)
        )
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _binding = FragmentNowPlayingBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        requireActivity().addMenuProvider(object : MenuProvider {
            override fun onCreateMenu(menu: Menu, menuInflater: MenuInflater) {
                menuInflater.inflate(R.menu.menu_nowplaying, menu)
            }
            override fun onMenuItemSelected(item: MenuItem): Boolean {
                if (item.itemId == R.id.action_settings) {
                    findNavController().navigate(R.id.action_nowplaying_to_settings)
                    return true
                }
                return false
            }
        }, viewLifecycleOwner, Lifecycle.State.RESUMED)

        binding.btnPauseResume.setOnClickListener { viewModel.onPauseResumeClicked() }
        binding.btnScan.setOnClickListener { viewModel.onForceScanClicked() }
        binding.btnRestart.setOnClickListener { viewModel.onRestartClicked() }

        viewLifecycleOwner.lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state -> render(state) }
            }
        }

        viewModel.startPolling()
    }

    private fun render(state: DisplayUiState) {
        when (state) {
            is DisplayUiState.Loading -> {
                binding.progressBar.visibility = View.VISIBLE
                binding.groupTrack.visibility = View.GONE
                binding.tvStatus.text = "Connecting..."
                binding.btnPauseResume.isEnabled = false
                binding.btnScan.isEnabled = false
            }
            is DisplayUiState.Unreachable -> {
                binding.progressBar.visibility = View.GONE
                binding.groupTrack.visibility = View.GONE
                binding.tvStatus.text = "Can't reach Pi (192.168.1.91)"
                binding.btnPauseResume.isEnabled = false
                binding.btnScan.isEnabled = false
            }
            is DisplayUiState.Paused -> {
                binding.progressBar.visibility = View.GONE
                binding.tvStatus.text = "Paused"
                binding.btnPauseResume.text = "Resume"
                binding.btnPauseResume.isEnabled = true
                binding.btnScan.isEnabled = false
                showTrack(state.lastTrack, null)
            }
            is DisplayUiState.Recognizing -> {
                binding.progressBar.visibility = View.VISIBLE
                binding.tvStatus.text = "Listening..."
                binding.btnPauseResume.text = "Pause"
                binding.btnPauseResume.isEnabled = true
                binding.btnScan.isEnabled = false
                showTrack(state.lastTrack, null)
            }
            is DisplayUiState.Playing -> {
                binding.progressBar.visibility = View.GONE
                binding.tvStatus.text = "Now Playing"
                binding.btnPauseResume.text = "Pause"
                binding.btnPauseResume.isEnabled = true
                binding.btnScan.isEnabled = true
                binding.groupTrack.visibility = View.VISIBLE
                binding.tvTitle.text = state.track.title
                binding.tvArtist.text = state.track.artist ?: ""
                binding.tvAlbum.text = state.track.album ?: ""
                if (state.artBitmap != null) {
                    binding.imgArt.setImageBitmap(state.artBitmap)
                    binding.imgArt.visibility = View.VISIBLE
                } else {
                    binding.imgArt.visibility = View.GONE
                }
            }
            is DisplayUiState.NoTrack -> {
                binding.progressBar.visibility = View.GONE
                binding.groupTrack.visibility = View.GONE
                binding.tvStatus.text = "Nothing playing"
                binding.btnPauseResume.text = "Pause"
                binding.btnPauseResume.isEnabled = true
                binding.btnScan.isEnabled = true
            }
        }
    }

    private fun showTrack(track: com.example.musicremote.data.model.TrackInfo?, art: android.graphics.Bitmap?) {
        if (track != null) {
            binding.groupTrack.visibility = View.VISIBLE
            binding.tvTitle.text = track.title
            binding.tvArtist.text = track.artist ?: ""
            binding.tvAlbum.text = track.album ?: ""
            binding.imgArt.visibility = View.GONE
        } else {
            binding.groupTrack.visibility = View.GONE
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
