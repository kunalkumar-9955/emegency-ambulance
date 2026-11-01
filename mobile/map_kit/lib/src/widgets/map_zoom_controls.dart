import 'package:flutter/material.dart';

import '../controllers/map_controller.dart';

class MapZoomControls extends StatelessWidget {
  const MapZoomControls({
    super.key,
    required this.controller,
    this.onDarkModeToggle,
    this.showDarkToggle = true,
  });

  final EmergencyMapController controller;
  final VoidCallback? onDarkModeToggle;
  final bool showDarkToggle;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        _btn(Icons.add, controller.zoomIn),
        const SizedBox(height: 8),
        _btn(Icons.remove, controller.zoomOut),
        const SizedBox(height: 8),
        _btn(Icons.my_location, controller.centerOnUser),
        if (showDarkToggle) ...[
          const SizedBox(height: 8),
          _btn(
            controller.darkMode ? Icons.light_mode : Icons.dark_mode,
            onDarkModeToggle ?? controller.toggleDarkMode,
          ),
        ],
      ],
    );
  }

  Widget _btn(IconData icon, VoidCallback onTap) {
    return Material(
      elevation: 3,
      borderRadius: BorderRadius.circular(8),
      color: Colors.white,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: SizedBox(
          width: 44,
          height: 44,
          child: Icon(icon, color: const Color(0xFF0F172A)),
        ),
      ),
    );
  }
}
